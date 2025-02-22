#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ["Christophe Druet"]
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

from pathlib import Path
from typing import Optional

from loguru import logger
from pemmdb_classes import CurveTable, DataTable
from pemmdb_classes.classes import get_model_classes
from pemmdb_classes.config import DataCollectionConfig
from pemmdb_classes.cryptors import Encryptor


class DataCollection:
    """
    A data collection is a collection of tables, curves, etc.
    """
    def __init__(self, 
                 config: DataCollectionConfig,
                 encryptor: Optional[Encryptor] = None,
                 version_path: str | Path = '.'):
        logger.debug(f"Creating DataCollection for {config.nickname} version {config.version} in {version_path}")
        self.sheets = []
        self.version_path = version_path
        for item in config.sheets:
            if model_classes := get_model_classes(config.nickname, item):
                table_class = DataTable if item.sheet_type == 'table' else CurveTable
                table = table_class(pemmdb_class=model_classes.main,
                                    pemmdb_curve_cls=model_classes.point,
                                    uuid=item.uuid,
                                    encryptor=encryptor, 
                                    base_path=Path(version_path))
            else:
                table = DataTable(sheet_name=item.sheet_name,
                                  uuid=item.uuid,
                                  encryptor=encryptor, 
                                  base_path=Path(version_path))
            logger.debug(f"Adding {item.sheet_type} {table.sheet_name} to the collection (from {version_path})")
            self.sheets.append(table)

    @property
    def version(self) -> str:
        return self.version_path.name
    
    @version.setter
    def version(self, value: str):
        path = Path(self.version_path).parent / value
        if not path.is_dir():
            logger.error(f"Version path {path} does not exist")
        else:
            self.version_path = path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    # curves: List[Curve]


