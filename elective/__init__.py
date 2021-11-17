# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""elective:  a Python configuration loader generator."""

from .config import Config
from .config import load
from .generate import _generate_argparse_display_action
from .generate import _generate_argparse_parser
from .generate import _generate_file_banner
from .generate import generate
