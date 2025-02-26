#!/usr/bin/env python3

"""The main configuration class."""

import configparser
import pathlib
import typing

from cutcutcodec.core.colorspace.cst import PRIMARIES, TRC
from cutcutcodec.utils import MetaSingleton


class Config(metaclass=MetaSingleton):
    """Contains all the cutcutcodec configuration parameters.

    Attributes
    ----------
    target_prim : str
        The terminal color primaries.
    target_trc : str
        The terminal color transfere function.
    working_prim : str
        The working space color primaries.

    Examples
    --------
    >>> import pathlib, tempfile
    >>> from cutcutcodec.config.config import Config
    >>> file = pathlib.Path(tempfile.gettempdir()) / "cutcutcodec.ini"
    >>> with open(file, "w") as raw:
    ...     _ = raw.write(
    ...         '''
    ...         [colorspace]
    ...         target-prim = bt2020
    ...         target-trc = smpte2084
    ...         working-prim = bt2020
    ...         '''
    ...     )
    >>> Config(file).working_prim
    'bt2020'
    >>> file.unlink()
    >>>
    """

    def __init__(
        self,
        config_file: typing.Union[str, bytes, pathlib.Path] = "~/.config/cutcutcodec/conf.ini"
    ):
        """Initialise the configuration from the file.

        Parameters
        ----------
        config_file : pathlike, default=~/.config/cutcutcodec/conf.ini
            The configuration file.
        """
        self._config = configparser.ConfigParser()
        self._config["colorspace"] = {  # default values
            "target-prim": "bt709",
            "target-trc": "srgb",
            "working-prim": "bt709",
        }
        config_file = pathlib.Path(config_file).expanduser().resolve()
        if config_file.is_file():
            self._config.read(config_file)

    @property
    def target_prim(self) -> str:
        """Return the terminal color primaries."""
        return self._config["colorspace"]["target-prim"]

    @target_prim.setter
    def target_prim(self, new: str):
        assert isinstance(new, str), new.__class__.__name__
        assert new in PRIMARIES, f"{new} not in {sorted(PRIMARIES)}"
        self._config["colorspace"]["target-prim"] = new

    @property
    def target_trc(self) -> str:
        """Return the terminal color transfere function."""
        return self._config["colorspace"]["target-trc"]

    @target_trc.setter
    def target_trc(self, new: str):
        assert isinstance(new, str), new.__class__.__name__
        assert new in TRC, f"{new} not in {sorted(TRC)}"
        self._config["colorspace"]["target-trc"] = new

    @property
    def working_prim(self) -> str:
        """Return the working space color primaries."""
        return self._config["colorspace"]["working-prim"]

    @working_prim.setter
    def working_prim(self, new: str):
        assert isinstance(new, str), new.__class__.__name__
        assert new in PRIMARIES, f"{new} not in {sorted(PRIMARIES)}"
        self._config["colorspace"]["working-prim"] = new
