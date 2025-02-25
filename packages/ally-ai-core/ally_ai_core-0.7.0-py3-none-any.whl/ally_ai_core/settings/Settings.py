import yaml
from typing import List, Literal
from ..errors import YamlParseError
import logging

import re
import os


class Settings(dict):
    """
    Represents app settings yaml file
    """

    def __init__(self,
                 section: str,
                 path="./app-settings.yaml",
                 **kwargs):
        """
        Reads given yaml file
        - Use kwargs to override values
        """
        super().__init__()
        self.path = path
        self.section = section

        try:
            # read yaml file
            yaml_content = self._read_yaml(path)

            self._replace_with_environment_variables(yaml_content)

            # add values
            yaml_section = yaml_content[section]
            for key, value in yaml_section.items():
                self[key] = value

            # override values
            self.update({key: value for key, value in kwargs.items()})

        except Exception as ex:
            logging.error(
                f"Failed to read '{section}' section from '{self.path}'. Original: {ex}"
            )
            raise

    def _read_yaml(self, path):
        try:
            with open(path, "r") as file:
                yaml_content = yaml.safe_load(file)
                return yaml_content
        except FileNotFoundError:
            raise
        except Exception as ex:
            raise YamlParseError(
                f"File '{self.path}' could not be parsed correcty to yaml! Original: {ex}"
            )

    def _set_nested_value(self, yaml_data: dict, keys: List[str], value):
        for key in keys[:-1]:
            yaml_data = yaml_data.setdefault(key, {})
        if value is not None and value:
            yaml_data[keys[-1]] = value

    def _replace_with_environment_variables(self, yaml_content):
        # Pattern to match environment variables with double underscores
        pattern = re.compile(r"(?i)^[a-z][a-z0-9_]*(?:__[a-z][a-z0-9_]*)+$")

        # Process each environment variable
        for key, value in os.environ.items():
            if pattern.match(key):
                # Split the key into parts
                keys = key.lower().split("__")
                # Update the YAML configuration
                self._set_nested_value(yaml_content, keys, value)

    def __repr__(self) -> str:
        return self._hide_keys().__repr__()

    def __str__(self) -> str:
        return self._hide_keys().__str__()

    def _hide_keys(self) -> dict:
        temp = super().copy()
        special_words = ["password", "key", "token", "secret"]
        pairs = [
            (key, value)
            for key, value in temp.items()
            if any(word in key for word in special_words)
        ]
        for key, value in pairs:
            value_str = str(value)
            temp[key] = f"{value_str[:1]}*****{value_str[-1:]}"
        return temp
