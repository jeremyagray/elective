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

import elective


def test__load_env_no_env():
    """Should handle no environment."""
    actual = elective.load_env(prefix="ELECTIVE_TEST_")
    expected = {}

    assert actual == expected


def test__load_env_variable(monkeypatch):
    """Should load a variable from the environment."""
    monkeypatch.setenv("ELECTIVE_TEST_CHECK", "true")
    monkeypatch.setenv("ELECTIVE_TEST_NOCHECK", "false")

    actual = elective.load_env(prefix="ELECTIVE_TEST_")
    expected = {
        "CHECK": "true",
        "NOCHECK": "false",
    }

    assert actual == expected
