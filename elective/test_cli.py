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

    with pytest.raises(SystemExit) as error:
        cli.load(argv=["--errors", "3.14"])

    assert error.type == SystemExit
    assert error.value.code == 2
    assert "invalid int value" in capsys.readouterr().err


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

    with pytest.raises(SystemExit) as error:
        cli.load(argv=["-p", "22/7"])

    assert error.type == SystemExit
    assert error.value.code == 2
    assert "invalid float value" in capsys.readouterr().err


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
