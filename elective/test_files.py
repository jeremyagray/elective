# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""elective file utility tests."""

import json

import bespon
import pytest
import toml
from ruamel.yaml.error import YAMLError

import elective


def test_load_toml_file_no_file():
    """Should handle no file."""
    actual = elective.load_toml_file("", raise_on_error=False)
    expected = {}

    assert actual == expected

    with pytest.raises(FileNotFoundError):
        elective.load_toml_file("")


def test_load_toml_file_bad_file(fs):
    """Should handle a bad file."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("TOML sucks")

    actual = elective.load_toml_file(fn, raise_on_error=False)
    expected = {}

    assert actual == expected

    with pytest.raises(toml.TomlDecodeError):
        elective.load_toml_file(fn)


def test_load_toml_file_good_file(fs):
    """Should handle good files."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("[option]\n\ntoml = 'is cool'\n")

    actual = elective.load_toml_file(fn)
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

    actual = elective.load_toml_file(fn, section="[tool.option]")
    expected = {
        "yaml": "is not cool",
    }

    assert actual == expected


def test_load_json_file_no_file():
    """Should handle no file."""
    actual = elective.load_json_file("", raise_on_error=False)
    expected = {}

    assert actual == expected

    with pytest.raises(FileNotFoundError):
        elective.load_json_file("")


def test_load_json_file_bad_file(fs):
    """Should handle a bad file."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("JSON sucks")

    actual = elective.load_json_file(fn, raise_on_error=False)
    expected = {}

    assert actual == expected

    with pytest.raises(json.JSONDecodeError):
        elective.load_json_file(fn)


def test_load_json_file_good_file(fs):
    """Should handle good files."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write('{"option": {\n  "json": "is cool"\n  }\n}\n')

    actual = elective.load_json_file(fn)
    expected = {
        "option": {
            "json": "is cool",
        },
    }

    assert actual == expected

    fn = "config2.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write(
            """\
{
  "option": {
    "json": "is cool"
  },
  "tool": {
    "option": {
      "yaml": "is not cool"
    }
  }
}
"""
        )

    actual = elective.load_json_file(fn, section="[tool.option]")
    expected = {
        "yaml": "is not cool",
    }

    assert actual == expected


def test_load_bespon_file_no_file():
    """Should handle no file."""
    actual = elective.load_bespon_file("", raise_on_error=False)
    expected = {}

    assert actual == expected

    with pytest.raises(FileNotFoundError):
        elective.load_bespon_file("")


def test_load_bespon_file_bad_file(fs):
    """Should handle a bad file."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("BespON sucks")

    actual = elective.load_bespon_file(fn, raise_on_error=False)
    expected = {}

    assert actual == expected

    with pytest.raises(bespon.erring.DecodingException):
        elective.load_bespon_file(fn)


def test_load_bespon_file_good_file(fs):
    """Should handle good files."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    content = r"""option =
      bespon = "is cool"
    """
    with open(fn, "w") as file:
        file.write(content)

    actual = elective.load_bespon_file(fn)
    expected = {
        "option": {
            "bespon": "is cool",
        },
    }

    assert actual == expected

    fn = "config2.txt"
    fs.create_file(fn)

    content = """\
    option =
      bespon = "is cool"
    tool =
      option =
        yaml = "is not cool"
    """

    with open(fn, "w") as file:
        file.write(content)

    actual = elective.load_bespon_file(fn, section="[tool.option]")
    expected = {
        "yaml": "is not cool",
    }

    assert actual == expected


def test_load_yaml_file_no_file():
    """Should handle no file."""
    actual = elective.load_yaml_file("", raise_on_error=False)
    expected = {}

    assert actual == expected

    with pytest.raises(FileNotFoundError):
        elective.load_yaml_file("")


def test_load_yaml_file_bad_file(fs):
    """Should handle a bad file."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)

    content = """\
    ---
    :
    """

    with open(fn, "w") as file:
        file.write(content)

    actual = elective.load_yaml_file(fn, raise_on_error=False)
    expected = {}

    assert actual == expected

    with pytest.raises(YAMLError):
        elective.load_yaml_file(fn)


def test_load_yaml_file_good_file(fs):
    """Should handle good files."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    content = "---\noption:\n  yaml: is cool\n"
    with open(fn, "w") as file:
        file.write(content)

    actual = elective.load_yaml_file(fn)
    expected = {
        "option": {
            "yaml": "is cool",
        },
    }

    assert actual == expected

    fn = "config2.txt"
    fs.create_file(fn)

    content = "---\noption:\n  yaml: is cool\ntool:\n  option:\n    yaml: is not cool\n"

    with open(fn, "w") as file:
        file.write(content)

    actual = elective.load_yaml_file(fn, section="[tool.option]")
    expected = {
        "yaml": "is not cool",
    }

    assert actual == expected
