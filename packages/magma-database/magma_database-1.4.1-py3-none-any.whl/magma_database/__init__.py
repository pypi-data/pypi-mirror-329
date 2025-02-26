#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .config import Config, config
from .models.volcano import Volcano
from .models.station import Station
from .models.sds import Sds
from .models.winston_scnl import WinstonSCNL
from .models.rsam_csv import RsamCSV
from .models.mounts import MountsSO2, MountsThermal
from pkg_resources import get_distribution

__version__ = get_distribution("magma-database").version
__author__ = "Martanto"
__author_email__ = "martanto@live.COM"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024, MAGMA Indonesia"
__url__ = "https://github.com/martanto/magma-database"

__all__ = [
    "Volcano",
    "Station",
    "Sds",
    "WinstonSCNL",
    "RsamCSV",
    "MountsSO2",
    "MountsThermal",
    "Config",
    "config",
]
