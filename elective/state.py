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

    def __init__(self, *args):
        """Initialize a state.

        Initialize a state with the tuples supplied in ``args``.

        Parameters
        ----------
        args : tuple
            An iterable of tuples of value and source pairs.
        """
        self.values = []
        self.sources = []
        self._current = None

        for pair in args:
            self.update(pair[0], pair[1])

    def __str__(self):
        """Stringify a state."""
        if self.values:
            return f"current value: {self.values[-1]} source: {self.sources[-1]}"
        else:
            return "current value: None source: None"

    def __repr__(self):
        """Reproduce a state."""
        if self.values:
            return f"State(({self.values[-1]}, {self.sources[-1]}))"
        else:
            return "State((, ))"

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
            return (
                self.values[-1] == other.values[-1]
                and self.sources[-1] == other.sources[-1]
            )

        return False

    @property
    def current(self):
        """Get the current value of the state."""
        return self._current

    def update(self, value, source):
        """Update the current state."""
        self.values.append(value)
        self.sources.append(source)
        self._current = value

    def append(self, other):
        """Append other's history onto self's history."""
        if not isinstance(other, State):
            raise TypeError("other must be a State")

        for (v, s) in zip(other.values, other.sources):
            self.update(v, s)
