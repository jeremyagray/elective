# ******************************************************************************
#
# elective, a Python configuration loader generator
#
# Copyright 2021-2025 Jeremy A Gray <gray@flyquackswim.com>.
#
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Utility functions."""

import json

import bespon
import toml
from ruamel.yaml import YAML, YAMLError

from .exceptions import ElectiveFileDecodingError


def _is_listdict(d):
    """Determine if the keys of a dict are list indices."""
    # All integers?
    keys = []
    for k in d.keys():
        try:
            keys.append(int(k))
        except ValueError:
            return False

    keys = sorted(keys)

    # Zero start?
    if min(keys) != 0:
        return False

    # Consecutive?
    if keys != list(range(0, max(keys) + 1)):
        return False

    return True


def _convert_dict_to_list(d):
    """Convert a list-style dict to a list."""
    keys = sorted(d.keys())
    the_list = []
    for k in keys:
        the_list.append(d[k])

    return the_list


def _flatten_to_list(ds):
    """Convert lists as dicts to lists in a data structure."""
    for k in ds.keys():
        if isinstance(ds[k], dict):
            # If the item points a dict, descend.
            ds[k] = _flatten_to_list(ds[k])
            # We're back.  Now check if the dict is a list-style dict
            # and maybe convert to a list.
            if _is_listdict(ds[k]):
                ds[k] = _convert_dict_to_list(ds[k])

    return ds


def _format_sh(k, v, prefix):
    """Format a configuration value as a Bourne shell environment variable."""
    return f"export {prefix!s}{k!s}='{v!s}'"


def _get_section(config, section):
    """Get a section of a configuration file.

    Get a section (sub-dict) of a configuration file dict.

    Parameters
    ----------
    config : dict
        A configuration file decoded as a dict.
    section: iterable
        A sequence of top-down sub-dicts that locates the desired
        section.  The tuple ``("tool", "poetry")`` would point to
        the ``[tool.poetry]`` section of a ``pyproject.toml`` file.

    Returns
    -------
    dict
        The indicated sub-dict of the configuration dict.

    """
    contents = config

    for k in section:
        contents = contents[k]

    return contents


def _file_loader(
    fn,
    loader,
    decoding_error,
    section=None,
):
    """Load a configuration file.

    Load a configuration file, optionally only returning the
    specified sub-dictionary ``section``, as in a ``tool`` section
    of a ``pyproject.toml`` file.

    Parameters
    ----------
    fn : string
        The path of the file to load.
    loader : function
        A function to load and parse the configuration file, such as
        ``toml.load()``.
    decoding_error : Exception
        Error raised by the loader for decoding errors.
    section : iterable
        Optional section of the file to load.

    Returns
    -------
    dict
       Dictionary corresponding to the data in the file.

    Raises
    ------
    ElectiveFileDecodingError
        Raises ``ElectiveFileDecodingError`` on any decoding error.

    """
    # Return the loaded data.  Raise or return on any problems.
    try:
        with open(fn, "r") as f:
            contents = loader(f)

    except decoding_error as error:
        raise ElectiveFileDecodingError(message=str(error)) from error

    if section:
        contents = _get_section(contents, section)

    return contents


def _bespon_file_loader(
    fn,
    section=None,
):
    """Load a BespON configuration file.

    Load a BespON configuration file, optionally only returning the
    specified sub-dictionary ``section``, as in a ``tool`` section
    of a ``pyproject.bespon`` file.

    Parameters
    ----------
    fn : string
        The path of the file to load.
    section : string
        Optional section of the file to load.

    Returns
    -------
    dict
       Dictionary corresponding to the data in the file.

    """
    return _file_loader(
        fn,
        bespon.load,
        bespon.erring.DecodingException,
        section=section,
    )


def _json_file_loader(
    fn,
    section=None,
):
    """Load a JSON configuration file.

    Load a JSON configuration file, optionally only returning the
    specified sub-dictionary ``section``, as in a ``tool`` section
    of a ``pyproject.json`` file.

    Parameters
    ----------
    fn : string
        The path of the file to load.
    section : string
        Optional section of the file to load.

    Returns
    -------
    dict
       Dictionary corresponding to the data in the file.


    """
    return _file_loader(
        fn,
        json.load,
        json.JSONDecodeError,
        section=section,
    )


def _toml_file_loader(
    fn,
    section=None,
):
    """Load a TOML configuration file.

    Load a TOML configuration file, optionally only returning the
    specified sub-dictionary ``section``, as in a ``tool`` section
    of a ``pyproject.toml`` file.

    Parameters
    ----------
    fn : string
        The path of the file to load.
    section : string
        Optional section of the file to load.

    Returns
    -------
    dict
       Dictionary corresponding to the data in the file.


    """
    return _file_loader(
        fn,
        toml.load,
        toml.TomlDecodeError,
        section=section,
    )


def _yaml_file_loader(
    fn,
    section=None,
):
    """Load a YAML configuration file.

    Load a YAML configuration file, optionally only returning the
    specified sub-dictionary ``section``, as in a ``tool`` section
    of a ``pyproject.yaml`` file.

    Parameters
    ----------
    fn : string
        The path of the file to load.
    section : string
        Optional section of the file to load.

    Returns
    -------
    dict
       Dictionary corresponding to the data in the file.


    """
    return _file_loader(
        fn,
        YAML(typ="safe").load,
        YAMLError,
        section=section,
    )
