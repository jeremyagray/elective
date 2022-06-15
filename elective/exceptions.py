# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Elective exceptions."""


class ElectiveFileLoadingError(Exception):
    """Exception thrown on file loading."""

    def __init__(self, message, *args, **kwargs):
        """Initialize an ``ElectiveFileLoadingError``."""
        super().__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        """Stringify an ``ElectiveFileLoadingError``."""
        return self.message

    def __repr__(self):
        """Reproduce an ``ElectiveFileLoadingError``."""
        return "ElectiveFileLoadingError(" f"message={repr(self.message)}," ")"
