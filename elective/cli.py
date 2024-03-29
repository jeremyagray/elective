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
        # Call the super.
        super().__init__(*args, **kwargs)

        # Initialize ourself.
        self.parser = argparse.ArgumentParser()

        # Pop our arguments.
        self.parser.description = kwargs.pop("description", None)
        self.options = kwargs.pop("options")

    def _register_boolean(self, **kwargs):
        """Register a boolean argument in the parser."""
        self.parser.add_argument(
            f"-{kwargs.get('short', None)}",
            f"--{kwargs.get('long', None)}",
            dest=kwargs.get("dest", None),
            default=kwargs.get("default", None),
            action=kwargs.get("action", None),
            help=kwargs.get("help", None),
        )

    def _register_int(self, **kwargs):
        """Register an integer argument in the parser."""
        self.parser.add_argument(
            f"-{kwargs.get('short', None)}",
            f"--{kwargs.get('long', None)}",
            dest=kwargs.get("dest", None),
            default=kwargs.get("default", None),
            help=kwargs.get("help", None),
            type=int,
        )

    def _register_float(self, **kwargs):
        """Register a float argument in the parser."""
        self.parser.add_argument(
            f"-{kwargs.get('short', None)}",
            f"--{kwargs.get('long', None)}",
            dest=kwargs.get("dest", None),
            default=kwargs.get("default", None),
            help=kwargs.get("help", None),
            type=float,
        )

    def _register_str(self, **kwargs):
        """Register a string argument in the parser."""
        self.parser.add_argument(
            f"-{kwargs.get('short', None)}",
            f"--{kwargs.get('long', None)}",
            dest=kwargs.get("dest", None),
            default=kwargs.get("default", None),
            help=kwargs.get("help", None),
            type=str,
        )

    def _register_list(self, **kwargs):
        """Register a list argument in the parser."""
        self.parser.add_argument(
            f"-{kwargs.get('short', None)}",
            f"--{kwargs.get('long', None)}",
            dest=kwargs.get("dest", None),
            default=kwargs.get("default", None),
            help=kwargs.get("help", None),
            type=lambda s: []
            if len(s) == 0
            else [item.strip() for item in s.split(",")],
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

    def config(self):
        """Configure a client argument parser."""
        # Add any options to the parser.
        for (k, v) in self.options.items():
            if "cli" in v["providers"]:
                dest = k
                # Optionally set ``dest``.
                try:
                    dest = v["dest"]
                except (KeyError):
                    pass

                if v["type"] == "display":
                    self._register_display_action(
                        name=k,
                        dest=dest,
                        default=v["default"],
                        help=v["help"],
                    )
                elif v["type"] == "boolean_group":
                    self._register_boolean_group(
                        dest=dest,
                        help=v["help"],
                        short_pos=v["short_pos"],
                        short_neg=v["short_neg"],
                        long_pos=v["long_pos"],
                        long_neg=v["long_neg"],
                    )
                elif v["type"] == "boolean":
                    self._register_boolean(
                        action=v["action"],
                        default=v["default"],
                        dest=dest,
                        help=v["help"],
                        long=v["long"],
                        short=v["short"],
                    )
                elif v["type"] == "int":
                    self._register_int(
                        default=v["default"],
                        dest=dest,
                        help=v["help"],
                        long=v["long"],
                        short=v["short"],
                    )
                elif v["type"] == "float":
                    self._register_float(
                        default=v["default"],
                        dest=dest,
                        help=v["help"],
                        long=v["long"],
                        short=v["short"],
                    )
                elif v["type"] == "str":
                    self._register_str(
                        default=v["default"],
                        dest=dest,
                        help=v["help"],
                        long=v["long"],
                        short=v["short"],
                    )
                elif v["type"] == "list":
                    self._register_list(
                        default=v["default"],
                        dest=dest,
                        help=v["help"],
                        long=v["long"],
                        short=v["short"],
                    )

    def reset_parser(self):
        """Reset an argument parser."""
        self.parser = argparse.ArgumentParser()

    def load(self, *args, **kwargs):
        """Load CLI arguments."""
        # Pop our arguments.
        argv = kwargs.pop("argv", None)

        # Convert the argparse `Namespace()` object to a dict.
        if argv is not None:
            self.options = vars(self.parser.parse_args(argv))
        else:
            self.options = vars(self.parser.parse_args())
