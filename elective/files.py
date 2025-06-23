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

"""File loading utilities."""

from .config import Configuration
from .exceptions import ElectiveFileDecodingError
from .util import (
    _bespon_file_loader,
    _json_file_loader,
    _toml_file_loader,
    _yaml_file_loader,
)


class FileConfiguration(Configuration):
    """File configuration loader."""

    def __init__(
        self, fn, section=None, raise_on_decode_error=False, raise_on_file_error=True
    ):
        """Initialize a file configuration."""
        self.fn = fn
        self.section = section
        self.raise_on_decode_error = raise_on_decode_error
        self.raise_on_file_error = raise_on_file_error

        self.loaders = [
            _toml_file_loader,
            _yaml_file_loader,
            _json_file_loader,
            _bespon_file_loader,
        ]

    def load(self):
        """Load configuration file."""
        for loader in self.loaders:
            try:
                self.options = loader(
                    self.fn,
                    section=self.section,
                )

                return

            except ElectiveFileDecodingError:
                pass

            except FileNotFoundError:
                if self.raise_on_file_error:
                    raise

                self.options = {}
                return

        self.options = {}

        if self.raise_on_decode_error:
            raise ElectiveFileDecodingError(message=f"{self.fn} could not be decoded.")
