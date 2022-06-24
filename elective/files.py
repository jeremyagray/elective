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

from .config import Configuration
from .exceptions import ElectiveFileLoadingError


class FileConfiguration(Configuration):
    """File configuration loader for the client program."""

    def __init__(self, *args, **kwargs):
        """Initialize a client argument parser."""
        formats = [
            "toml",
            "json",
            "yaml",
            "bespon",
        ]

        self.formats = []
        order = kwargs.pop("order", [])
        for format in formats:
            if format in order:
                self.formats.append(format)

        # Call the super.
        super().__init__(*args, **kwargs)

    @staticmethod
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
           Dictionary corresponding to the data in the file.

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

        except (decode_exc, FileNotFoundError) as error:
            if raise_on_error:
                raise ElectiveFileLoadingError(str(error))
            else:
                return {}

    def load(self, *args, **kwargs):
        """Load file configuration."""
        loaders = {
            "toml": {
                "loader": toml.load,
                "exc": toml.TomlDecodeError,
            },
            "json": {
                "loader": json.load,
                "exc": json.JSONDecodeError,
            },
            "yaml": {
                "loader": YAML(typ="safe").load,
                "exc": YAMLError,
            },
            "bespon": {
                "loader": bespon.load,
                "exc": bespon.erring.DecodingException,
            },
        }

        fn = f"{kwargs.pop('fn')}"
        section = kwargs.pop("section", None)
        raise_on_error = kwargs.pop("raise_on_error", True)

        for format in self.formats:
            self.options[format] = FileConfiguration._load_file(
                f"{fn}.{format}",
                loader=loaders[format]["loader"],
                decode_exc=loaders[format]["exc"],
                section=section,
                raise_on_error=raise_on_error,
            )
