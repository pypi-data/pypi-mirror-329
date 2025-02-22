#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ["Christophe Druet"]
__license__ = "Proprietary"
__version__ = "0.2.2"
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"
__status__ = "Dev"

from pathlib import Path

import ijson
import polars as pl
from loguru import logger
from pemmdb_classes.table import Table
from pydantic import BaseModel

from .processors import expand, index, pivot, synchronize


class CurveTable(Table):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)
        
        self.pemmdb_curve_cls = kwargs.get('pemmdb_curve_cls', None)
        if self.pemmdb_curve_cls is None:
            raise ValueError("A curve class is required to instantiate a CurveTable")
        
        structured_file_path = self.file_path.parent / 'structured' / self.file_path.name
        structured_file_path = structured_file_path.with_suffix('.pemmdb' if self.encryptor else '.json')
        self.structured_file_path = structured_file_path if structured_file_path.is_file() else None

    def iter_curves(self, with_class: BaseModel | None = None):
        """
        Generator to iterate over the curves.

        Yields:
            BaseModel: An instance of the Pydantic model populated with data from the CSV or decrypted data.
        """
        model_class = with_class or self.pemmdb_curve_cls

        if self.structured_file_path is None:
            raise FileNotFoundError(f"File {self.structured_file_path} does not exist")
        
        if self.encryptor is None:
            # Use ijson module to parse the JSON file one line at a time
            with self.structured_file_path.open('r', encoding='utf-8') as file:
                i = 0
                for curve in ijson.items(file, 'item'):
                    i += 1
                    yield i, model_class(**curve)
        else:
            with self.structured_file_path.open('rb') as file:
                i = 0
                for row in file:
                    i += 1
                    decrypted = self.encryptor.decrypt(row.strip())
                    yield i, model_class(**decrypted)

    def as_polars(self, **kwargs) -> pl.DataFrame:
        logger.debug(f"Getting a dataframe for curve table {self.sheet_name}")
        df = super().as_polars()

        if df.is_empty():
            logger.warning(f"Curve table {self.sheet_name} is empty")
            return df

        if kwargs.get('index', False):
            return index(df)

        mode = kwargs.get('mode', 'raw')
        if mode not in ['raw', 'pivot', 'synchronize', 'expand']:
            logger.warning(f"Unknown mode: {mode} for processing curve table {self.sheet_name}. Using 'raw' mode.")
            mode = 'raw'

        logger.debug(f"Getting a dataframe for curve table {self.sheet_name} in mode {mode}")

        match mode:
            case 'pivot':
                return pivot(df, self.cls.__timescale__)
            case 'synchronize':
                return synchronize(df, self.cls.__timescale__)
            case 'expand':
                return expand(df, self.cls.__timescale__)
            case _:
                return df

    def write_csv(self, path: Path, **kwargs):
        """
        Write the table to a CSV file.

        Args:
            path (Path): The path where the CSV file will be written.
            **kwargs: Additional keyword arguments to pass to the Polars DataFrame.
        """
        mode = kwargs.get('mode', 'raw')
        if mode not in ['raw', 'pivot', 'synchronize', 'expand']:
            logger.warning(f"Unknown mode: {mode} for processing curve table {self.sheet_name}. Using 'raw' mode.")
            mode = 'raw'

        logger.debug(f"Writing curve table {self.sheet_name} to {path} in mode {mode}")

        match mode:
            case 'raw':
                logger.debug(f"Writing raw curve table {self.sheet_name} to {path}")
                super().write_csv(path)
            case 'pivot':
                logger.debug(f"Pivoting {self.sheet_name}")
                self.as_polars(mode='pivot').write_csv(path)
            case 'synchronize':
                logger.debug(f"Synchronizing {self.sheet_name}")
                self.as_polars(mode='synchronize').write_csv(path)
            case 'expand':
                logger.debug(f"Expanding {self.sheet_name}")
                self.as_polars(mode='expand').write_csv(path)

        if kwargs.get('index', False):
            logger.debug(f"Indexing {self.sheet_name}")
            ipath = path.with_stem(f'{path.stem} Index')
            self.as_polars(index=True).write_csv(ipath)
