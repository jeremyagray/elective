# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""elective file utility tests."""

import pytest
import toml

import elective


def test__load_toml_file_no_file():
    """Should handle no file."""
    actual = elective._load_toml_file("", raise_on_error=False)
    expected = {}

    assert actual == expected

    with pytest.raises(FileNotFoundError):
        elective._load_toml_file("")


def test__load_toml_file_bad_file(fs):
    """Should handle a bad file."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("TOML sucks")

    actual = elective._load_toml_file(fn, raise_on_error=False)
    expected = {}

    assert actual == expected

    with pytest.raises(toml.TomlDecodeError):
        elective._load_toml_file(fn)


def test__load_toml_file_good_file(fs):
    """Should handle good files."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("[option]\n\ntoml = 'is cool'\n")

    actual = elective._load_toml_file(fn)
    expected = {
        "option": {
            "toml": "is cool",
        },
    }

    assert actual == expected

    fn = "config2.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write(
            """\
[option]

toml = 'is cool'

[tool]

[tool.option]

yaml = 'is not cool'
"""
        )

    actual = elective._load_toml_file(fn, section="[tool.option]")
    expected = {
        "yaml": "is not cool",
    }

    assert actual == expected
