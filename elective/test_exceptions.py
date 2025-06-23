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

"""Elective exception tests."""

import pytest

import elective


def raises(msg):
    """Raise a ``ElectiveFileDecodingError``."""
    raise elective.ElectiveFileDecodingError(msg)


def test_ElectiveFileDecodingError___str__():
    """Should stringify a ``ElectiveFileDecodingError``."""
    with pytest.raises(elective.ElectiveFileDecodingError) as exc:
        raises("I will fail")

    assert str(exc.value) == "I will fail"


def test_ElectiveFileDecodingError___repr__():
    """Should reproduce a ``ElectiveFileDecodingError``."""
    with pytest.raises(elective.ElectiveFileDecodingError) as exc:
        raises("I will fail")

    assert repr(exc.value) == f"ElectiveFileDecodingError(message={'I will fail'!r},)"
