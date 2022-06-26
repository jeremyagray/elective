# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Elective exception tests."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

import elective


def raises(msg):
    """Raise a ``ElectiveFileLoadingError``."""
    raise elective.ElectiveFileLoadingError(msg)


def test_ElectiveFileLoadingError___str__():
    """Should stringify a ``ElectiveFileLoadingError``."""
    with pytest.raises(elective.ElectiveFileLoadingError) as exc:
        raises("I will fail")

    assert str(exc.value) == "I will fail"


def test_ElectiveFileLoadingError___repr__():
    """Should reproduce a ``ElectiveFileLoadingError``."""
    with pytest.raises(elective.ElectiveFileLoadingError) as exc:
        raises("I will fail")

    assert (
        repr(exc.value) == f"ElectiveFileLoadingError(message={repr('I will fail')},)"
    )
