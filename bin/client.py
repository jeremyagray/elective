#!/usr/bin/env python
#
# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Elective test program."""

import sys

import toml

sys.path.insert(0, "/home/gray/src/work/elective")

import elective  # noqa: E402


def main(argv=None):
    """Configure a program."""
    e = elective.ElectiveConfig()
    e.load_elective_config("./.client.elective")
    e.load_client_config()
    print(e.config)


if __name__ == "__main__":

    main()
