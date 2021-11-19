#!/usr/bin/env python
"""Elective configuration generator front end."""

import sys

sys.path.insert(0, "/home/gray/src/work/elective")

import elective  # noqa: E402


def main(argv=None):
    """Generate a new configurator."""
    try:
        conf = elective._load_toml_file(sys.argv[1])
        print(elective.generate(conf))
        sys.exit(0)
    except Exception as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":

    main()
