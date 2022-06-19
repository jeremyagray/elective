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

        print(f"args: {args}")
        for pair in args:
            print(f"pair: {pair}")
            self.set(pair[0], pair[1])

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

    def set(self, value, source):
        """Set the current state."""
        self.values.append(value)
        self.sources.append(source)
        self._current = value
