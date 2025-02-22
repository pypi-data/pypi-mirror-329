#  Copyright © 2025 Brockmann Consult GmbH.
#  This software is distributed under the terms and conditions of the
#  MIT license (https://mit-license.org/).

import sys
from os import PathLike
from pathlib import Path
from typing import Any

import fsspec

from xrlint.config import Config
from xrlint.util.formatting import format_message_type_of
from xrlint.util.importutil import ValueImportError, import_value


def read_config(config_path: str | Path | PathLike[str]) -> Config:
    """Read configuration from configuration file.

    Args:
        config_path: configuration file path.

    Returns:
        A `Config` instance.

    Raises:
        TypeError: if `config_path` is not a path-like object
        FileNotFoundError: if configuration file could not be found
        ConfigError: if the configuration could not be read or is
            otherwise invalid.
    """
    if not isinstance(config_path, (str, Path, PathLike)):
        raise TypeError(
            format_message_type_of("config_path", config_path, "str|Path|PathLike")
        )

    try:
        config_like = _read_config_like(str(config_path))
    except FileNotFoundError:
        raise
    except OSError as e:
        raise ConfigError(config_path, e) from e

    try:
        return Config.from_value(config_like)
    except (ValueError, TypeError) as e:
        raise ConfigError(config_path, e) from e


def _read_config_like(config_path: str) -> Any:
    if config_path.endswith(".yml") or config_path.endswith(".yaml"):
        return _read_config_yaml(config_path)
    if config_path.endswith(".json"):
        return _read_config_json(config_path)
    if config_path.endswith(".py"):
        return _read_config_python(config_path)
    raise ConfigError(config_path, "unsupported configuration file format")


def _read_config_yaml(config_path) -> Any:
    import yaml

    with fsspec.open(config_path, mode="r") as f:
        try:
            return yaml.load(f, Loader=yaml.SafeLoader)
        except yaml.YAMLError as e:
            raise ConfigError(config_path, e) from e


def _read_config_json(config_path) -> Any:
    import json

    with fsspec.open(config_path, mode="r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(config_path, e) from e


def _read_config_python(config_path: str) -> Any:
    module_path = Path(config_path)

    if not module_path.exists():
        raise FileNotFoundError(f"file not found: {config_path}")

    module_parent = module_path.parent
    module_name = module_path.stem

    old_sys_path = sys.path
    sys.path = [module_parent.as_posix()] + sys.path
    try:
        return import_value(
            module_name,
            "export_config",
            factory=Config.from_value,
        )[0]
    except ValueImportError as e:
        raise ConfigError(config_path, e) from e
    finally:
        sys.path = old_sys_path


class ConfigError(Exception):
    """An error raised if loading of configuration fails."""

    def __init__(self, config_path: str, e: Exception | str | None = None):
        super().__init__(config_path if e is None else f"{config_path}: {e}")
