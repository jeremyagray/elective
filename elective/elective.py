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

from .cli import CliLoader
from .exceptions import ElectiveFileLoadingError
from .files import load_bespon_file
from .files import load_json_file
from .files import load_toml_file
from .files import load_yaml_file


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

    def __str__(self):
        """Stringify an ``ElectiveConfig`` object."""
        pass

    def __repr__(self):
        """Reproduce an ``ElectiveConfig`` object."""
        pass

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

    def load_elective_config(self, fn):
        """Load configuration data."""
        options = load_toml_file(fn, section="elective")

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

    def merge(self, config):
        """Merge ``self`` and ``config`` configuration options.

        Merge the configuration options in ``self`` and ``config``
        according to the current elective configuration.

        Merging direction is configurable.  A left merge will update
        values in ``self``.  A right merge will update values in
        ``config`` and then copy those values into ``self``.  If no
        merge is selected, then ``config`` will replace the options in
        ``self``.

        Parameters
        ----------
        self : object
            The current configuration object.
        config : dict
            A dictionary containing configuration options.
        """
        if self.elective["combine"] == "left":
            self._left_merge(config)
        elif self.elective["combine"] == "right":
            self._right_merge(config)
        elif self.elective["combine"] is None:
            self._set_options(config)

    @staticmethod
    def _merge(left, right):
        """Merge ``right`` into ``left``."""
        for (k, v) in right.items():
            if isinstance(v, dict):
                if left[k]:
                    left[k] = ElectiveConfig._merge(left[k], v)
                else:
                    left[k] = v
            else:
                left[k] = v

        return left

    def _left_merge(self, config):
        """Left merge ``self`` and ``config`` configuration options."""
        self.options = ElectiveConfig._merge(self.options, config)

    def _right_merge(self, config):
        """Right merge ``self`` and ``config`` configuration options."""
        self.options = ElectiveConfig._merge(config, self.options)

    @staticmethod
    def _mask_options(defaults, options):
        """Mask ``options`` with the defaults."""
        new = {}
        for (k, v) in defaults.items():
            new[k] = options.get(k, defaults[k])

        return new

    def _set_options(self, options):
        """Set ``options`` as the configuration options."""
        self.options = ElectiveConfig._mask_options(options)

    def _load_cli_options(self):
        """Load CLI options."""
        cli = CliLoader()
        cli.config(self)
        cli.load()
        return cli.options

    def _load_toml_options(self):
        """Load TOML options."""
        try:
            opts = ElectiveConfig._mask_options(
                load_toml_file("./.{self.elective['name']}.{file}")
            )
        except:  # noqa: E722
            opts = {}

        return opts

    def _load_json_options(self):
        """Load JSON options."""
        try:
            opts = ElectiveConfig._mask_options(
                load_json_file("./.{self.elective['name']}.{file}")
            )
        except:  # noqa: E722
            opts = {}

        return opts

    def _load_yaml_options(self):
        """Load YAML options."""
        try:
            opts = ElectiveConfig._mask_options(
                load_yaml_file("./.{self.elective['name']}.{file}")
            )
        except:  # noqa: E722
            opts = {}

        return opts

    def _load_bespon_options(self):
        """Load BespON options."""
        try:
            opts = ElectiveConfig._mask_options(
                load_bespon_file("./.{self.elective['name']}.{file}")
            )
        except:  # noqa: E722
            opts = {}

        return opts

    def _load_file_options(self, file):
        """Load file options."""
        try:
            opts = ElectiveConfig._mask_options(
                load_bespon_file("./.{self.elective['name']}.{file}")
            )
        except (ElectiveFileLoadingError) as error:
            print(error)
            opts = {}

        return opts

    def load_client_config(self):
        """Load the client configuration options."""
        if not self._configured:
            raise ValueError(
                "``self.options`` is not configured.  "
                "Call ``self.load_elective_config()`` first."
            )

        loaders = {
            "cli": self._load_cli_options,
            "toml": self._load_toml_options,
            "json": self._load_json_options,
            "yaml": self._load_yaml_options,
            "bespon": self._load_bespon_options,
        }

        opts = {
            "defaults": self.defaults,
            "cli": self._load_cli_options(),
        }

        for loader in ["toml", "json", "yaml", "bespon"]:
            opts[loader] = loaders[loader]()

        self.config = {}

        if self.elective["combine"] is None:
            for source in self.elective["order"].reverse():
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
                    if not final and opts[source]:
                        final = opts[source]
                    elif opts[source]:
                        final = ElectiveConfig._merge(final, opts[source])
                except (KeyError):
                    pass

            self.config = final
