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

"""Generic configuration support."""


class Configuration:
    """A generic configuration."""

    def __init__(self):
        """Initialize a configuration."""
        self.options = {}

    def load(self):
        """Load a configuration."""
        raise NotImplementedError("Implement this method in your subclass.")

    def dump(self):
        """Dump a configuration."""
        raise NotImplementedError("Implement this method in your subclass.")
