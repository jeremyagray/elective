# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Generic configuration support."""


class Configuration:
    """A generic configuration."""

    def __init__(self, *args, **kwargs):
        """Initialize a configuration."""
        self.options = {}

    def load(self, *args, **kwargs):
        """Load a configuration."""
        raise NotImplementedError("Implement this method in your subclass.")

    def dump(self, *args, **kwargs):
        """Dump a configuration."""
        raise NotImplementedError("Implement this method in your subclass.")
