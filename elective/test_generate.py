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

from elective import generate


def test_generate_returns_string():
    """elective.generate() should return a string."""
    actual = generate()

    assert isinstance(actual, str)
