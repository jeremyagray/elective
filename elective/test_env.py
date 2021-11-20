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

import pytest

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
