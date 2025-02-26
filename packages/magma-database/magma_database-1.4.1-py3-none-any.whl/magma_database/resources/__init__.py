#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from importlib_resources import files

volcanoes_df = pd.read_excel(files("magma_database.resources").joinpath('volcanoes.xlsx'))

channels_df = pd.read_excel(files("magma_database.resources").joinpath('channels.xlsx'))
