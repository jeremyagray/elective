# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Environment loading utilities."""

import os
import sys

from .config import Configuration


class EnvConfiguration(Configuration):
    """Client program environment variable loader."""

    def __init__(self, *args, **kwargs):
        """Initialize the client environment variable loader."""
        # Pop our arguments.
        self.prefix = kwargs.pop("prefix", "ELECTIVE_")
        self.separator = kwargs.pop("separator", "__")

        # Call the super.
        super().__init__(*args, **kwargs)

    @staticmethod
    def _are_keys_indices(d):
        """Determine if the keys of a dict are list indices."""
        # All integers?
        keys = []
        for k in d.keys():
            try:
                keys.append(int(k))
            except (ValueError):
                return False

        keys = sorted(keys)

        # Zero start?
        if min(keys) != 0:
            return False

        # Consecutive?
        if keys != list(range(0, max(keys) + 1)):
            return False

        return True

    @staticmethod
    def _is_listdict(d):
        """Determine if the keys of a dict are list indices."""
        # All integers?
        keys = []
        for k in d.keys():
            try:
                keys.append(int(k))
            except (ValueError):
                return False

        keys = sorted(keys)

        # Zero start?
        if min(keys) != 0:
            return False

        # Consecutive?
        if keys != list(range(0, max(keys) + 1)):
            return False

        return True

    @staticmethod
    def _convert_dict_to_list(d):
        """Convert a list-style dict to a list."""
        keys = sorted(d.keys())
        the_list = []
        for k in keys:
            the_list.append(d[k])

        return the_list

    @staticmethod
    def _convert_listdict_to_list(ds):
        """Convert lists as dicts to lists in a data structure."""
        for (k, v) in ds.items():
            if isinstance(ds[k], dict):
                # If the item points a dict, descend.
                ds[k] = EnvConfiguration._convert_listdict_to_list(ds[k])
                # We're back.  Now check if the dict is a list-style dict
                # and maybe convert to a list.
                if EnvConfiguration._are_keys_indices(ds[k]):
                    ds[k] = EnvConfiguration._convert_dict_to_list(ds[k])

        return ds

    def load(self):
        """Load configuration variables from the enviroment.

        This function searches the environment for variables prepended
        with ``prefix``.  This function can read boolean, string, and
        number variables directly from the environment and reconstruct
        lists and hashes from properly formatted series of environment
        variables.
        """
        config = {}

        for (key, value) in os.environ.items():
            if key.startswith(self.prefix):
                # Find the prefixed values and strip the prefix.
                if sys.version_info >= (3, 6) and sys.version_info < (3, 9):
                    name = key[len(self.prefix) :]
                else:
                    name = key.removeprefix(self.prefix)

                if "__" not in name:
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
                        except (KeyError):
                            sub_config[k] = {}
                            sub_config = sub_config[k]
                    sub_config[keys[-1]] = value

        self.options = EnvConfiguration._convert_listdict_to_list(config)

    # def dump(self, export=True, shell="sh"):
    def dump(self, *args, **kwargs):
        """Dump configuration as environment variable strings.

        Parameters
        ----------
        export : boolean, default=True
            Prepend each environment variable string with "export ", or
            not.
        shell : string, default="sh"
            Type of shell used.  Currently, only Bourne style shells
            are supported.

        Returns
        -------
        string
            The current configuration as a string setting environment
            variables.
        """
        # Pop our arguments.
        export = kwargs.pop("export", True)
        # sh = kwargs.pop("shell", "sh")

        stack = []
        dumps = []
        if export:
            exp = "export "
        else:
            exp = ""

        # Convert the config dict into a list (stack).
        for (k, v) in self.options.items():
            stack.append((k, v))

        while stack:
            (k, v) = stack.pop(0)
            if isinstance(v, list):
                for (i, sv) in enumerate(v):
                    stack.append((f"{k}__{i}", sv))
            elif isinstance(v, dict):
                for (sk, sv) in v.items():
                    stack.append((f"{k}__{sk}", sv))
            else:
                dumps.append(f"{str(k)}='{str(v)}'")

        return "\n".join(f"{exp}{self.prefix}{line}" for line in dumps)
