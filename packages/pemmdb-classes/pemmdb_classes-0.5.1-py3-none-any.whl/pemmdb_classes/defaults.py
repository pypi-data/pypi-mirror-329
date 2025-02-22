#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ["Christophe Druet"]
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

from pathlib import Path
from typing import Any, Dict

from benedict import benedict
from loguru import logger


def load_defaults(data_collection: str, sheet: str) -> benedict:
    """
    Load default settings from a specified file.

    This function attempts to load a defaults file from the given path. 
    If the file does not have a suffix, it will check for the existence 
    of files with common configuration file extensions (.yaml, .yml, 
    .pickle, .toml, .json) and use the first one found.

    Args:
        data_collection (str): The name of the data collection.
        sheet (str): The name of the sheet (e.g. 'thermal', 'dsr_derating')

    Returns:
        benedict: A benedict object containing the loaded defaults.

    Raises:
        FileNotFoundError: If no defaults file is found
        ValueError: if the file extension is unsupported.
    """
    # Use glob to find a file data_collection.* taking the first one found
    dir_path = Path('defaults') / data_collection
    path = next(dir_path.glob(f'{sheet}.*', case_sensitive=True), None)
    if not path:
        logger.warning(f'No defaults for {sheet} in {data_collection}.')
        return benedict()
    else:
        logger.debug(f'Loading defaults file: {path}')
        return benedict(path, format=path.suffix[1:])
