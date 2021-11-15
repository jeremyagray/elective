#!/usr/bin/env python
"""Test and development entry point."""

import sys

sys.path.insert(0, "/home/gray/src/work/elective")

import elective  # noqa: E402

sys.path.insert(0, "/home/gray/src/work/elective/bin")

from testconfig import load  # noqa: E402


def main(argv=None):
    """Run the test program."""
    try:
        print(load(argv))
        sys.exit(0)
    except Exception as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":

    main()
