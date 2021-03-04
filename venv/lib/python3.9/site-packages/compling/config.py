import pkg_resources
from typing import *
from configparser import ConfigParser


class ConfigManager:

    def __init__(self) -> None:
        self.__config_path__ = pkg_resources.resource_filename('compling', 'config.ini')
        self.__config_parser__ = None
        self.__config_load__()

    def __config_load__(self) -> None:
        """Loads set-up parameters."""

        self.__config_parser__ = ConfigParser(interpolation=None)
        self.__config_parser__.read(self.__config_path__)


    def cat(self) -> None:
        """Shows set-up parameters."""
        with open(self.__config_path__, mode='r') as f:
            cat = f.read()
        print(cat)

    def updates(self, sections_key_values: List[Tuple[str]]) -> None:
        """Updates some set-up parameters.

        Args:
           sections_key_values (List[Tuple[str]]): Each tuple must consist of 3 strings: (section, key, value)
        """

        for section, key, value in sections_key_values:
            self.__config_parser__.set(section, key, value)

        # Write changes back to file
        with open(self.__config_path__, mode='w') as f_config:
            self.__config_parser__.write(f_config)

    def update(self, s: str, k: str, v: str) -> None:
        """Updates the set-up parameter "k" with the value "v" in the section "s".

        Args:
           s (str): Section name.
           k (str): Section key.
           v (str): New k value.
        """

        self.__config_parser__.set(s, k, v)

        # Write changes back to file
        with open(self.__config_path__, mode='w') as f_config:
            self.__config_parser__.write(f_config)

    def get(self, s: str, k: str) -> str:
        """Returns the value "v" for the key "k" in the section "s" """

        return self.__config_parser__[s][k]

    def get_section(self, s: str) -> dict:
        """Returns the set-up parameters in a section "s" """

        return dict(self.__config_parser__._sections[s])

    def reset(self) -> None:
        """Resets the set-up parameters."""

        with open(pkg_resources.resource_filename('compling', 'default_config.ini'), mode='r') as f:
            default = f.read()
        with open(self.__config_path__, mode='w') as f:
            f.write(default)

        self.__config_load__()

    def __whereisconfig__(self) -> str:
        """Shows the configuration file location."""

        return pkg_resources.resource_filename('compling', self.__config_path__)
