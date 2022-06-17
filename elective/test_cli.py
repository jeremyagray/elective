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

import pytest
from hypothesis import given
from hypothesis import strategies as st

import elective


@given(
    desc=st.text(alphabet=st.characters()),
)
def test_client_parser_set_description(desc):
    """Should set the description."""
    parser = elective.CliConfiguration()
    assert parser.parser.description is None

    parser.set_description(desc)
    assert parser.parser.description == desc
