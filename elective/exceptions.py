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

"""Elective exceptions."""


class ElectiveFileDecodingError(Exception):
    """File decoding error."""

    def __init__(self, message, *args, **kwargs):
        """Initialize an ``ElectiveFileDecodingError``."""
        super().__init__(*args, **kwargs)
        self.message = message

    def __str__(self):
        """Stringify an ``ElectiveFileDecodingError``."""
        return self.message

    def __repr__(self):
        """Reproduce an ``ElectiveFileDecodingError``."""
        return f"ElectiveFileDecodingError(message={self.message!r},)"
