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
from elective import EnvConfiguration


def test_load_no_env():
    """Should handle no environment."""
    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    actual = env.options
    expected = {}

    assert actual == expected


@pytest.mark.parametrize(
    "val",
    ("true", "yes", "1"),
)
def test_load_env_boolean_true(val, monkeypatch):
    """Should load a boolean variable from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_CHECK", val)
    monkeypatch.setenv("ELECTIVE_TEST_NO_CHECK", val)

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_boolean("check", env.options) is True
    assert elective.process_boolean("no_check", env.options) is False


@pytest.mark.parametrize(
    "val",
    ("false", "no", "0"),
)
def test__load_env_boolean_false(val, monkeypatch):
    """Should load a boolean variable from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_CHECK", val)
    monkeypatch.setenv("ELECTIVE_TEST_NO_CHECK", val)

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_boolean("check", env.options) is False
    assert elective.process_boolean("no_check", env.options) is True


def test_load_env_bad_boolean(monkeypatch):
    """Should handle bad boolean variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_CHECK", "true")
    monkeypatch.setenv("ELECTIVE_TEST_NO_CHECK", "false")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_boolean("bob", env.options) is None


@given(
    str=st.text(alphabet=st.characters(blacklist_categories=("Cc", "Cs"))),
)
def test_load_env_string(str):
    """Should load a string variable from the environment."""
    with pytest.MonkeyPatch().context() as mp:
        mp.setenv("ELECTIVE_TEST_FOO", str)

        env = EnvConfiguration(prefix="ELECTIVE_TEST_")
        env.load()

        assert elective.process_string("foo", env.options) == str


def test_load_env_bad_string(monkeypatch):
    """Should handle bad string variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_FOO", "bar")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_string("bar", env.options) is None


@given(
    val=st.integers(),
)
def test_load_env_integer(val):
    """Should load a integer variable from the environment."""
    with pytest.MonkeyPatch().context() as mp:
        mp.setenv("ELECTIVE_TEST_NUM", str(val))

        env = EnvConfiguration(prefix="ELECTIVE_TEST_")
        env.load()

        assert elective.process_integer("num", env.options) == val


def test_load_env_missing_integer(monkeypatch):
    """Should handle missing integer variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_NUM", "314")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_integer("bar", env.options) is None


def test_load_env_non_integer(monkeypatch):
    """Should handle non-integer variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_NUM", "3.14")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_integer("num", env.options) is None


@given(
    val=st.floats(),
)
def test_load_env_float(val):
    """Should load a float variable from the environment."""
    with pytest.MonkeyPatch().context() as mp:
        mp.setenv("ELECTIVE_TEST_NUM", str(val))

        env = EnvConfiguration(prefix="ELECTIVE_TEST_")
        env.load()

        if math.isnan(val):
            assert math.isnan(elective.process_float("num", env.options)) is True
        else:
            assert elective.process_float("num", env.options) == val


def test_load_env_missing_float(monkeypatch):
    """Should handle missing float variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_NUM", "3.14")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_float("bar", env.options) is None


def test_load_env_non_float(monkeypatch):
    """Should handle non-float variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_NUM", "bar")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_float("num", env.options) is None


def test_load_env_list(monkeypatch):
    """Should load a list variable from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_LIST__0", "0")
    monkeypatch.setenv("ELECTIVE_TEST_LIST__1", "1")
    monkeypatch.setenv("ELECTIVE_TEST_LIST__2", "2")
    monkeypatch.setenv("ELECTIVE_TEST_LIST__3", "3")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_list("list", env.options) == ["0", "1", "2", "3"]


def test_load_env_missing_list(monkeypatch):
    """Should handle missing list variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_LIST__0", "0")
    monkeypatch.setenv("ELECTIVE_TEST_LIST__1", "1")
    monkeypatch.setenv("ELECTIVE_TEST_LIST__2", "2")
    monkeypatch.setenv("ELECTIVE_TEST_LIST__3", "3")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_list("bar", env.options) is None


def test_load_env_non_list(monkeypatch):
    """Should handle non-list variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_DICT__ONE", "uno")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__TWO", "dos")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__THREE", "tres")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__FOUR", "cuatro")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_list("dict", env.options) is None


def test_load_env_dict(monkeypatch):
    """Should load a dict variable from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_DICT__ONE", "uno")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__TWO", "dos")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__THREE", "tres")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__FOUR", "cuatro")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    actual = elective.process_dict("dict", env.options)
    expected = {
        "ONE": "uno",
        "TWO": "dos",
        "THREE": "tres",
        "FOUR": "cuatro",
    }

    assert actual == expected


def test_load_env_missing_dict(monkeypatch):
    """Should handle missing dict variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_DICT__ONE", "uno")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__TWO", "dos")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__THREE", "tres")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__FOUR", "cuatro")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_dict("bar", env.options) is None


def test__load_env_non_dict(monkeypatch):
    """Should handle non-dict variables from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_DICT__0", "0")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__1", "1")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__2", "2")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__3", "3")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert elective.process_dict("dict", env.options) is None
