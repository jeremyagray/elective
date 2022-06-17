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


def process_checks(name, conf):
    """Check validity of an environment variable in a configuration dict."""
    key = name.upper()

    try:
        conf[key]
        return key
    except KeyError:
        return None


def process_boolean(name, conf):
    """Process and validate a boolean environment variable."""
    key = process_checks(name, conf)

    if not key:
        return None

    if key.startswith("NO_"):
        if conf[key] == "true" or conf[key] == "yes" or conf[key] == "1":
            return False
        return True

    if conf[key] == "true" or conf[key] == "yes" or conf[key] == "1":
        return True
    return False


def process_string(name, conf):
    """Process and validate a string environment variable."""
    key = process_checks(name, conf)

    if not key:
        return None

    return conf[key]


def process_integer(name, conf):
    """Process and validate an integer environment variable."""
    key = process_checks(name, conf)

    if not key:
        return None

    try:
        return int(conf[key])
    except ValueError:
        return None


def process_float(name, conf):
    """Process and validate a float environment variable."""
    name = process_checks(name, conf)

    if not name:
        return None

    try:
        return float(conf[name])
    except ValueError:
        return None


def process_list(name, conf):
    """Process and validate a list environment variable set.

    Caller is responsible for any type validation of the contents of
    the list.
    """
    key = process_checks(name, conf)

    if not key:
        return None

    data = conf[key]
    if isinstance(data, list):
        return data

    return None


def process_dict(name, conf):
    """Process and validate a dict environment variable.

    Caller is responsible for any type validation of the contents of
    the dict.
    """
    key = process_checks(name, conf)

    if not key:
        return None

    data = conf[key]

    if isinstance(data, dict):
        return data
    else:
        return None


def process_conf(vars, conf):
    """Process and return a configuration dict."""
    filtered = {}

    for (name, kind) in vars:
        if kind == "boolean":
            filtered[name] = process_boolean(conf)
        elif kind == "string":
            filtered[name] = process_string(conf)
        elif kind == "int":
            filtered[name] = process_integer(conf)
        elif kind == "float":
            filtered[name] = process_float(conf)
        # elif kind == "list":
        #     filtered[name] = process_list(name, conf)
        # elif kind == "dict":
        #     filtered[name] = process_dict(name, conf)

    return filtered
