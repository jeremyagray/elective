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

from pathlib import Path

import toml


def _load_toml_file(fn, section=None, raise_on_error=True):
    """Load a TOML file.

    Load a TOML file, optionally only returning the provided section,
    as in a ``tool`` section of a ``pyproject.toml`` file.

    Parameters
    ----------
    fn : string
        TOML file to load.
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
    TomlDecodeError
        Raised if there are problems decoding a TOML configuration
        file.
    FileNotFoundError
        Raised if the configuration file does not exist or is not
        readable.
    """
    # Check if ``fn`` is a file.  Raise or return if not.
    if not Path(fn).is_file():
        if raise_on_error:
            raise FileNotFoundError
        else:
            return {}

    # Return the loaded data.  Raise or return on any problems.
    try:
        with open(fn, "r") as f:
            contents = toml.load(f)

            if section:
                for k in section.lstrip("[").rstrip("]").split("."):
                    contents = contents[k]
                return contents
            else:
                return contents

    except (toml.TomlDecodeError, FileNotFoundError) as error:
        if raise_on_error:
            raise error
        else:
            return {}
