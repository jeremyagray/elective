"""Config() object tests."""

import sys
import types

import pytest

sys.path.insert(0, "/home/gray/src/work/elective")

import elective  # noqa: E402


def test_config_interface():
    """Test existence of functions and classes of elective.Config()."""
    assert isinstance(elective.Config.__init__, types.FunctionType)
    assert isinstance(elective.Config.__str__, types.FunctionType)
    assert isinstance(elective.Config.__repr__, types.FunctionType)
