# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""elective generator tests."""

import elective


def test_generate_returns_string():
    """Should return a string."""
    actual = elective.generate()

    assert isinstance(actual, str)


def test__generate_argparse_display_action_returns_correct_parser():
    """Should return a good parser."""
    name = "warranty"
    message = "There is no spoon."

    actual = elective._generate_argparse_display_action(
        name=name,
        message=message,
    )

    assert name in actual["blocks"][0]
    assert name in actual["classes"][0]


def test__generate_file_banner_default():
    """Should return the default banner."""
    actual = elective._generate_file_banner()["blocks"][0]
    expected = '"""Configuration module generated by elective."""'

    assert actual == expected


def test__generate_file_banner_custom():
    """Should return a custom banner."""
    message = "This is a message."
    actual = elective._generate_file_banner(message=message)["blocks"][0]
    expected = f'"""{message}"""'

    assert actual == expected


def test__generate_argparse_parser():
    """Should return an argument parser."""
    description = "This is a description."
    actual = elective._generate_argparse_parser(
        description=description,
    )

    assert actual["dependencies"][0] == "import argparse"
    assert description in actual["blocks"][0]


def test__generate_argparse_boolean():
    """Generate an ``argparse`` boolean argument."""
    group = "parser"
    short = "c"
    long = "spell-check"
    dest = "spell_check"
    action = "store_true"
    help = "Spell check the commit.  Default is no spell checking."

    actual = elective._generate_argparse_boolean(
        group=group,
        short=short,
        long=long,
        dest=dest,
        default=None,
        action=action,
        help=help,
    )

    assert actual["dependencies"][0] == "import argparse"

    assert group in actual["blocks"][0]
    assert group in actual["blocks"][0]
    assert f"-{short}" in actual["blocks"][0]
    assert f"--{long}" in actual["blocks"][0]
    assert dest in actual["blocks"][0]
    assert action in actual["blocks"][0]
    assert help in actual["blocks"][0]


def test__generate_argparse_boolean_group():
    """Generate an ``argparse`` boolean argument group."""
    short = "c"
    long = "spell-check"
    dest = "spell_check"
    help = "Spell check the commit.  Default is no spell checking."

    actual = elective._generate_argparse_boolean_group(
        short=short,
        long=long,
        dest=dest,
        default=None,
        help=help,
    )

    assert actual["dependencies"][0] == "import argparse"

    code = "\n".join(actual["blocks"])

    assert f"-{short}" in code
    assert f"-{short.upper()}" in code
    assert f"--{long}" in code
    assert f"--no-{long}" in code
    assert dest in code
    assert "store_true" in code
    assert "store_false" in code
    assert help in code


def test__generate_loader():
    """Generate the loader."""
    actual = elective._generate_loader()
    expected = """\
def load(argv=None):
    \"\"\"Load the configuration.\"\"\"
    args = _create_argument_parser().parse_args(argv)

    return args
"""
    assert actual["blocks"][0] == expected
