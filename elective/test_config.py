# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Elective generic configuration tests."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

import elective


def test_configuration___init__():
    """Should have an empty ``options`` property."""
    conf = elective.Configuration()

    assert conf.options == {}


def test_configuration_load():
    """Should raise ``NotImplementedError``."""
    conf = elective.Configuration()

    with pytest.raises(NotImplementedError):
        conf.load()


def test_configuration_dump():
    """Should raise ``NotImplementedError``."""
    conf = elective.Configuration()

    with pytest.raises(NotImplementedError):
        conf.dump()
