# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""File loading utilities."""

import json
from pathlib import Path

import bespon
import toml
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from .exceptions import ElectiveFileLoadingError


def _load_file(
    fn,
    loader=toml.load,
    decode_exc=toml.TomlDecodeError,
    section=None,
    raise_on_error=True,
):
    """Load a configuration file.

    Load a configuration file, optionally only returning the specified
    sub-dictionary ``section``, as in a ``tool`` section of a
    ``pyproject.toml`` file.

    Parameters
    ----------
    loader : function
        A function to load and parse the configuration file, such as
        ``toml.load()``.
    fn : string
        The path of the file to load.
    section : string
        Optional section of the file to load.
    raise_on_error : boolean
        Raise exception on error, or fail silently and return an empty
        dict.  Default is ``True``.

    Returns
    -------
    dict
       Dictionary corresponding to the data in the TOML file.

    Raises
    ------
    elective.ElectiveFileLoadingError
        Raised if the configuration file does not exist, is not
        readable, or is not parsable for a given format.
    """
    # Check if ``fn`` is a file.  Raise or return if not.
    if not Path(fn).is_file():
        if raise_on_error:
            raise ElectiveFileLoadingError(f"file {fn} not found")
        else:
            return {}

    # Return the loaded data.  Raise or return on any problems.
    try:
        with open(fn, "r") as f:
            contents = loader(f)

            if section:
                for k in section.lstrip("[").rstrip("]").split("."):
                    contents = contents[k]
                return contents
            else:
                return contents

    except (decode_exc, FileNotFoundError) as error:
        if raise_on_error:
            raise ElectiveFileLoadingError(str(error))
        else:
            return {}


def load_toml_file(fn, section=None, raise_on_error=True):
    """Load a TOML file."""
    return _load_file(
        fn,
        loader=toml.load,
        decode_exc=toml.TomlDecodeError,
        section=section,
        raise_on_error=raise_on_error,
    )


def load_json_file(fn, section=None, raise_on_error=True):
    """Load a JSON file."""
    return _load_file(
        fn,
        loader=json.load,
        decode_exc=json.JSONDecodeError,
        section=section,
        raise_on_error=raise_on_error,
    )


def load_yaml_file(fn, section=None, raise_on_error=True):
    """Load a YAML file."""
    yaml = YAML(typ="safe")

    return _load_file(
        fn,
        loader=yaml.load,
        decode_exc=YAMLError,
        section=section,
        raise_on_error=raise_on_error,
    )


def load_bespon_file(fn, section=None, raise_on_error=True):
    """Load a BespON file."""
    return _load_file(
        fn,
        loader=bespon.load,
        decode_exc=bespon.erring.DecodingException,
        section=section,
        raise_on_error=raise_on_error,
    )
