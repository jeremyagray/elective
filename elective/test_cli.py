# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Elective CLI tests."""

import sys

import pytest
from hypothesis import given
from hypothesis import strategies as st

import elective


def test_reset_parser():
    """Should reset parser."""
    # Load CLI options.
    description = "This is a description."
    options = {}
    options["spell-check"] = {
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "type": "boolean",
        "default": False,
        "action": "store_true",
        "short": "c",
        "long": "spell-check",
        "help": "Spell check.  Default is no spell checking.",
    }

    cli = elective.CliConfiguration(
        description=description,
        options=options,
    )
    cli.config()

    assert cli.parser.description == description
    cli.reset_parser()
    assert cli.parser.description is None


def test_bad_option(capsys):
    """Should raise and bail on a bad option."""
    # Load CLI options.
    description = "This is a description."
    options = {}
    options["spell-check"] = {
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "type": "boolean_group",
        "default": False,
        "dest": "spell-check",
        "short_pos": "c",
        "short_neg": "C",
        "long_pos": "spell-check",
        "long_neg": "no-spell-check",
        "help": "Spell check.  Default is no spell checking.",
    }

    cli = elective.CliConfiguration(
        description=description,
        options=options,
    )
    cli.config()

    with pytest.raises(SystemExit) as error:
        cli.load(argv=["-d"])

    assert error.type == SystemExit
    assert error.value.code == 2
    assert "unrecognized arguments" in capsys.readouterr().err


def test_boolean_option():
    """Should load a boolean option."""
    # Load CLI options.
    description = "This is a description."
    options = {}
    options["spell-check"] = {
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "type": "boolean",
        "default": False,
        "action": "store_true",
        "short": "c",
        "long": "spell-check",
        "help": "Spell check.  Default is no spell checking.",
    }

    cli = elective.CliConfiguration(
        description=description,
        options=options,
    )
    cli.config()

    cli.load(argv=["-c"])

    expected = {
        "spell-check": True,
    }

    assert cli.options == expected

    cli.load(argv=["--spell-check"])
    assert cli.options == expected

    cli.load(argv=[])

    expected = {
        "spell-check": False,
    }

    assert cli.options == expected


def test_int_option(capsys):
    """Should load an integer option."""
    # Load CLI options.
    description = "This is a description."
    options = {}
    options["errors"] = {
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "type": "int",
        "default": 0,
        "short": "e",
        "long": "errors",
        "help": "Errors allowed.  Default is 0.",
    }

    cli = elective.CliConfiguration(
        description=description,
        options=options,
    )
    cli.config()

    cli.load(argv=["-e", "5"])

    expected = {
        "errors": 5,
    }

    assert cli.options == expected

    cli.load(argv=["--errors", "5"])
    assert cli.options == expected

    cli.load(argv=[])

    expected = {
        "errors": 0,
    }

    assert cli.options == expected

    # Non-integer.
    with pytest.raises(SystemExit) as error:
        cli.load(argv=["--errors", "3.14"])

    assert error.type == SystemExit
    assert error.value.code == 2
    assert "invalid int value" in capsys.readouterr().err

    # No argument.
    with pytest.raises(SystemExit) as error:
        cli.load(argv=["-e"])

    assert error.type == SystemExit
    assert error.value.code == 2
    assert "expected one argument" in capsys.readouterr().err


def test_float_option(capsys):
    """Should load a float option."""
    # Load CLI options.
    description = "This is a description."
    options = {}
    options["pi"] = {
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "type": "float",
        "default": 3.0,
        "short": "p",
        "long": "pi",
        "help": "The value of pi.  Default is 3.0.",
    }

    cli = elective.CliConfiguration(
        description=description,
        options=options,
    )
    cli.config()

    cli.load(argv=["-p", "3.14"])

    expected = {
        "pi": 3.14,
    }

    assert cli.options == expected

    cli.load(argv=["--pi", "3.14"])
    assert cli.options == expected

    cli.load(argv=[])

    expected = {
        "pi": 3.0,
    }

    assert cli.options == expected

    # Non-float.
    with pytest.raises(SystemExit) as error:
        cli.load(argv=["-p", "22/7"])

    assert error.type == SystemExit
    assert error.value.code == 2
    assert "invalid float value" in capsys.readouterr().err

    # No argument.
    with pytest.raises(SystemExit) as error:
        cli.load(argv=["-p"])

    assert error.type == SystemExit
    assert error.value.code == 2
    assert "expected one argument" in capsys.readouterr().err


def test_string_option(capsys):
    """Should load a string option."""
    # Load CLI options.
    description = "This is a description."
    options = {}
    options["message"] = {
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "type": "str",
        "default": "This is a message.",
        "short": "m",
        "long": "message",
        "help": "A message.  Default is 'This is a message.'.",
    }

    cli = elective.CliConfiguration(
        description=description,
        options=options,
    )
    cli.config()

    cli.load(argv=["-m", "Another message."])

    expected = {
        "message": "Another message.",
    }

    assert cli.options == expected

    cli.load(argv=["--message", "Another message."])
    assert cli.options == expected

    cli.load(argv=[])

    expected = {
        "message": "This is a message.",
    }

    assert cli.options == expected

    # No message.
    with pytest.raises(SystemExit) as error:
        cli.load(argv=["-m"])

    assert error.type == SystemExit
    assert error.value.code == 2
    assert "expected one argument" in capsys.readouterr().err


def test_list_option(capsys):
    """Should load a list option."""
    # Load CLI options.
    description = "This is a description."
    options = {}
    options["list"] = {
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "type": "list",
        "default": ["one"],
        "short": "l",
        "long": "list",
        "help": "A list.  Default is ``['one']``.",
    }

    cli = elective.CliConfiguration(
        description=description,
        options=options,
    )
    cli.config()

    # No items.
    cli.load(argv=["-l", ""])

    expected = {
        "list": [],
    }

    assert cli.options == expected

    cli.load(argv=["--list", ""])
    assert cli.options == expected

    # One item.
    cli.load(argv=["-l", "two"])

    expected = {
        "list": ["two"],
    }

    assert cli.options == expected

    cli.load(argv=["--list", "two"])
    assert cli.options == expected

    # Multiple items.
    cli.load(argv=["-l", "two,three,four"])

    expected = {
        "list": ["two", "three", "four"],
    }

    assert cli.options == expected

    cli.load(argv=["--list", "two,three,four"])
    assert cli.options == expected

    # No list.
    with pytest.raises(SystemExit) as error:
        cli.load(argv=["-l"])

    assert error.type == SystemExit
    assert error.value.code == 2
    assert "expected one argument" in capsys.readouterr().err


def test_boolean_group_option():
    """Should load a boolean group option."""
    # Load CLI options.
    description = "This is a description."
    options = {}
    options["spell-check"] = {
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "type": "boolean_group",
        "default": False,
        "dest": "spell-check",
        "short_pos": "c",
        "short_neg": "C",
        "long_pos": "spell-check",
        "long_neg": "no-spell-check",
        "help": "Spell check.  Default is no spell checking.",
    }

    cli = elective.CliConfiguration(
        description=description,
        options=options,
    )
    cli.config()

    cli.load(argv=["-c"])

    expected = {
        "spell-check": True,
    }

    assert cli.options == expected

    cli.load(argv=["-C"])

    expected = {
        "spell-check": False,
    }

    assert cli.options == expected

    cli.load(argv=["--spell-check"])

    expected = {
        "spell-check": True,
    }

    assert cli.options == expected

    cli.load(argv=["--no-spell-check"])

    expected = {
        "spell-check": False,
    }

    assert cli.options == expected


def test_display_option(fs, capsys):
    """Should display a message."""
    # Load CLI options.
    description = "This is a description."
    license = "This is my license."
    options = {}
    options["show-license"] = {
        "providers": [
            "cli",
        ],
        "type": "display",
        "default": "This is my license.",
        "help": "Show license.",
    }

    cli = elective.CliConfiguration(
        description=description,
        options=options,
    )
    cli.config()

    with pytest.raises(SystemExit) as error:
        cli.load(argv=["--show-license"])

    assert error.type == SystemExit
    assert error.value.code == 0
    assert license in capsys.readouterr().out
