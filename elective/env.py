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

"""Environment loading utilities."""

import os

from .config import Configuration
from .util import _flatten_to_list, _format_sh


class EnvConfiguration(Configuration):
    """Client program environment variable loader."""

    def __init__(self, *args, **kwargs):
        """Initialize the client environment variable loader."""
        # Defaults.
        self.prefix = kwargs.pop("prefix", "ELECTIVE_")
        self.separator = kwargs.pop("separator", "__")

        # Call the super.
        super().__init__(*args, **kwargs)

    def load(self):
        """Load configuration variables from the enviroment.

        This function searches the environment for variables prepended
        with ``prefix``.  This function can read boolean, string, and
        number variables directly from the environment and reconstruct
        lists and hashes from properly formatted series of environment
        variables.
        """
        config = {}

        for key, value in os.environ.items():
            if key.startswith(self.prefix):
                # Find the prefixed values and strip the prefix.
                name = key.removeprefix(self.prefix)

                if self.separator not in name:
                    # Find the non-dict and non-list pairs and add them to
                    # the dict.
                    config[name] = value
                else:
                    # Handle the flattened data structures, treating the
                    # list type variables as dicts.
                    # Based on:
                    # https://gist.github.com/fmder/494aaa2dd6f8c428cede
                    keys = name.split(self.separator)
                    sub_config = config
                    for k in keys[:-1]:
                        try:
                            if not isinstance(sub_config[k], dict):
                                raise Exception(
                                    f"{k} is defined multiple times in the environment."
                                )
                            sub_config = sub_config[k]
                        except KeyError:
                            sub_config[k] = {}
                            sub_config = sub_config[k]
                    sub_config[keys[-1]] = value

        self.options = _flatten_to_list(config)

    def dump(self, formatter=_format_sh):
        """Dump configuration as environment variable strings.

        Parameters
        ----------
        formatter : function, default=_format_sh
            Formatting function that accepts a key, value, and prefix
            as its arguments and returns a string that can set a
            variable in a shell.

        Returns
        -------
        string
            The current configuration as a string setting environment
            variables.

        """
        stack = []
        dumps = []

        # Convert the config dict into a list (stack).
        for k, v in self.options.items():
            stack.append((k, v))

        while stack:
            (k, v) = stack.pop(0)
            if isinstance(v, list):
                for i, sv in enumerate(v):
                    stack.append((f"{k}{self.separator}{i}", sv))
            elif isinstance(v, dict):
                for sk, sv in v.items():
                    stack.append((f"{k}{self.separator}{sk}", sv))
            else:
                dumps.append(formatter(k, v, prefix=self.prefix))

        return "\n".join(line for line in dumps)
