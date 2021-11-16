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

# from elective import generate
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
