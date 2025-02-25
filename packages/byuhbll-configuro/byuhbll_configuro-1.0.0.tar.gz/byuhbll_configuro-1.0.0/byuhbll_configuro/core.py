"""
Provides configuration related functionality.
"""

import copy
from collections import abc
from collections.abc import Mapping
from os import environ
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    MutableMapping,
    Optional,
    Sequence,
    TextIO,
    Type,
    TypeVar,
    Union,
    cast,
)

import yaml

__all__ = ['Config', 'EnvYamlConfig', 'YamlConfig', 'load', 'merge']

TConfig = TypeVar('TConfig', bound='Config')
TYamlConfig = TypeVar('TYamlConfig', bound='YamlConfig')
TEnvYamlConfig = TypeVar('TEnvYamlConfig', bound='EnvYamlConfig')

INHERITANCE_SENTINEL = '...'


def correct_index(index: str, config: Union[list, dict]) -> Union[int, str]:
    """Converts a str to an int if the config is a list."""
    return int(index) if isinstance(config, list) else index


def merge(*dicts: MutableMapping[str, Any]) -> Dict[str, Any]:
    """
    Returns a `dict` that is the result of merging all mutable mappings in 'dicts'.
    `dict` with highest precedence should be passed last

    Arguments:
        *dicts - a variable number of mutable mappings passed as positional args

    """
    all_dicts = all(isinstance(element, abc.MutableMapping) for element in dicts)

    if not all_dicts:
        raise ValueError('Each arg must be a dict or other MutableMapping')

    new: dict = {}
    for d in dicts:
        for key, value in d.items():
            # recursively traverse nested dicts
            if isinstance(value, abc.MutableMapping) and value:
                new[key] = merge(new.get(key, {}), value)
            # no need for tuple, !!python/tuple can't be parsed with yaml.safe_load()
            elif isinstance(value, list) and INHERITANCE_SENTINEL in value:
                sentinel_index = value.index(INHERITANCE_SENTINEL)
                sentinel_leapfrog = sentinel_index + 1
                # replace sentinel value with parent list values
                new[key] = (
                    value[:sentinel_index]
                    + new.get(key, [])
                    + value[sentinel_leapfrog:]
                )
            elif value is None:
                continue
            else:  # found leaf node (str, int, list w/o sentinel, etc.)
                new[key] = value
    return new


class Config(Mapping):
    """A class to store configuration values."""

    delimiter = '/'

    def __init__(self, **configuration: Any) -> None:
        self._config = configuration

    @classmethod
    def build(
        cls: Type[TConfig], *, dicts: Optional[List[dict]] = None, **init_kwargs: Any
    ) -> TConfig:
        """
        Class method for instantiating a Config from a list of dictionaries.
        """
        if dicts:
            one_dict = merge(*dicts, init_kwargs)
            return cls(**cast(dict, one_dict))
        else:
            return cls()

    # Start by filling-out the abstract methods
    def __len__(self):
        return len(self._config)

    def __iter__(self: TConfig) -> Iterator[str]:
        return iter(self._config)

    def __getitem__(self: TConfig, key: Sequence):
        if isinstance(key, str):
            path: Sequence[str] = key.split(self.delimiter)
        elif isinstance(key, Sequence):
            path = key
        else:
            raise TypeError('expected Sequence (str, list, tuple)')
        current_config: Union[list, dict] = self._config
        for part in path:
            index = correct_index(part, current_config)
            # may raise to exit early if the path doesn't exist
            value = current_config[cast(Any, index)]
            current_config = value
        return value

    # Now we get Mapping mixins for free
    # keys, items, values, get, __eq__, __ne__, __contains__
    # modify .get() to be compatible with indexes
    def get(self: TConfig, key_path: Sequence, default: Any = None) -> Any:
        """
        Returns the nested configuration value found at key_path.
        If the path doesn't exist, returns the default.

        Arguments:
            key_path (Sequence): A path through the configuration either:
                                 1. a string separated by self.delimiter,
                                    e.g. `config.get('general/debug')`
                                 2. a pre-split sequence,
                                    e.g. `config.get(('general', 'debug'))
            default (any): Value to return if the path doesn't exist.
        """
        try:
            return self[key_path]
        except (KeyError, IndexError):
            return default

    def dict_copy(self: TConfig) -> dict:
        """Return a copy of the configuration that is a plain old dict."""
        return copy.deepcopy(self._config)


class YamlConfig(Config):
    """Yaml configuration."""

    @staticmethod
    def _parse_yaml(yml: Union[TextIO, str]) -> dict:
        return yaml.safe_load(yml) or {}

    @classmethod
    def _get_config_dict_from_yaml(cls: Type[TYamlConfig], file: str) -> dict:
        """
        Returns a dictionary read from a YAML file.
        """
        with Path(file).open() as data_file:
            return cls._parse_yaml(cast(TextIO, data_file))

    @classmethod
    def build(
        cls: Type[TYamlConfig],
        *,
        yaml_str: Optional[str] = None,
        yaml_files: Optional[List[str]] = None,
        dicts: Optional[List[dict]] = None,
        **init_kwargs: Any,
    ) -> TYamlConfig:
        """
        Instantiates a YamlConfig.
        """
        configs = [init_kwargs]

        if dicts:
            configs.extend(dicts)

        if yaml_files:
            files = (file for file in yaml_files if file)

            for file in files:
                configs.append(cls._get_config_dict_from_yaml(file))

        elif yaml_str:
            yaml_dict = cls._parse_yaml(yaml_str)
            configs.append(yaml_dict)

        return super().build(dicts=configs)


class EnvYamlConfig(YamlConfig):
    """An YamlConfig object with additional environment variable support."""

    def __init__(self: TEnvYamlConfig, env_prefix: str = '', **kwargs: Any) -> None:
        self.env_prefix = env_prefix
        super().__init__(**kwargs)
        # Add environ attribute with environment variables matching the prefix
        self.environ = {
            k: v for k, v in environ.items() if k.startswith(self.env_prefix)
        }
        # override the generated configs with environment variables
        self.override_with_environ()

    def override_with_environ(self: TEnvYamlConfig) -> None:
        """
        Override existing configs with matching env vars.

        To specify a deep path, double underscores (__) are used in environment
        variable names. If there is not a matching configuration, the
        environment variable is ignored (but is still available in
        self.environ).

        For example, if you have a config file with the following:

            django:
              databases:
                default:
                  ENGINE: "django.db.backends.sqlite"
                  NAME: "default.db"
              secret_key: "asdf"

        You can override the default database name with the following
        environment variable (assuming the environment variable prefix is
        DJANGO_):

            DJANGO_django__databases__default__NAME=test.db

        Notice that after the prefix (DJANGO_) the parts of the path are case
        sensitive and are separated by double underscores.

        The double underscore path exists to support the need to override
        variables with a single underscore in the name. So to override
        secret_key, you could provide the following:

            DJANGO_django__secret_key=fdsa
        """
        for var, value in self.environ.items():
            # prefix slice, if prefix is DJANGO, this will remove DJANGO_
            prefix_part = len(self.env_prefix) + 1
            path = var[prefix_part:].split('__')
            config: Union[list, dict] = self._config
            # Go through all but the last element of the path to get the
            # configuration object that contains the final configuration.
            for i in path[:-1]:
                index = correct_index(i, config)
                try:
                    config = config[cast(Any, index)]
                except (IndexError, KeyError):
                    break
            else:
                # Reached the final configuration, if the last index exists,
                # then we will override it with the value from the environment
                # variable
                index = correct_index(path[-1], config)
                if not self._in_config(index, config):
                    continue

                # It exists, time to override. We treat the environment
                # variable value as a YAML value, performing a safe cast
                # from str to its proper class.
                config[cast(Any, index)] = yaml.safe_load(value)

    @staticmethod
    def _in_config(index: Union[int, str], config: Union[list, dict]):
        """Determine if the index exists in the config."""
        in_dict = isinstance(config, dict) and index in config
        in_list = isinstance(config, list) and cast(int, index) < len(config)
        return in_dict or in_list

    @classmethod
    def build(
        cls: Type[TEnvYamlConfig],
        *,
        env_prefix: str = '',
        yaml_str: Optional[str] = None,
        yaml_files: Optional[List[str]] = None,
        dicts: Optional[List[dict]] = None,
        **init_kwargs: Any,
    ) -> TEnvYamlConfig:
        """
        Instantiates an EnvYamlConfig.
        """

        config = super().build(
            yaml_str=yaml_str,
            yaml_files=yaml_files,
            dicts=dicts,
            env_prefix=env_prefix.upper(),
            **init_kwargs,
        )

        return config


def load(
    env_prefix: str = 'DJANGO',
    config_filename: str = 'config.yml',
    **additional_configurations: Any,
) -> EnvYamlConfig:
    """
    Loads a config file and those it extends from, merges them, and returns an
    instance of EnvYamlConfig.
    """
    config_var: str = '{}_CONFIG'.format(env_prefix.upper())
    config_yaml_file: str = environ.get(config_var, config_filename)
    config_files = get_config_file_names(config_yaml_file)

    return EnvYamlConfig.build(
        yaml_files=config_files,
        env_prefix=env_prefix,
        **additional_configurations,
    )


def get_config_file_names(config_file: str) -> List[str]:
    """
    Traverses the path of yaml config files extended from to return an
    inheritance list of filenames.
    """
    config = Path(config_file).resolve()
    base_dir = config.parent
    with config.open() as yaml_file:
        file_contents = yaml.safe_load(yaml_file)
        extends = file_contents.get('extends')

    files = [config_file]
    if extends:
        files = get_config_file_names(base_dir / extends) + files

    return files
