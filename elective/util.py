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

"""Utility functions."""


def _is_listdict(d):
    """Determine if the keys of a dict are list indices."""
    # All integers?
    keys = []
    for k in d.keys():
        try:
            keys.append(int(k))
        except ValueError:
            return False

    keys = sorted(keys)

    # Zero start?
    if min(keys) != 0:
        return False

    # Consecutive?
    if keys != list(range(0, max(keys) + 1)):
        return False

    return True


def _convert_dict_to_list(d):
    """Convert a list-style dict to a list."""
    keys = sorted(d.keys())
    the_list = []
    for k in keys:
        the_list.append(d[k])

    return the_list


def _flatten_to_list(ds):
    """Convert lists as dicts to lists in a data structure."""
    for k in ds.keys():
        if isinstance(ds[k], dict):
            # If the item points a dict, descend.
            ds[k] = _flatten_to_list(ds[k])
            # We're back.  Now check if the dict is a list-style dict
            # and maybe convert to a list.
            if _is_listdict(ds[k]):
                ds[k] = _convert_dict_to_list(ds[k])

    return ds


def _format_sh(k, v, prefix):
    """Format a configuration value as a Bourne shell environment variable."""
    return f"export {prefix!s}{k!s}='{v!s}'"
