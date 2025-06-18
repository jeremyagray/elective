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

"""Environment configuration tests."""

# import math
# import sys

# import pytest
# from hypothesis import given
# from hypothesis import strategies as st

import elective


def test__is_listdict_detects_list():
    """Should detect a list."""
    ds = {
        "0": "apple",
        "1": "banana",
        "2": "orange",
    }

    assert elective._is_listdict(ds) is True


def test__is_listdict_noninteger_indices():
    """Should detect a non-integer indices."""
    ds = {
        "zero": "apple",
        "1": "banana",
        "2": "orange",
    }

    assert elective._is_listdict(ds) is False
    ds = {
        "0": "apple",
        "one": "banana",
        "2": "orange",
    }

    assert elective._is_listdict(ds) is False
    ds = {
        "0": "apple",
        "1": "banana",
        "two": "orange",
    }

    assert elective._is_listdict(ds) is False


def test__is_listdict_nonzero_start():
    """Should detect a non-zero starting index."""
    ds = {
        "3": "apple",
        "1": "banana",
        "2": "orange",
    }

    assert elective._is_listdict(ds) is False

    ds = {
        "1": "banana",
        "2": "orange",
        "3": "apple",
    }

    assert elective._is_listdict(ds) is False

    ds = {
        "3": "apple",
        "2": "orange",
        "1": "banana",
    }

    assert elective._is_listdict(ds) is False


def test__is_listdict_nonsequential_indices():
    """Should detect a non-sequential indices."""
    ds = {
        "0": "apple",
        "2": "banana",
        "3": "orange",
    }

    assert elective._is_listdict(ds) is False

    ds = {
        "2": "banana",
        "0": "apple",
        "3": "orange",
    }

    assert elective._is_listdict(ds) is False


def test__convert_dict_to_list():
    """Should convert dict to list."""
    listdict = {
        "0": "apple",
        "1": "banana",
        "2": "orange",
    }

    actual = elective._convert_dict_to_list(listdict)

    expected = [
        "apple",
        "banana",
        "orange",
    ]

    assert actual == expected

    listdict = {
        "1": "banana",
        "0": "apple",
        "2": "orange",
    }

    actual = elective._convert_dict_to_list(listdict)

    assert actual == expected

    listdict = {
        "2": "orange",
        "1": "banana",
        "0": "apple",
    }

    actual = elective._convert_dict_to_list(listdict)

    assert actual == expected


def test__flatten_to_list_listdict():
    """Should flatten a list-style dict to a list."""
    ds = {
        "fruit": {
            "0": "apple",
            "1": "banana",
            "2": "orange",
        },
    }

    actual = elective._flatten_to_list(ds)

    expected = {
        "fruit": [
            "apple",
            "banana",
            "orange",
        ],
    }

    assert actual == expected


def test__flatten_to_list_dict():
    """Should not change a regular dict."""
    ds = {
        "fruit": {
            "zero": "apple",
            "one": "banana",
            "two": "orange",
        },
    }

    actual = elective._flatten_to_list(ds)

    expected = ds

    assert actual == expected


def test__flatten_to_list_nested_lists():
    """Should convert listdict to list."""
    ds = {
        "fruit": {
            "0": {
                "apples": {
                    "0": "red",
                    "1": "yellow",
                    "2": "green",
                },
            },
            "1": "banana",
            "2": "orange",
        },
    }

    actual = elective._flatten_to_list(ds)

    expected = {
        "fruit": [
            {
                "apples": [
                    "red",
                    "yellow",
                    "green",
                ],
            },
            "banana",
            "orange",
        ],
    }

    assert actual == expected


def test__format_sh_formats_strings():
    """Should format string values."""
    prefix = "ELECTIVE_"
    actual = elective._format_sh("TEST", "yay", prefix)

    expected = "export ELECTIVE_TEST='yay'"

    assert actual == expected
