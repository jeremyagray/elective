# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""elective environment utility tests."""

import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

import elective


def test__load_env_no_env():
    """Should handle no environment."""
    actual = elective.load_env(prefix="ELECTIVE_TEST_")
    expected = {}

    assert actual == expected


@pytest.mark.parametrize(
    "val",
    ("true", "yes", "1"),
)
def test__load_env_boolean_true(val, monkeypatch):
    """Should load a boolean variable from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_CHECK", val)
    monkeypatch.setenv("ELECTIVE_TEST_NO_CHECK", val)

    conf = elective.load_env(prefix="ELECTIVE_TEST_")
    assert elective.process_boolean("check", conf) is True
    assert elective.process_boolean("no_check", conf) is False


@pytest.mark.parametrize(
    "val",
    ("false", "no", "0"),
)
def test__load_env_boolean_false(val, monkeypatch):
    """Should load a boolean variable from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_CHECK", val)
    monkeypatch.setenv("ELECTIVE_TEST_NO_CHECK", val)

    conf = elective.load_env(prefix="ELECTIVE_TEST_")
    assert elective.process_boolean("check", conf) is False
    assert elective.process_boolean("no_check", conf) is True


def test__load_env_bad_boolean(monkeypatch):
    """Should handle bad boolean variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_CHECK", "true")
    monkeypatch.setenv("ELECTIVE_TEST_NO_CHECK", "false")

    conf = elective.load_env(prefix="ELECTIVE_TEST_")

    assert elective.process_boolean("bob", conf) is None


@given(
    str=st.text(alphabet=st.characters(blacklist_categories=("Cc", "Cs"))),
)
def test__load_env_string(str):
    """Should load a boolean variable from the environment."""
    with pytest.MonkeyPatch().context() as mp:
        mp.setenv("ELECTIVE_TEST_FOO", str)
        conf = elective.load_env(prefix="ELECTIVE_TEST_")
        assert elective.process_string("foo", conf) == str


def test__load_env_bad_string(monkeypatch):
    """Should handle bad string variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_FOO", "bar")

    conf = elective.load_env(prefix="ELECTIVE_TEST_")

    assert elective.process_string("bar", conf) is None


@given(
    val=st.integers(),
)
def test__load_env_integer(val):
    """Should load a integer variable from the environment."""
    with pytest.MonkeyPatch().context() as mp:
        mp.setenv("ELECTIVE_TEST_NUM", str(val))
        conf = elective.load_env(prefix="ELECTIVE_TEST_")
        assert elective.process_integer("num", conf) == val


def test__load_env_missing_integer(monkeypatch):
    """Should handle missing integer variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_NUM", "314")

    conf = elective.load_env(prefix="ELECTIVE_TEST_")

    assert elective.process_integer("bar", conf) is None


def test__load_env_non_integer(monkeypatch):
    """Should handle non-integer variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_NUM", "3.14")

    conf = elective.load_env(prefix="ELECTIVE_TEST_")

    assert elective.process_integer("num", conf) is None


@given(
    val=st.floats(),
)
def test__load_env_float(val):
    """Should load a float variable from the environment."""
    with pytest.MonkeyPatch().context() as mp:
        mp.setenv("ELECTIVE_TEST_NUM", str(val))
        conf = elective.load_env(prefix="ELECTIVE_TEST_")
        if math.isnan(val):
            assert math.isnan(elective.process_float("num", conf)) is True
        else:
            assert elective.process_float("num", conf) == val


def test__load_env_missing_float(monkeypatch):
    """Should handle missing integer variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_NUM", "3.14")

    conf = elective.load_env(prefix="ELECTIVE_TEST_")

    assert elective.process_float("bar", conf) is None


def test__load_env_non_float(monkeypatch):
    """Should handle non-float variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_NUM", "bar")

    conf = elective.load_env(prefix="ELECTIVE_TEST_")

    assert elective.process_float("num", conf) is None
