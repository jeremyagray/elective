# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Scalar variable value and history support."""


class State:
    """A variable with history."""

    def __init__(self, initial=None):
        """Initialize a state."""
        self.values = []
        self.sources = []
        self._current = None

        if initial:
            self.set(initial[0], initial[1])

    def __eq__(self, other):
        """Determine if two states are equal."""
        if all(
            (
                len(self.values) > 0,
                len(other.values) > 0,
                len(self.sources) > 0,
                len(other.sources) > 0,
            )
        ):
            print("good length")
            print(f"self v:{self.values[-1]} s:{self.sources[-1]}")
            print(f"other v:{other.values[-1]} s:{other.sources[-1]}")
            print(
                self.values[-1] == other.values[-1]
                and self.sources[-1] == other.sources[-1]
            )
            return (
                self.values[-1] == other.values[-1]
                and self.sources[-1] == other.sources[-1]
            )

        return False

    @property
    def current(self):
        """Get the current value of the state."""
        return self._current

    def set(self, value, source):
        """Set the current state."""
        self.values.append(value)
        self.sources.append(source)
        self._current = value
