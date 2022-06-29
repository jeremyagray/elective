# ******************************************************************************
#
# elective:  a Python configuration loader generator
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""elective configuration functions."""

import copy

from .cli import CliConfiguration
from .exceptions import ElectiveFileLoadingError
from .files import FileConfiguration
from .state import State


class ElectiveConfig:
    """Elective configuration options and values."""

    def __init__(self):
        """Initialize an ``ElectiveConfig`` object."""
        self.elective = {}
        self.elective["description"] = ""
        self.elective["prefix"] = ""
        self.elective["combine"] = "left"
        self.elective["order"] = [
            "defaults",
            "toml",
            "json",
            "yaml",
            "bespon",
            "env",
            "cli",
        ]
        self.defaults = {}
        self.options = {}
        self._configured = False

    @staticmethod
    def _make_stateful(d, source):
        """Convert ``d`` from a dict to a stateful dict."""
        # Scalar types; return State.
        if any(
            (
                isinstance(d, str),
                isinstance(d, bool),
                isinstance(d, int),
                isinstance(d, float),
                d is None,
            )
        ):
            return State((d, source))

        # Lists; recurse on items.
        if any(
            (
                isinstance(d, list),
                isinstance(d, tuple),
            )
        ):
            res = []

            for item in d:
                res.append(ElectiveConfig._make_stateful(item, source))

            return res

        # Dicts; recurse on common key/value pairs.
        if isinstance(d, dict):
            res = {}
            for (k, v) in d.items():
                res[k] = ElectiveConfig._make_stateful(v, source)

            return res

        raise NotImplementedError(
            "stateful handling of type {type(d)} is not implemented"
        )

    @staticmethod
    def _process_option(option):
        """Process an option."""
        cleaned = None

        if isinstance(option, list):
            if not cleaned:
                cleaned = []
                for item in option:
                    cleaned.append(ElectiveConfig._process_single_option(item))
        else:
            cleaned = ElectiveConfig._process_single_option(option)

        return cleaned

    @staticmethod
    def _process_single_option(option):
        """Process a single option."""
        cleaned = {}
        cleaned["type"] = option.get("type", None)
        cleaned["providers"] = option.get("providers", None)
        cleaned["default"] = option.get("default", None)
        cleaned["short_pos"] = option.get("short_pos", None)
        cleaned["long_pos"] = option.get("long_pos", None)
        cleaned["short_neg"] = option.get("short_neg", None)
        cleaned["long_neg"] = option.get("long_neg", None)
        cleaned["help"] = option.get("help", None)
        cleaned["dest"] = option.get("dest", None)

        return cleaned

    def _set_defaults(self, options):
        """Set the defaults from the options."""
        for (k, v) in options.items():
            self.defaults[k] = v["default"]

        self.defaults = ElectiveConfig._make_stateful(self.defaults, "default")

    def load_elective_config(self, fn):
        """Load configuration data."""
        options = FileConfiguration._load_file(
            fn=fn,
            section="elective",
        )

        self.elective["description"] = options.get("description", None)

        try:
            self.elective["name"] = options["name"]
            self.elective["prefix"] = f"ELECTIVE_{options['name'].upper()}_"
        except (KeyError):
            raise ValueError("client program name is undefined")

        combine = options.get("combine", None)
        combine_options = (
            "left",
            "right",
            None,
        )

        if combine not in combine_options:
            raise ValueError(
                f"configured value for `combine` ({combine})"
                f" is not one of {combine_options}"
            )

        self.elective["combine"] = options.get("combine", None)
        self.elective["order"] = options.get("order", None)

        if "options" in options:
            self.options = {}
            for (k, v) in options["options"].items():
                self.options[k] = ElectiveConfig._process_option(v)

            # Set defaults from options.
            self._set_defaults(options["options"])

        self._configured = True

    @staticmethod
    def _merge(left, right, _debug=False):
        """Merge ``right`` into ``left``.

        Merge ``right`` dictionary into ``left`` dictionary and return ``left``.

        Parameters
        ----------
        left : dict
            Left dict.
        right : dict
            Right dict.
        _debug : bool, default=False
            Print debugging output, or not.

        Returns
        -------
        left : dict
            Dictionary resulting from merging ``right`` and ``left``.

        Raises
        ------
        ValueError
            Raises when ``left`` has a previously stored value that
            does not match the similar value in ``right`` or when a
            ``right`` value is not a dict, list, or ``State``.
        """
        # No left; return right.
        if not left:
            return copy.deepcopy(right)

        res = copy.deepcopy(left)

        # Scalars; combine right into left.
        if isinstance(right, State):
            print("merging scalars") if _debug else None

            if not isinstance(left, State):
                raise TypeError(
                    f"merge type mismatch; right is a State and left is a {type(res)}"
                )

            if (right.current is None and left.current is None) or (
                right.current is not None
            ):
                res.append(right)

            return res

        # List types; recurse on common items.
        if any(
            (
                isinstance(right, list),
                isinstance(right, tuple),
            )
        ):
            print("merging lists") if _debug else None

            if not isinstance(left, list):
                raise TypeError(
                    "merge type mismatch;"
                    " right is a list or tuple"
                    f" and left is a {type(left)}, but should be a list"
                )

            for item in right:
                res.append(copy.deepcopy(item))

            return res

        # Dicts; recurse on common key/value pairs.
        if isinstance(right, dict):
            print("merging dicts") if _debug else None

            if not isinstance(left, dict):
                raise TypeError(
                    "merge type mismatch;"
                    " right is a dict"
                    "and left is a {type(left)}, but should be a dict"
                )

            for (k, v) in right.items():
                if k in left:
                    # Exists in left; merge.
                    print("merging dict entries") if _debug else None
                    res[k] = ElectiveConfig._merge(left[k], v)
                else:
                    # Not in left; append.
                    print("appending dict entries") if _debug else None
                    res[k] = copy.deepcopy(v)

            return res

    def load_client_config(self, *args, **kwargs):
        """Load the client configuration options."""
        if not self._configured:
            raise ValueError(
                "``self.options`` is not configured.  "
                "Call ``self.load_elective_config()`` first."
            )

        argv = kwargs.pop("argv", None)

        opts = {
            "defaults": self.defaults,
        }

        # Load CLI options.
        cli = CliConfiguration(
            description=self.elective["description"],
            options=self.options,
        )
        cli.config()
        cli.load(argv=argv)
        opts["cli"] = ElectiveConfig._make_stateful(cli.options, "cli")

        # Load file options.
        file = FileConfiguration(
            order=self.elective["order"],
            fn=self.elective["name"],
        )
        file.load(section=self.elective["name"])
        for (k, v) in file.options.items():
            opts[k] = ElectiveConfig._make_stateful(v, k)

        self.config = {}

        if self.elective["combine"] is None:
            self.elective["order"].reverse()
            for source in self.elective["order"]:
                try:
                    self.config = opts[source]
                    break
                except (KeyError):
                    pass
        else:
            final = {}

            if self.elective["combine"] == "right":
                self.elective["order"].reverse()

            for source in self.elective["order"]:
                try:
                    print(opts[source])
                    if not final and opts[source]:
                        final = opts[source]
                    elif opts[source]:
                        final = ElectiveConfig._merge(final, opts[source])
                    print(final)
                except (KeyError):
                    pass

            self.config = final
