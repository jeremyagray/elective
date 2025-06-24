# ******************************************************************************
#
# elective, a Python configuration loader generator
#
# Copyright 2021-2025 Jeremy A Gray <gray@flyquackswim.com>.
#
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Generic ``Configuration`` tests."""

import pytest

import elective


def test_configuration_initial_is_empty():
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
