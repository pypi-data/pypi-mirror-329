# Standard Imports
from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING

# Third Party Imports
import yamlcore

# Local Imports
from pipeline_flow.common.utils import SingletonMeta
from pipeline_flow.core.parsers import secret_parser

# Type Imports
if TYPE_CHECKING:
    from io import StringIO
    from typing import Match, Self

    from yaml.nodes import Node

    from pipeline_flow.common.type_def import PluginRegistryJSON, StreamType


type JSON_DATA = dict

DEFAULT_CONCURRENCY = 2

ENV_VAR_YAML_TAG = "!env_var"
ENV_VAR_PATTERN = re.compile(r"\${{\s*env\.([^}]+?)\s*}}")

SECRET_YAML_TAG = "!secret"  # noqa: S105 - False Positive
SECRET_PATTERN = re.compile(r"\${{\s*secrets\.([^}]+?)\s*}}")

VARIABLE_YAML_TAG = "!variable"
VARIABLE_PATTERN = re.compile(r"\${{\s*variables\.([^}]+?)\s*}}")


class YamlAttribute(StrEnum):
    SECRETS = "secrets"
    VARIABLES = "variables"
    PIPELINES = "pipelines"
    PLUGINS = "plugins"
    CONCURRENCY = "concurrency"


@dataclass(frozen=True)
class YamlConfig(metaclass=SingletonMeta):
    concurrency: int = DEFAULT_CONCURRENCY


class ExtendedCoreLoader(yamlcore.CCoreLoader):
    """An extension of YAML 1.2 Compliant Loader to handle boolean values like `on` or `off`."""

    def __init__(self: Self, stream: StreamType) -> None:
        super().__init__(stream)
        self.secrets = {}
        self.variables = {}

    def update_variables(self: Self, new_variables: dict[str, str]) -> None:
        """Update the variables dynamically after initialization."""
        self.variables.update(new_variables)

    def update_secrets(self: Self, new_secrets: dict[str, str]) -> None:
        """Update the secrets dynamically after initialization."""
        self.secrets.update(new_secrets)

    def substitute_env_var_placeholder(self: Self, node: Node) -> str:
        """Parses a YAML node for an env var reference and replaces it with the value.

        Args:
            node (Node): A YAML node containing the `!env_var` reference added by implicit resolver.

        Raises:
            ValueError: If the environment variable is not set.

        Returns:
            str: A String with the environment variable's value.
        """
        value = node.value

        for match in ENV_VAR_PATTERN.finditer(value):
            match_group = match.group()
            env_key = match.group(1)

            env_var_value = os.environ.get(env_key, None)
            if not env_var_value:
                error_msg = f"Environment variable `{env_key}` is not set."
                raise ValueError(error_msg)

            value = value.replace(match_group, env_var_value)
        return value

    def substitute_variable_placeholder(self: Self, node: Node) -> str:
        """Parses a YAML node for a variable reference and replaces it with the value.

        If the value is a single variable, it returns the original type (int, dict, etc.).
        Else it converts the value to a string for inline substitution.

        Args:
            node (Node): A YAML node containing the `!variable` reference added by implicit resolver.

        Returns:
            str: A String with the variable's value.
        """
        value = node.value

        # Check if the entire value is just a single variable (preserve original type)
        full_match = VARIABLE_PATTERN.fullmatch(value)
        if full_match:
            variable_key = full_match.group(1)
            if variable_key not in self.variables:
                msg = f"Variable `{variable_key}` is not set."
                raise ValueError(msg)
            return self.variables[variable_key]  # Return the original type (int, dict, etc.)

        # Use re.sub with a callback for single-pass substitution of variables in strings
        def replace_match(match: Match) -> str:
            variable_key = match.group(1)
            if variable_key not in self.variables:
                msg = f"Variable `{variable_key}` is not set."
                raise ValueError(msg)
            return str(self.variables[variable_key])  # Convert to string for inline substitution

        return VARIABLE_PATTERN.sub(replace_match, value)

    def substitute_secret_placeholder(self: Self, node: Node) -> str:
        """Parses a YAML node for a secret reference and replaces it with the value.

        Args:
            node (Node): A YAML node containing the `!secret` reference added by implicit resolver.

        Returns:
            str: A String with the secret's value.
        """
        value = node.value
        match = SECRET_PATTERN.match(value)

        secret_key = match.group(1)

        if secret_key not in self.secrets:
            error_msg = (
                f"Secret `{secret_key}` is not set. "
                "Ensure that variables/secrets are defined in the first document YAML."
            )
            raise ValueError(error_msg)
        return self.secrets[secret_key]


# Register the implicit resolver to detect '${{ env.KEY }}'
ExtendedCoreLoader.add_implicit_resolver(ENV_VAR_YAML_TAG, ENV_VAR_PATTERN, None)
ExtendedCoreLoader.add_constructor(ENV_VAR_YAML_TAG, ExtendedCoreLoader.substitute_env_var_placeholder)

# Register the implicit resolver to detect '${{ secrets.KEY }}'
ExtendedCoreLoader.add_implicit_resolver(SECRET_YAML_TAG, SECRET_PATTERN, None)
ExtendedCoreLoader.add_constructor(SECRET_YAML_TAG, ExtendedCoreLoader.substitute_secret_placeholder)

# Register the implicit resolver to detect '${{ variables.KEY }}'
ExtendedCoreLoader.add_implicit_resolver(VARIABLE_YAML_TAG, VARIABLE_PATTERN, None)
ExtendedCoreLoader.add_constructor(VARIABLE_YAML_TAG, ExtendedCoreLoader.substitute_variable_placeholder)


class YamlParser:
    """YamlParser class that parses YAML content and returns the parsed data.

    Internally, it uses PyYAML Reader class to parse the YAML. That reader accepts:
        - a `bytes` object
        - a `str` object
        - a file-like object with its `read` method returning `str`
        - a file-like object with its `read` method returning `unicode`
        - a file path (automatically read)
    """

    def __init__(self: Self, stream: StreamType, *, read_local_file: bool = False) -> None:
        converted_stream = self._convert_to_stream(stream, read_local_file=read_local_file)
        self.content = self.load(converted_stream)

    @classmethod
    def from_input(cls: type[Self], yaml_text: StreamType | None, file_path: str | None) -> Self:
        """Initializes YamlParser using either a YAML text or a local file path.

        Args:
            yaml_text (StreamType | None): YAML content as a string or stream.
            file_path (str | None): Local file path to a YAML file.

        Returns:
            YamlParser: An instance of YamlParser.

        Raises:
            ValueError: If neither yaml_text nor file_path is provided.
        """
        if not yaml_text and not file_path:
            raise ValueError("Either yaml_text or file_path must be provided.")
        # Prioritize YAML text if provided.
        stream = yaml_text if yaml_text is not None else file_path
        read_local_file = file_path is not None and yaml_text is None

        # Initialize YAML parser
        return cls(stream=stream, read_local_file=read_local_file)

    @staticmethod
    def _read_file(file_path: str) -> StringIO:
        """Reads the content of the file and returns it."""
        try:
            # async with aiofiles.open(file_path, encoding="utf-8") as file.
            # This works but need to test if async is needed at this point.
            with Path(file_path).open("r") as file:
                return file.read()
        except FileNotFoundError:
            error_msg = f"File not found: {file_path}"
            logging.error(error_msg)
            raise

    def _convert_to_stream(self: Self, source: StreamType, *, read_local_file: bool) -> StreamType:
        """Converts the content to a stream and returns it."""
        if isinstance(source, str):
            if read_local_file:
                return self._read_file(source)
            return source
        return source

    @staticmethod
    def load(stream: StreamType) -> JSON_DATA:
        """Loads the YAML content from the stream and returns the parsed data.

        It is a wrapper over yaml.load_all() to handle the secrets and env variables.

        Args:
            stream (StreamType): The stream to read the YAML content from.

        Returns:
            JSON_DATA: A dictionary containing the parsed YAML content.
        """
        loader = ExtendedCoreLoader(stream)

        try:
            while loader.check_data():
                data = loader.get_data()

                if YamlAttribute.SECRETS in data:
                    secrets = secret_parser(data[YamlAttribute.SECRETS])
                    loader.update_secrets(secrets)

                if YamlAttribute.VARIABLES in data:
                    variables = data[YamlAttribute.VARIABLES]
                    loader.update_variables(variables)

                if YamlAttribute.SECRETS in data or YamlAttribute.VARIABLES in data:
                    # Skip the document if it contains secrets or variables and move to the next document
                    # to ensure that the secrets and variables are updated before parsing the next document.
                    continue

                return data
        finally:
            loader.dispose()

    def get_pipelines_dict(self: Self) -> JSON_DATA:
        """Return the 'pipelines' section from the parsed YAML."""
        return self.content.get(YamlAttribute.PIPELINES, {})

    def get_plugins_dict(self: Self) -> PluginRegistryJSON | None:
        """Return the 'plugins' section from the parsed YAML."""
        return self.content.get(YamlAttribute.PLUGINS, None)

    def initialize_yaml_config(self: Self) -> YamlConfig:
        """Initialize the YAML Configuration object with the default values or passed in."""
        # Create the map of attributes with their values
        attrs_map = {
            YamlAttribute.CONCURRENCY: self.content.get(YamlAttribute.CONCURRENCY, DEFAULT_CONCURRENCY),
        }

        # Filter out the None values
        attrs = {key: value for key, value in attrs_map.items() if value is not None}

        return YamlConfig(**attrs)
