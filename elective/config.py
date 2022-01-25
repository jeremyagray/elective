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
    cleaned["short_pos"] = option.get("short_pos", None)
    cleaned["long_pos"] = option.get("long_pos", None)
    cleaned["short_neg"] = option.get("short_neg", None)
    cleaned["long_neg"] = option.get("long_neg", None)
    cleaned["help"] = option.get("help", None)
    cleaned["dest"] = option.get("dest", None)

    return cleaned


def _process_option(option):
    """Process an option."""
    cleaned = None

    if isinstance(option, list):
        if not cleaned:
            cleaned = []
            for item in option:
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

        # String.
        self.options["description"] = options.get("description", None)
        # String.
        self.options["prefix"] = options.get("prefix", None)

        # String enum.
        combine = options.get("combine", None)
        combine_options = ("left_merge", "right_merge", "join", None)

        if combine not in combine_options:
            raise ValueError(
                f"configured value for `combine` ({combine})"
                f" is not one of {combine_options}"
            )

        self.options["combine"] = options.get("combine", None)

        # String iterable.
        self.options["order"] = options.get("order", None)

        # Option objects.
        if "options" in options:
            self.options["options"] = {}
            for (k, v) in options["options"].items():
                self.options["options"][k] = _process_option(v)
