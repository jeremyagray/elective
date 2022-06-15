# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Elective config tests."""

import types

import pytest
from hypothesis import given
from hypothesis import strategies as st

import elective


def test_elective_config_interface():
    """Should have the correct interface."""
    assert isinstance(elective.ElectiveConfig.__init__, types.FunctionType)
    assert isinstance(elective.ElectiveConfig.__str__, types.FunctionType)
    assert isinstance(elective.ElectiveConfig.__repr__, types.FunctionType)


def test_elective_config_load_combine_exception(fs):
    """Should throw ValueError on an invalid combine option."""
    # Create a configuration file.
    fn = "config.toml"
    fs.create_file(fn)
    with open(fn, "w") as f:
        f.write(
            """[elective]

description = '''
This program comes with ABSOLUTELY NO WARRANTY; for details type
``elective --show-warranty``.  This is free software, and you are welcome
to redistribute it under certain conditions; type ``elective
--show-license`` for details.
'''

name = "elective"

combine = "booyah"

order = [
  "default",
  "toml",
  "json",
  "yaml",
  "bespon",
  "env",
  "cli",
]
"""
        )

    conf = elective.ElectiveConfig()
    with pytest.raises(ValueError):
        conf.load_elective_config(fn)


def test_elective_config_load_combine(fs):
    """Should load a combine option."""
    # Create a configuration file.
    fn = "config.toml"
    fs.create_file(fn)
    with open(fn, "w") as f:
        f.write(
            """[elective]

description = '''
This program comes with ABSOLUTELY NO WARRANTY; for details type
``elective --show-warranty``.  This is free software, and you are welcome
to redistribute it under certain conditions; type ``elective
--show-license`` for details.
'''

name = "elective"

combine = "left"

order = [
  "default",
  "toml",
  "json",
  "yaml",
  "bespon",
  "env",
  "cli",
]
"""
        )

    conf = elective.ElectiveConfig()
    conf.load_elective_config(fn)
    assert conf.elective["combine"] == "left"

    with open(fn, "w") as f:
        f.write(
            """[elective]

description = '''
This program comes with ABSOLUTELY NO WARRANTY; for details type
``elective --show-warranty``.  This is free software, and you are welcome
to redistribute it under certain conditions; type ``elective
--show-license`` for details.
'''

name = "elective"

combine = "right"

order = [
  "default",
  "toml",
  "json",
  "yaml",
  "bespon",
  "env",
  "cli",
]
"""
        )

    conf = elective.ElectiveConfig()
    conf.load_elective_config(fn)
    assert conf.elective["combine"] == "right"

    with open(fn, "w") as f:
        f.write(
            """[elective]

description = '''
This program comes with ABSOLUTELY NO WARRANTY; for details type
``elective --show-warranty``.  This is free software, and you are welcome
to redistribute it under certain conditions; type ``elective
--show-license`` for details.
'''

name = "elective"

order = [
  "default",
  "toml",
  "json",
  "yaml",
  "bespon",
  "env",
  "cli",
]
"""
        )

    conf = elective.ElectiveConfig()
    conf.load_elective_config(fn)
    assert conf.elective["combine"] is None


def test_elective_config_load_prefix(fs):
    """Should load the prefix option."""
    # Create a configuration file.
    fn = "config.toml"
    fs.create_file(fn)
    with open(fn, "w") as f:
        f.write(
            """[elective]

description = '''
This program comes with ABSOLUTELY NO WARRANTY; for details type
``elective --show-warranty``.  This is free software, and you are welcome
to redistribute it under certain conditions; type ``elective
--show-license`` for details.
'''

name = "elective"

combine = "left"

order = [
  "default",
  "toml",
  "json",
  "yaml",
  "bespon",
  "env",
  "cli",
]
"""
        )

    conf = elective.ElectiveConfig()
    conf.load_elective_config(fn)
    assert conf.elective["prefix"] == "ELECTIVE_ELECTIVE_"


def test_elective_config_load_description(fs):
    """Should load the description option."""
    # Create a configuration file.
    fn = "config.toml"
    fs.create_file(fn)
    with open(fn, "w") as f:
        f.write(
            """[elective]

description = '''
This program comes with ABSOLUTELY NO WARRANTY; for details type
``elective --show-warranty``.  This is free software, and you are welcome
to redistribute it under certain conditions; type ``elective
--show-license`` for details.
'''

name = "elective"
combine = "left"

order = [
  "default",
  "toml",
  "json",
  "yaml",
  "bespon",
  "env",
  "cli",
]
"""
        )

    description = """This program comes with ABSOLUTELY NO WARRANTY; for details type
``elective --show-warranty``.  This is free software, and you are welcome
to redistribute it under certain conditions; type ``elective
--show-license`` for details.
"""

    conf = elective.ElectiveConfig()
    conf.load_elective_config(fn)
    assert conf.elective["description"] == description

    with open(fn, "w") as f:
        f.write(
            """[elective]
name = "elective"
combine = "right"

order = [
  "default",
  "toml",
  "json",
  "yaml",
  "bespon",
  "env",
  "cli",
]
"""
        )

    conf = elective.ElectiveConfig()
    conf.load_elective_config(fn)
    assert conf.elective["description"] is None


def test__process_single_option_idempotent():
    """Should return the same dictionary."""
    options = {
        "type": "boolean",
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "default": False,
        "short_pos": "c",
        "long_pos": "spell-check",
        "short_neg": "C",
        "long_neg": "no-spell-check",
        "help": "Spell check.  Default is no spell checking.",
        "dest": "spell",
    }

    assert options == elective.ElectiveConfig._process_single_option(options)


def test__process_single_option_missing_is_none():
    """Should return the same dictionary."""
    options = {
        "type": "boolean",
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "short_pos": "c",
        "long_pos": "spell-check",
        "short_neg": "C",
        "long_neg": "no-spell-check",
        "help": "Spell check.  Default is no spell checking.",
        "dest": "spell",
    }
    cleaned = {
        "type": "boolean",
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "default": None,
        "short_pos": "c",
        "long_pos": "spell-check",
        "short_neg": "C",
        "long_neg": "no-spell-check",
        "help": "Spell check.  Default is no spell checking.",
        "dest": "spell",
    }

    assert cleaned == elective.ElectiveConfig._process_single_option(options)


def test__process_single_option_extra_is_ignored():
    """Should return the same dictionary."""
    options = {
        "type": "boolean",
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "default": False,
        "short_pos": "c",
        "long_pos": "spell-check",
        "short_neg": "C",
        "long_neg": "no-spell-check",
        "help": "Spell check.  Default is no spell checking.",
        "dest": "spell",
        "yourface": "is ugly",
    }
    cleaned = {
        "type": "boolean",
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "default": False,
        "short_pos": "c",
        "long_pos": "spell-check",
        "short_neg": "C",
        "long_neg": "no-spell-check",
        "help": "Spell check.  Default is no spell checking.",
        "dest": "spell",
    }

    assert cleaned == elective.ElectiveConfig._process_single_option(options)
    assert hasattr(cleaned, "yourface") is False


def test__process_option_one_idempotent():
    """Should return the same dictionary."""
    options = {
        "type": "boolean",
        "providers": [
            "cli",
            "env",
            "file",
        ],
        "default": False,
        "short_pos": "c",
        "long_pos": "spell-check",
        "short_neg": "C",
        "long_neg": "no-spell-check",
        "help": "Spell check.  Default is no spell checking.",
        "dest": "spell",
    }

    assert options == elective.ElectiveConfig._process_option(options)


def test__process_option_list_idempotent():
    """Should return the same list."""
    options = [
        {
            "type": "boolean",
            "providers": [
                "cli",
                "env",
                "file",
            ],
            "default": False,
            "short_pos": "c",
            "long_pos": "spell-check",
            "short_neg": "C",
            "long_neg": "no-spell-check",
            "help": "Spell check.  Default is no spell checking.",
            "dest": "spell",
        },
        {
            "type": "boolean",
            "providers": [
                "cli",
                "env",
                "file",
            ],
            "default": False,
            "short_pos": "w",
            "long_pos": "wrap",
            "short_neg": "W",
            "long_neg": "no-wrap",
            "help": "Wrap lines.  Default is no line wrapping.",
            "dest": "wrap",
        },
    ]

    assert options == elective.ElectiveConfig._process_option(options)


def test_elective_config_load_options(fs):
    """Should load a combine option."""
    # Create a configuration file.
    fn = "config.toml"
    fs.create_file(fn)
    with open(fn, "w") as f:
        f.write(
            """[elective]

description = '''
This program comes with ABSOLUTELY NO WARRANTY; for details type
``elective --show-warranty``.  This is free software, and you are welcome
to redistribute it under certain conditions; type ``elective
--show-license`` for details.
'''

name = "elective"

# ("left" | "right" | None)
combine = "right"

order = [
  "default",
  "toml",
  "json",
  "yaml",
  "bespon",
  "env",
  "cli",
]

[elective.options]

[elective.options.show-license]

providers = [
  "cli",
]
type = "display"
default = '''
elective:  a Python configuration loader generator.

Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
help = "Show license."

[elective.options.show-warranty]

providers = [
  "cli",
]
type = "display"
default = '''
elective:  a Python configuration loader generator.

Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
help = "Show warranty."

[elective.options.spell-check]

providers = [
  "cli",
  "env",
  "file",
]
type = "boolean"
default = false
short_pos = "c"
short_neg = "C"
long_pos = "spell-check"
long_neg = "no-spell-check"
dest = "spell"
help = "Spell check.  Default is no spell checking."

[elective.options.line-wrap]

providers = [
  "cli",
  "env",
  "file",
]
type = "boolean"
default = false
short_pos = "w"
short_neg = "W"
long_pos = "wrap"
long_neg = "no-wrap"
dest = "wrap"
help = "Wrap lines.  Default is no line wrapping."
"""
        )

    options = {
        "spell-check": {
            "type": "boolean",
            "providers": [
                "cli",
                "env",
                "file",
            ],
            "default": False,
            "short_pos": "c",
            "long_pos": "spell-check",
            "short_neg": "C",
            "long_neg": "no-spell-check",
            "help": "Spell check.  Default is no spell checking.",
            "dest": "spell",
        },
        "line-wrap": {
            "type": "boolean",
            "providers": [
                "cli",
                "env",
                "file",
            ],
            "default": False,
            "short_pos": "w",
            "long_pos": "wrap",
            "short_neg": "W",
            "long_neg": "no-wrap",
            "help": "Wrap lines.  Default is no line wrapping.",
            "dest": "wrap",
        },
        "show-warranty": {
            "providers": [
                "cli",
            ],
            "type": "display",
            "default": """elective:  a Python configuration loader generator.

Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""",
            "help": "Show warranty.",
            "short_neg": None,
            "long_neg": None,
            "short_pos": None,
            "long_pos": None,
            "dest": None,
        },
        "show-license": {
            "providers": [
                "cli",
            ],
            "type": "display",
            "default": """elective:  a Python configuration loader generator.

Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""",
            "help": "Show license.",
            "short_neg": None,
            "long_neg": None,
            "short_pos": None,
            "long_pos": None,
            "dest": None,
        },
    }

    conf = elective.ElectiveConfig()
    conf.load_elective_config(fn)

    assert "line-wrap" in conf.options
    assert conf.options["line-wrap"] == options["line-wrap"]
    assert "spell-check" in conf.options
    assert conf.options["spell-check"] == options["spell-check"]
    assert "show-license" in conf.options
    assert conf.options["show-license"] == options["show-license"]
    assert "show-warranty" in conf.options
    assert conf.options["show-warranty"] == options["show-warranty"]
