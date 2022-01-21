# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""elective configuration functions."""

from .files import _load_toml_file


def _process_single_option(option):
    """Process a single option."""
    cleaned = {}
    cleaned["type"] = option.get("type", None)
    cleaned["providers"] = option.get("providers", None)
    cleaned["default"] = option.get("default", None)
    cleaned["short"] = option.get("short", None)
    cleaned["long"] = option.get("long", None)
    cleaned["help"] = option.get("help", None)
    cleaned["dest"] = option.get("dest", None)

    return cleaned


def _process_option(option):
    """Process an option."""
    cleaned = None

    if isinstance(option, list):
        if not cleaned:
            cleaned = []
            for item in option.items():
                cleaned.append(_process_single_option(item))
    else:
        cleaned = _process_single_option(option)

    return cleaned


class ElectiveConfig:
    """Elective configuration options and values."""

    def __init__(self):
        """Initialize an ``ElectiveConfig`` object."""
        self.options = {}

    def __str__(self):
        """Stringify an ``ElectiveConfig`` object."""
        pass

    def __repr__(self):
        """Reproduce an ``ElectiveConfig`` object."""
        pass

    def load(self, fn):
        """Load configuration data."""
        options = _load_toml_file(fn, section="elective")

        self.options["description"] = options.get("description", None)
        self.options["prefix"] = options.get("prefix", None)
        self.options["combine"] = options.get("combine", None)
        self.options["order"] = options.get("order", None)

        self.options["options"] = {}
        for (k, v) in options["options"].items():
            self.options["options"][k] = _process_option(v)
