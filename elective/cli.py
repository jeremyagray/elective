# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""CLI loader."""

import argparse
import textwrap

from .config import Configuration


class CliConfiguration(Configuration):
    """CLI loader for the client program."""

    def __init__(self, *args, **kwargs):
        """Initialize a client argument parser."""
        # Initialize ourself.
        self.parser = argparse.ArgumentParser()

        # Call the super.
        super().__init__(*args, **kwargs)

    def _set_description(self, description):
        """Set the argparse description."""
        self.parser.description = description

    def reset_parser(self):
        """Reset an argument parser."""
        self.parser = argparse.ArgumentParser()

    def _register_boolean(self, **kwargs):
        """Register a boolean argument in the parser."""
        self.parser.add_argument(
            "-{kwargs.get('short', None)}",
            "--{kwargs.get('long', None)}",
            dest=kwargs.get("dest", None),
            default=None,
            action=None,
            help=kwargs.get("help", None),
        )

    def _register_boolean_group(self, **kwargs):
        """Register a mutually exclusive boolean group in the parser."""
        group = self.parser.add_mutually_exclusive_group()
        dest = kwargs.get("dest", None)
        help = kwargs.get("help", None)
        short_pos = "-" + kwargs.get("short_pos", None)
        short_neg = "-" + kwargs.get("short_neg", None)
        long_pos = "--" + kwargs.get("long_pos", None)
        long_neg = "--" + kwargs.get("long_neg", None)

        group.add_argument(
            short_pos,
            long_pos,
            dest=dest,
            default=None,
            action="store_true",
            help=help,
        )
        group.add_argument(
            short_neg,
            long_neg,
            dest=dest,
            default=None,
            action="store_false",
            help=help,
        )

    def _register_display_action(self, line_length=72, **kwargs):
        """Register a display action."""
        name = kwargs.get("name", None)
        dest = kwargs.get("dest", None)
        default = kwargs.get("default", None)
        help = kwargs.get("help", None)

        rendered_message = "\n\n".join(
            list(
                map(
                    lambda item: "\n".join(
                        textwrap.wrap(
                            item.strip(),
                            line_length,
                        ),
                    ),
                    textwrap.dedent(default).strip().split("\n\n"),
                )
            )
        )

        class _DisplayAction(argparse.Action):
            """Custom display action for argparse."""

            def __init__(self, option_strings, dest, **kwargs):
                """Initialize display action."""
                super().__init__(option_strings, dest, **kwargs)

            def __call__(self, parser, namespace, values, optionString=None):
                """Call the display action."""
                print(rendered_message)

                parser.exit(status=0),

        self.parser.add_argument(
            f"--{name.lower()}",
            nargs=0,
            action=_DisplayAction,
            help=help,
            dest=dest,
        )

    def config(self, ec):
        """Configure a client argument parser."""
        # Set the program description.
        self._set_description(ec.elective["description"])

        # Add any options to the parser.
        for (k, v) in ec.options.items():
            if "cli" in v["providers"]:
                if v["type"] == "display":
                    self._register_display_action(
                        name=k,
                        dest=v["dest"] or k,
                        default=v["default"],
                        help=v["help"],
                    )
                elif v["type"] == "boolean":
                    self._register_boolean_group(
                        dest=v["dest"] or k,
                        help=v["help"],
                        short_pos=v["short_pos"],
                        short_neg=v["short_neg"],
                        long_pos=v["long_pos"],
                        long_neg=v["long_neg"],
                    )

    def load(self, *args, **kwargs):
        """Load CLI arguments."""
        # Pop our arguments.
        argv = kwargs.pop("argv", None)

        # Convert the argparse `Namespace()` object to a dict.
        self.options = vars(self.parser.parse_args(args=argv))
