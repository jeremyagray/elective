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

"""File configuration tests."""

import pytest

import elective


def test_load_no_file_return():
    """Should return empty configuration with no file."""
    cf = elective.FileConfiguration(
        "",
        raise_on_file_error=False,
    )
    cf.load()

    actual = cf.options

    expected = {}

    assert actual == expected


def test_load_no_file_raise():
    """Should raise with no file."""
    with pytest.raises(FileNotFoundError):
        cf = elective.FileConfiguration("")
        cf.load()


def test_load_bad_file_return(fs):
    """Should return an empty configuration for a bad file."""
    # Bad fake file.
    fn = "config.txt"
    fs.create_file(fn)

    content = """\
    ---
    :
    """

    with open(fn, "w") as file:
        file.write(content)

    cf = elective.FileConfiguration(fn)
    cf.load()

    actual = cf.options

    expected = {}

    assert actual == expected


def test_load_bad_file_raise(fs):
    """Should raise with a bad file."""
    # Bad fake file.
    fn = "config.txt"
    fs.create_file(fn)

    content = """\
    ---
    :
    """

    with open(fn, "w") as file:
        file.write(content)

    with pytest.raises(elective.ElectiveFileDecodingError):
        cf = elective.FileConfiguration(fn, raise_on_decode_error=True)
        cf.load()


def test_load_good_toml_file(fs):
    """Should return a configuration for a good TOML file."""
    # Good TOML fake file.
    fn = "config.txt"
    fs.create_file(fn)

    content = """[option]

toml = "is cool"
"""

    with open(fn, "w") as file:
        file.write(content)

    cf = elective.FileConfiguration(fn, raise_on_file_error=False)
    cf.load()
    actual = cf.options

    expected = {
        "option": {
            "toml": "is cool",
        },
    }

    assert actual == expected


def test_load_toml_subsection(fs):
    """Should return a subsection of a TOML configuration."""
    # Good TOML fake file.
    fn = "config.txt"
    fs.create_file(fn)

    content = """[option]

toml = "is cool"

[option.section]

number = 1

[option.section.subsection]

number = 2
"""

    with open(fn, "w") as file:
        file.write(content)

    cf = elective.FileConfiguration(
        fn,
        section=(
            "option",
            "section",
            "subsection",
        ),
        raise_on_file_error=False,
    )
    cf.load()
    actual = cf.options

    expected = {
        "number": 2,
    }

    assert actual == expected


def test_load_good_json_file(fs):
    """Should return a configuration for a good JSON file."""
    # Good JSON fake file.
    fn = "config.txt"
    fs.create_file(fn)

    content = """{
  "option": {
    "json": "is cool"
  }
}
"""

    with open(fn, "w") as file:
        file.write(content)

    cf = elective.FileConfiguration(fn, raise_on_file_error=False)
    cf.load()
    actual = cf.options

    expected = {
        "option": {
            "json": "is cool",
        },
    }

    assert actual == expected


def test_load_good_yaml_file(fs):
    """Should return a configuration for a good YAML file."""
    # Good YAML fake file.
    fn = "config.txt"
    fs.create_file(fn)

    content = """
---
option:
  yaml: is cool
"""

    with open(fn, "w") as file:
        file.write(content)

    cf = elective.FileConfiguration(fn, raise_on_file_error=False)
    cf.load()
    actual = cf.options

    expected = {
        "option": {
            "yaml": "is cool",
        },
    }

    assert actual == expected


def test_load_good_bespon_file(fs):
    """Should return a configuration for a good BespON file."""
    # Good BespON fake file.
    fn = "config.txt"
    fs.create_file(fn)

    content = """option =
  bespon = "is cool"
"""

    with open(fn, "w") as file:
        file.write(content)

    cf = elective.FileConfiguration(fn, raise_on_file_error=False)
    cf.loaders = [
        elective._bespon_file_loader,
    ]
    cf.load()
    actual = cf.options

    expected = {
        "option": {
            "bespon": "is cool",
        },
    }

    assert actual == expected
