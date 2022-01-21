# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Elective config tests."""

import types

from hypothesis import given
from hypothesis import strategies as st

import elective


def test_elective_config_interface():
    """Should have the correct interface."""
    assert isinstance(elective.ElectiveConfig.__init__, types.FunctionType)
    assert isinstance(elective.ElectiveConfig.__str__, types.FunctionType)
    assert isinstance(elective.ElectiveConfig.__repr__, types.FunctionType)
