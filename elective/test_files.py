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
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

import elective


def test_load_toml_file_no_file():
    """Should handle no file."""
    actual = elective.FileConfiguration._load_file(
        fn="",
        raise_on_error=False,
    )
    expected = {}

    assert actual == expected

    with pytest.raises(elective.ElectiveFileLoadingError):
        elective.FileConfiguration._load_file(
            fn="",
        )


def test_load_toml_file_bad_file(fs):
    """Should handle a bad file."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("TOML sucks")

    actual = elective.FileConfiguration._load_file(
        fn=fn,
        raise_on_error=False,
    )
    expected = {}

    assert actual == expected

    with pytest.raises(elective.ElectiveFileLoadingError):
        elective.FileConfiguration._load_file(fn)


def test_load_toml_file_good_file(fs):
    """Should handle good files."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("[option]\n\ntoml = 'is cool'\n")

    actual = elective.FileConfiguration._load_file(fn)
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

    actual = elective.FileConfiguration._load_file(fn, section="[tool.option]")
    expected = {
        "yaml": "is not cool",
    }

    assert actual == expected


def test_load_json_file_no_file():
    """Should handle no file."""
    actual = elective.FileConfiguration._load_file(
        "",
        loader=json.load,
        decode_exc=json.JSONDecodeError,
        raise_on_error=False,
    )
    expected = {}

    assert actual == expected

    with pytest.raises(elective.ElectiveFileLoadingError):
        elective.FileConfiguration._load_file(
            "",
            loader=json.load,
            decode_exc=json.JSONDecodeError,
        )


def test_load_json_file_bad_file(fs):
    """Should handle a bad file."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("JSON sucks")

    actual = elective.FileConfiguration._load_file(
        fn,
        loader=json.load,
        decode_exc=json.JSONDecodeError,
        raise_on_error=False,
    )
    expected = {}

    assert actual == expected

    with pytest.raises(elective.ElectiveFileLoadingError):
        elective.FileConfiguration._load_file(
            "",
            loader=json.load,
            decode_exc=json.JSONDecodeError,
        )


def test_load_json_file_good_file(fs):
    """Should handle good files."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write('{"option": {\n  "json": "is cool"\n  }\n}\n')

    actual = elective.FileConfiguration._load_file(
        fn,
        loader=json.load,
        decode_exc=json.JSONDecodeError,
    )
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

    actual = elective.FileConfiguration._load_file(
        fn,
        loader=json.load,
        decode_exc=json.JSONDecodeError,
        section="[tool.option]",
    )
    expected = {
        "yaml": "is not cool",
    }

    assert actual == expected


def test_load_bespon_file_no_file():
    """Should handle no file."""
    actual = elective.FileConfiguration._load_file(
        "",
        loader=bespon.load,
        decode_exc=bespon.erring.DecodingException,
        raise_on_error=False,
    )
    expected = {}

    assert actual == expected

    with pytest.raises(elective.ElectiveFileLoadingError):
        elective.FileConfiguration._load_file(
            "",
            loader=bespon.load,
            decode_exc=bespon.erring.DecodingException,
        )


def test_load_bespon_file_bad_file(fs):
    """Should handle a bad file."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    with open(fn, "w") as file:
        file.write("BespON sucks")

    actual = elective.FileConfiguration._load_file(
        fn,
        loader=bespon.load,
        decode_exc=bespon.erring.DecodingException,
        raise_on_error=False,
    )
    expected = {}

    assert actual == expected

    with pytest.raises(elective.ElectiveFileLoadingError):
        elective.FileConfiguration._load_file(
            fn,
            loader=bespon.load,
            decode_exc=bespon.erring.DecodingException,
        )


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

    actual = elective.FileConfiguration._load_file(
        fn,
        loader=bespon.load,
        decode_exc=bespon.erring.DecodingException,
    )
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

    actual = elective.FileConfiguration._load_file(
        fn,
        loader=bespon.load,
        decode_exc=bespon.erring.DecodingException,
        section="[tool.option]",
    )
    expected = {
        "yaml": "is not cool",
    }

    assert actual == expected


def test_load_yaml_file_no_file():
    """Should handle no file."""
    actual = elective.FileConfiguration._load_file(
        "",
        loader=YAML(typ="safe").load,
        decode_exc=YAMLError,
        raise_on_error=False,
    )
    expected = {}

    assert actual == expected

    with pytest.raises(elective.ElectiveFileLoadingError):
        elective.FileConfiguration._load_file(
            "",
            loader=YAML(typ="safe").load,
            decode_exc=YAMLError,
        )


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

    actual = elective.FileConfiguration._load_file(
        fn,
        loader=YAML(typ="safe").load,
        decode_exc=YAMLError,
        raise_on_error=False,
    )
    expected = {}

    assert actual == expected

    with pytest.raises(elective.ElectiveFileLoadingError):
        elective.FileConfiguration._load_file(
            fn,
            loader=YAML(typ="safe").load,
            decode_exc=YAMLError,
        )


def test_load_yaml_file_good_file(fs):
    """Should handle good files."""
    # Need a fake file here.
    fn = "config.txt"
    fs.create_file(fn)
    content = "---\noption:\n  yaml: is cool\n"
    with open(fn, "w") as file:
        file.write(content)

    actual = elective.FileConfiguration._load_file(
        fn,
        loader=YAML(typ="safe").load,
        decode_exc=YAMLError,
    )
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

    actual = elective.FileConfiguration._load_file(
        fn,
        loader=YAML(typ="safe").load,
        decode_exc=YAMLError,
        section="[tool.option]",
    )
    expected = {
        "yaml": "is not cool",
    }

    assert actual == expected


def test_load(fs):
    """Should load a configuration."""
    # Need a fake file here.
    fn = ".client"
    toml_fn = f"{fn}.toml"
    fs.create_file(toml_fn)
    with open(toml_fn, "w") as file:
        file.write("[elective]\n\n[elective.client]\n\nspell-check = true\n")

    json_fn = f"{fn}.json"
    fs.create_file(json_fn)
    with open(json_fn, "w") as file:
        file.write('{"elective": {"client": {"spell-check": true}}}')

    bespon_fn = f"{fn}.bespon"
    fs.create_file(bespon_fn)
    with open(bespon_fn, "w") as file:
        file.write('elective =\n  client =\n    "spell-check" = true\n')

    yaml_fn = f"{fn}.yaml"
    fs.create_file(yaml_fn)
    with open(yaml_fn, "w") as file:
        file.write("---\nelective:\n  client:\n    spell-check: true\n")

    formats = ["toml", "json", "bespon", "yaml"]
    fc = elective.FileConfiguration(
        combine="left",
        order=formats,
    )
    fc.load(
        fn=fn,
        section="elective.client",
    )

    expected = {
        "spell-check": True,
    }

    for format in formats:
        assert format in fc.options.keys()
        assert fc.options[format] == expected
