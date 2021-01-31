# SPDX-License-Identifier: GPL-3.0-or-later
#
# elective, a python program configuration option loader.
# Copyright (C) 2021 Jeremy A Gray <jeremy.a.gray@gmail.com>.
"""Sphinx configuration."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# Project information.

author = "Jeremy A Gray"
copyright = "2021, Jeremy A Gray"
project = "elective"
release = "0.0.1"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]

html_theme = "alabaster"
html_static_path = ["_static"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
