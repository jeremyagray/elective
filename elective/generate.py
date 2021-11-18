# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""elective configuration functions."""

import textwrap


def _generate_file_banner(message=None):
    """Generate the generated file banner."""
    if message:
        return {
            "blocks": [
                f'"""{message}"""',
            ],
        }
    else:
        return {
            "blocks": ['"""Configuration module generated by elective."""'],
        }


def _generate_argparse_parser(description=None):
    """Generate an argument parser."""
    block = f"""\
def _create_argument_parser():
    \"\"\"Create an argparse argument parser.\"\"\"
    parser = argparse.ArgumentParser(
        description=\"\"\"\\
{description}
\"\"\",
    )

"""

    return {
        "dependencies": [
            "import argparse",
        ],
        "blocks": [block],
    }


def _generate_argparse_boolean(group="parser", **kwargs):
    """Generate an ``argparse`` boolean argument."""
    block = f"""\
    {group}.add_argument(
        \"-{kwargs['short']}\",
        \"--{kwargs['long']}\",
        dest=\"{kwargs['dest']}\",
        default=None,
        action=\"{kwargs['action']}\",
        help=\"{kwargs['help']}\",
    )
"""

    return {
        "dependencies": [
            "import argparse",
        ],
        "blocks": [block],
    }


def _generate_argparse_boolean_group(**kwargs):
    """Generate an ``argparse`` mutually exclusive boolean group."""
    block = f"    {kwargs['dest']}_group = parser.add_mutually_exclusive_group()\n"

    return {
        "dependencies": [
            "import argparse",
        ],
        "blocks": [
            block,
            _generate_argparse_boolean(
                group=f"{kwargs['dest']}_group",
                short=kwargs["short"].lower(),
                long=kwargs["long"].lower(),
                dest=kwargs["dest"],
                default=None,
                action="store_true",
                help=kwargs["help"],
            )["blocks"][0],
            _generate_argparse_boolean(
                group=f"{kwargs['dest']}_group",
                short=kwargs["short"].upper(),
                long="no-" + kwargs["long"].lower(),
                dest=kwargs["dest"],
                default=None,
                action="store_false",
                help=kwargs["help"],
            )["blocks"][0],
        ],
    }


def _generate_argparse_display_action(name, message, line_length=72):
    """Generate an ``argparse`` display action option."""
    parser_block = f"""\
    parser.add_argument(
        "--show-{name.lower()}",
        nargs=0,
        action=_show_{name.lower()}_action,
        help="Show {name.lower()}.",
    )
"""

    rendered_message = "\n\n".join(
        list(
            map(
                lambda item: "\n".join(textwrap.wrap(item.strip(), line_length)),
                textwrap.dedent(message).strip().split("\n\n"),
            )
        )
    )

    parser_class = f"""\
class _show_{name.lower()}_action(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(\"\"\"\\\n{rendered_message}\n\"\"\")

        parser.exit(status=0)\n\n
"""

    return {
        "blocks": [parser_block],
        "classes": [parser_class],
    }


def _generate_loader():
    """Generate the load configuration function."""
    block = """\
def load(argv=None):
    \"\"\"Load the configuration.\"\"\"
    args = _create_argument_parser().parse_args(argv)

    return args
"""

    return {
        "blocks": [block],
    }


def generate(conf=None):
    """Generate a configuration loader."""
    module = ""

    module += (
        _generate_file_banner(message="Configuration module generated by elective.",)[
            "blocks"
        ][0]
        + "\n\n"
    )

    description = """\
This program comes with ABSOLUTELY NO WARRANTY; for details type
``elective --show-warranty``.  This is free software, and you are welcome
to redistribute it under certain conditions; type ``elective
--show-license`` for details.
"""
    parser = _generate_argparse_parser(description=description)
    module += parser["dependencies"][0] + "\n\n"
    module += parser["blocks"][0] + "\n\n"

    warranty = _generate_argparse_display_action(
        name="warranty",
        message="""\
elective:  a Python configuration loader generator.

Copyright 2021 Jeremy A Gray <gray@flyquackswim.com>.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

""",
    )

    license = _generate_argparse_display_action(
        name="license",
        message="""\
elective:  a Python configuration loader generator.

Copyright 2021 Jeremy A Gray <gray@flyquackswim.com>.

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
    )

    module += warranty["blocks"][0]
    module += license["blocks"][0]

    group = _generate_argparse_boolean_group(
        short="c",
        long="spell-check",
        dest="spell_check",
        default=None,
        help="Spell check the commit.  Default is no spell checking.",
    )

    module += group["blocks"][0]
    module += group["blocks"][1]
    module += group["blocks"][2]

    module += "\n    return parser\n"

    module += warranty["classes"][0]
    module += license["classes"][0]

    module += "\n\n\n" + _generate_loader()["blocks"][0]

    return module
