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

import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

import elective


def test_state___init___empty():
    """Should initialize an empty ``State``."""
    state = elective.State()

    assert state._current is None
    assert state.current is None
    assert state.values == []
    assert state.sources == []


@given(
    value=st.text(alphabet=st.characters()),
    source=st.text(alphabet=st.characters()),
)
def test_state___init___inital_string(value, source):
    """Should initialize a ``State`` with an initial string value."""
    state = elective.State((value, source))

    assert state._current == value
    assert state.current == value
    assert state.values == [value]
    assert state.sources == [source]


@given(
    value=st.integers(min_value=50, max_value=50),
    source=st.text(alphabet=st.characters()),
)
def test_state___init___inital_int(value, source):
    """Should initialize a ``State`` with an initial integer value."""
    state = elective.State((value, source))

    assert state._current == value
    assert state.current == value
    assert state.values == [value]
    assert state.sources == [source]


@given(
    value=st.floats(),
    source=st.text(alphabet=st.characters()),
)
def test_state___init___inital_float(value, source):
    """Should initialize a ``State`` with an initial float value."""
    state = elective.State((value, source))

    if math.isnan(value):
        assert math.isnan(state._current)
        assert math.isnan(state.current)
        assert math.isnan(state.values[0])
    else:
        assert state._current == value
        assert state.current == value
        assert state.values == [value]

    assert state.sources == [source]


@given(
    value=st.booleans(),
    source=st.text(alphabet=st.characters()),
)
def test_state___init___inital_bool(value, source):
    """Should initialize a ``State`` with an initial bool value."""
    state = elective.State((value, source))

    assert state._current == value
    assert state.current == value
    assert state.values == [value]
    assert state.sources == [source]


@given(
    v1=st.text(alphabet=st.characters()),
    s1=st.text(alphabet=st.characters()),
    v2=st.text(alphabet=st.characters()),
    s2=st.text(alphabet=st.characters()),
)
def test_state___eq___equal(v1, s1, v2, s2):
    """Should be equal."""
    left = elective.State()
    left.set(v1, s1)
    left.set(v2, s2)
    right = elective.State()
    right.set(v1, s1)
    right.set(v2, s2)

    assert left == right
    assert right == left


@given(
    args=st.lists(
        st.text(alphabet=st.characters()),
        min_size=4,
        max_size=4,
        unique=True,
    ),
)
def test_state___eq___unequal_values(args):
    """Should be unequal."""
    left = elective.State()
    left.set(args[0], args[1])
    left.set(args[0], args[1])
    right = elective.State()
    right.set(args[2], args[3])
    right.set(args[2], args[3])

    assert left != right
    assert right != left


@given(
    args=st.lists(
        st.text(alphabet=st.characters()),
        min_size=4,
        max_size=4,
        unique=True,
    ),
)
def test_state___eq___unequal_lengths(args):
    """Should be unequal."""
    left = elective.State()
    left.set(args[0], args[1])
    left.set(args[0], args[1])
    right = elective.State()
    right.set(args[2], args[3])

    assert left != right
    assert right != left


@given(
    args=st.lists(
        st.text(alphabet=st.characters()),
        min_size=4,
        max_size=4,
        unique=True,
    ),
)
def test_state___eq___unequal_empty(args):
    """Should be unequal."""
    left = elective.State()
    left.set(args[0], args[1])
    left.set(args[0], args[1])
    right = elective.State()

    assert left != right
    assert right != left
