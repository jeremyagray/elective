# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
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


def test__are_keys_indices():
    """Should determine if keys are list indices."""
    # They are indices.
    ds = {
        "0": "apple",
        "1": "banana",
        "2": "orange",
    }

    assert elective.EnvConfiguration._are_keys_indices(ds) is True

    # Non-integer index.
    ds = {
        "zero": "apple",
        "1": "banana",
        "2": "orange",
    }

    assert elective.EnvConfiguration._are_keys_indices(ds) is False

    # Wrong start.
    ds = {
        "3": "apple",
        "1": "banana",
        "2": "orange",
    }

    assert elective.EnvConfiguration._are_keys_indices(ds) is False

    # Non-sequential.
    ds = {
        "0": "apple",
        "2": "banana",
        "3": "orange",
    }

    assert elective.EnvConfiguration._are_keys_indices(ds) is False


def test__is_listdict():
    """Should determine if keys are list indices."""
    # They are indices.
    ds = {
        "0": "apple",
        "1": "banana",
        "2": "orange",
    }

    assert elective.EnvConfiguration._is_listdict(ds) is True

    # Non-integer index.
    ds = {
        "zero": "apple",
        "1": "banana",
        "2": "orange",
    }

    assert elective.EnvConfiguration._is_listdict(ds) is False

    # Wrong start.
    ds = {
        "3": "apple",
        "1": "banana",
        "2": "orange",
    }

    assert elective.EnvConfiguration._is_listdict(ds) is False

    # Non-sequential.
    ds = {
        "0": "apple",
        "2": "banana",
        "3": "orange",
    }

    assert elective.EnvConfiguration._is_listdict(ds) is False


def test__convert_listdict_to_list():
    """Should convert listdict to list."""
    listdict = {
        "0": "apple",
        "1": "banana",
        "2": "orange",
    }

    expected = [
        "apple",
        "banana",
        "orange",
    ]

    assert elective.EnvConfiguration._convert_dict_to_list(listdict) == expected


def test_load_no_env():
    """Should handle no environment."""
    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert env.options == {}

    env = EnvConfiguration()
    env.load()

    assert env.options == {}


def test_load_multiple_definitions(monkeypatch):
    """Should raise on multiple definitions."""
    monkeypatch.setenv("ELECTIVE_TEST_CHECK", "true")
    monkeypatch.setenv("ELECTIVE_TEST_CHECK__ONE__ONE", "1")
    monkeypatch.setenv("ELECTIVE_TEST_CHECK__ONE__TWO", "2")
    monkeypatch.setenv("ELECTIVE_TEST_CHECK__ONE__THREE", "3")
    env = EnvConfiguration(prefix="ELECTIVE_TEST_")

    with pytest.raises(Exception) as exc:
        env.load()

    assert "defined multiple times" in str(exc.value)


def test_load_undefined(monkeypatch):
    """Should raise ``KeyError`` on undefined variables."""
    monkeypatch.setenv("ELECTIVE_TEST_CHECK", "true")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    with pytest.raises(KeyError):
        env.options["BOB"]


@pytest.mark.parametrize(
    "val",
    ("true", "yes", "1", "false", "no", "0"),
)
def test_load_boolean(val, monkeypatch):
    """Should load a boolean variable from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_CHECK", val)
    monkeypatch.setenv("ELECTIVE_TEST_NO_CHECK", val)

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert env.options == {
        "CHECK": val,
        "NO_CHECK": val,
    }


@given(
    str=st.text(alphabet=st.characters(blacklist_categories=("Cc", "Cs"))),
)
def test_load_string(str):
    """Should load a string variable from the environment."""
    with pytest.MonkeyPatch().context() as mp:
        mp.setenv("ELECTIVE_TEST_FOO", str)

        env = EnvConfiguration(prefix="ELECTIVE_TEST_")
        env.load()

        assert env.options["FOO"] == str


@given(
    val=st.integers(),
)
def test_load_integer(val):
    """Should load a integer variable from the environment."""
    with pytest.MonkeyPatch().context() as mp:
        mp.setenv("ELECTIVE_TEST_NUM", str(val))

        env = EnvConfiguration(prefix="ELECTIVE_TEST_")
        env.load()

        assert int(env.options["NUM"]) == val


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
            assert math.isnan(float(env.options["NUM"]))
        else:
            assert float(env.options["NUM"]) == val


def test_load_list(monkeypatch):
    """Should load a list variable from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_LIST__0", "0")
    monkeypatch.setenv("ELECTIVE_TEST_LIST__1", "1")
    monkeypatch.setenv("ELECTIVE_TEST_LIST__2", "2")
    monkeypatch.setenv("ELECTIVE_TEST_LIST__3", "3")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert env.options["LIST"] == ["0", "1", "2", "3"]


def test_load_list_nested_in_dict(monkeypatch):
    """Should load a list nested in a dict."""
    monkeypatch.setenv("ELECTIVE_TEST_DICT__LIST__0", "0")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__LIST__1", "1")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__LIST__2", "2")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__LIST__3", "3")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    expected = {
        "DICT": {
            "LIST": [
                "0",
                "1",
                "2",
                "3",
            ],
        },
    }

    assert env.options == expected


def test_load_list_nested_in_list(monkeypatch):
    """Should load a list nested in a list."""
    monkeypatch.setenv("ELECTIVE_TEST_LIST__0__0", "0")
    monkeypatch.setenv("ELECTIVE_TEST_LIST__0__1", "1")
    monkeypatch.setenv("ELECTIVE_TEST_LIST__0__2", "2")
    monkeypatch.setenv("ELECTIVE_TEST_LIST__0__3", "3")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    expected = {
        "LIST": [
            [
                "0",
                "1",
                "2",
                "3",
            ],
        ],
    }

    assert env.options == expected


def test_load_env_dict(monkeypatch):
    """Should load a dict variable from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_DICT__ONE", "uno")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__TWO", "dos")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__THREE", "tres")
    monkeypatch.setenv("ELECTIVE_TEST_DICT__FOUR", "cuatro")

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    expected = {
        "DICT": {
            "ONE": "uno",
            "TWO": "dos",
            "THREE": "tres",
            "FOUR": "cuatro",
        },
    }

    assert env.options == expected


def test_load_mixed(monkeypatch):
    """Should load mixed options from the environment."""
    vals = [
        ("ELECTIVE_TEST_BREAKFAST", "toast"),
        ("ELECTIVE_TEST_FRUITLIST__0", "apple"),
        ("ELECTIVE_TEST_FRUITLIST__1", "banana"),
        ("ELECTIVE_TEST_FRUITLIST__2", "orange"),
        ("ELECTIVE_TEST_FOOD__FRUITLIST__0", "apple"),
        ("ELECTIVE_TEST_FOOD__FRUITLIST__1", "banana"),
        ("ELECTIVE_TEST_FOOD__FRUITLIST__2", "orange"),
        ("ELECTIVE_TEST_FRUIT__APPLE", "2"),
        ("ELECTIVE_TEST_FRUIT__BANANA", "3"),
        ("ELECTIVE_TEST_FRUIT__ORANGE", "5"),
        ("ELECTIVE_TEST_FOOD__FRUIT__APPLE", "2"),
        ("ELECTIVE_TEST_FOOD__FRUIT__BANANA", "3"),
        ("ELECTIVE_TEST_FOOD__FRUIT__ORANGE", "5"),
    ]

    for (name, val) in vals:
        monkeypatch.setenv(name, val)

    expected = {
        "BREAKFAST": "toast",
        "FRUITLIST": [
            "apple",
            "banana",
            "orange",
        ],
        "FRUIT": {
            "APPLE": "2",
            "BANANA": "3",
            "ORANGE": "5",
        },
        "FOOD": {
            "FRUITLIST": [
                "apple",
                "banana",
                "orange",
            ],
            "FRUIT": {
                "APPLE": "2",
                "BANANA": "3",
                "ORANGE": "5",
            },
        },
    }

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    assert env.options == expected


def test_load_mixed_no_prefix(monkeypatch):
    """Should load mixed options from the environment without prefixes."""
    vals = [
        ("ELECTIVE_TEST_BREAKFAST", "toast"),
        ("ELECTIVE_TEST_FRUITLIST__0", "apple"),
        ("ELECTIVE_TEST_FRUITLIST__1", "banana"),
        ("ELECTIVE_TEST_FRUITLIST__2", "orange"),
        ("ELECTIVE_TEST_FOOD__FRUITLIST__0", "apple"),
        ("ELECTIVE_TEST_FOOD__FRUITLIST__1", "banana"),
        ("ELECTIVE_TEST_FOOD__FRUITLIST__2", "orange"),
        ("ELECTIVE_TEST_FRUIT__APPLE", "2"),
        ("ELECTIVE_TEST_FRUIT__BANANA", "3"),
        ("ELECTIVE_TEST_FRUIT__ORANGE", "5"),
        ("ELECTIVE_TEST_FOOD__FRUIT__APPLE", "2"),
        ("ELECTIVE_TEST_FOOD__FRUIT__BANANA", "3"),
        ("ELECTIVE_TEST_FOOD__FRUIT__ORANGE", "5"),
    ]

    for (name, val) in vals:
        monkeypatch.setenv(
            f"ELECTIVE_{name.removeprefix('ELECTIVE_TEST_')}",
            val,
        )

    expected = {
        "BREAKFAST": "toast",
        "FRUITLIST": [
            "apple",
            "banana",
            "orange",
        ],
        "FRUIT": {
            "APPLE": "2",
            "BANANA": "3",
            "ORANGE": "5",
        },
        "FOOD": {
            "FRUITLIST": [
                "apple",
                "banana",
                "orange",
            ],
            "FRUIT": {
                "APPLE": "2",
                "BANANA": "3",
                "ORANGE": "5",
            },
        },
    }

    env = EnvConfiguration()
    env.load()

    assert env.options == expected


def test_dump_no_export(monkeypatch):
    """Should dump options, without export, to the environment."""
    vals = [
        ("ELECTIVE_TEST_BREAKFAST", "toast"),
        ("ELECTIVE_TEST_FRUITLIST__0", "apple"),
        ("ELECTIVE_TEST_FRUITLIST__1", "banana"),
        ("ELECTIVE_TEST_FRUITLIST__2", "orange"),
        ("ELECTIVE_TEST_FOOD__FRUITLIST__0", "apple"),
        ("ELECTIVE_TEST_FOOD__FRUITLIST__1", "banana"),
        ("ELECTIVE_TEST_FOOD__FRUITLIST__2", "orange"),
        ("ELECTIVE_TEST_FRUIT__APPLE", "2"),
        ("ELECTIVE_TEST_FRUIT__BANANA", "3"),
        ("ELECTIVE_TEST_FRUIT__ORANGE", "5"),
        ("ELECTIVE_TEST_FOOD__FRUIT__APPLE", "2"),
        ("ELECTIVE_TEST_FOOD__FRUIT__BANANA", "3"),
        ("ELECTIVE_TEST_FOOD__FRUIT__ORANGE", "5"),
    ]

    for (name, val) in vals:
        monkeypatch.setenv(name, val)

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    output = env.dump()
    for (name, val) in vals:
        assert f"export {name}='{val}'" in output


def test_dump_export(monkeypatch):
    """Should dump options to the environment."""
    vals = [
        ("ELECTIVE_TEST_BREAKFAST", "toast"),
        ("ELECTIVE_TEST_FRUITLIST__0", "apple"),
        ("ELECTIVE_TEST_FRUITLIST__1", "banana"),
        ("ELECTIVE_TEST_FRUITLIST__2", "orange"),
        ("ELECTIVE_TEST_FOOD__FRUITLIST__0", "apple"),
        ("ELECTIVE_TEST_FOOD__FRUITLIST__1", "banana"),
        ("ELECTIVE_TEST_FOOD__FRUITLIST__2", "orange"),
        ("ELECTIVE_TEST_FRUIT__APPLE", "2"),
        ("ELECTIVE_TEST_FRUIT__BANANA", "3"),
        ("ELECTIVE_TEST_FRUIT__ORANGE", "5"),
        ("ELECTIVE_TEST_FOOD__FRUIT__APPLE", "2"),
        ("ELECTIVE_TEST_FOOD__FRUIT__BANANA", "3"),
        ("ELECTIVE_TEST_FOOD__FRUIT__ORANGE", "5"),
    ]

    for (name, val) in vals:
        monkeypatch.setenv(name, val)

    env = EnvConfiguration(prefix="ELECTIVE_TEST_")
    env.load()

    output = env.dump(export=False)
    for (name, val) in vals:
        assert f"{name}='{val}'" in output
