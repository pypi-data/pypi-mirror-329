#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ["Christophe Druet"]
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

from pathlib import Path
import json
import pickle
import toml
import yaml

from benedict import benedict
from loguru import logger


def load_defaults(data_collection: str, sheet: str, base_path: Path = Path(".")) -> dict:
    """Load defaults from a configuration file."""
    dir_path = base_path / data_collection
    
    for ext in ['json', 'yaml', 'toml', 'pickle']:
        file_path = dir_path / f"{sheet}.{ext}"
        if file_path.is_file():
            if ext == 'pickle':
                with open(file_path, 'rb') as f:
                    return pickle.load(f)
            else:
                with open(file_path, 'r') as f:
                    if ext == 'json':
                        return json.load(f)
                    elif ext == 'yaml':
                        return yaml.safe_load(f)
                    elif ext == 'toml':
                        return toml.load(f)
    
    if sheet.endswith('_text'):
        raise ValueError('Invalid format: txt')
    return {}
