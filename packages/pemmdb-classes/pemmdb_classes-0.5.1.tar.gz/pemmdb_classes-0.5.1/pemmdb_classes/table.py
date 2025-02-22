#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ["Christophe Druet"]
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

import csv
import json
from pathlib import Path
from pprint import pformat
from typing import Generator, List, Optional, Self

import polars as pl
from loguru import logger
from pemmdb_classes import Raw
from pydantic import BaseModel


class Table:
    def __init__(self, **kwargs):
        """
        Initialize the DataTable with a Pydantic model class and an optional encryptor.

        Args:
            cls (BaseModel): A Pydantic model class that defines the structure of the data.
            encryptor (Optional[Encryptor]): An optional Encryptor instance for decrypting data.
        """
        self.cls = kwargs.get('pemmdb_class', None)
        if self.cls is None:
            logger.info('No pemmdb_class provided. Raw processing.')

        self.sheet_name = kwargs.get('sheet_name', None) or self.cls.sheet_name()
        self.uuid = kwargs.get('uuid', None) or self.cls.file_uuid()

        self.encryptor = kwargs.get('encryptor', None)
        base_path = Path(kwargs.get('base_path', '.'))

        if not base_path.is_dir():
            raise FileNotFoundError(f"Base path {base_path} does not exist.")
        
        data_file_path = (base_path / self.uuid).with_suffix('.pemmdb' if self.encryptor is not None else '.csv')
        if not data_file_path.is_file():
            raise FileNotFoundError(f"File {data_file_path} does not exist.")
        
        self.file_path = data_file_path

    def set_cls(self, cls: BaseModel) -> Self:
        self.cls = cls
        return self

    def headers(self) -> List[str]:
        """
        Get the headers of the table.
        """
        if self.cls is not None:
            return [field.alias for _name, field in self.cls.model_fields.items() if field.alias]
        else:
            logger.debug(f"Getting headers for {self.sheet_name} from {self.file_path}")
            with self.file_path.open('r', encoding='utf-8') as file:
                if self.encryptor is None:
                    reader = csv.DictReader(file)
                    return reader.fieldnames
                else:
                    first_row = file.readline()
                    decrypted = self.encryptor.decrypt(first_row.strip())
                    return list(decrypted.keys())

    def iter_rows(self, with_class: BaseModel | None = None) -> Generator[BaseModel, None, None]:
        """
        Generator to iterate over the rows of the table.

        Yields:
            BaseModel: An instance of the Pydantic model populated with data from the CSV or decrypted data.
        """
        logger.debug(f'Iterating over data for {self.sheet_name} from {self.file_path}...')
        model_class = with_class or self.cls or Raw
        with self.file_path.open('r', encoding='utf-8') as file:
            if self.encryptor is None:
                reader = csv.reader(file)
                i = 0
                for row in reader:
                    i += 1
                    # logger.debug(f"Unencrypted row {i}: {row}")
                    yield i, model_class.model_construct(**row)
            else:
                i = 0
                for row in file:
                    i += 1
                    # logger.debug(f"Encrypted row #{i}: {row}")
                    decrypted = self.encryptor.decrypt(row.strip())
                    # logger.debug(f"Decrypted row #{i}: {decrypted}")
                    instance = model_class.model_construct(**decrypted)
                    # logger.debug(f"Instance #{i}: {instance}")
                    yield i, instance

    def write_csv(self, path: Path, **kwargs):
        """
        Write the table to a CSV file.

        Args:
            path (Path): The path where the CSV file will be written.
            **kwargs: Additional keyword arguments to pass to the Polars DataFrame.
        """
        logger.debug(f"Treating {self.sheet_name} as a table")
        with path.with_suffix('.csv').open('w', newline='', encoding='utf-8') as file:
            logger.debug(f"Writing CSV file to {path.with_suffix('.csv')}")
            try:
                fieldnames = self.headers()
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
                writer.writeheader()

                for _, row in self.iter_rows():
                    writer.writerow(row.model_dump(by_alias=True))

            except ValueError as e:
                logger.error(e)
            logger.debug(f"CSV file written to {path.with_suffix('.csv')}")

    def as_polars(self, **kwargs) -> pl.DataFrame:
        """
        Return the table as a Polars DataFrame.

        Returns:
            pl.DataFrame: A Polars DataFrame containing the data from the table.
        """
        if self.cls is not None:
            return pl.DataFrame([row.model_dump(by_alias=True, exclude_none=True) for _, row in self.iter_rows()])
        else:
            return pl.DataFrame([row.model_dump(by_alias=True, exclude_none=True) for _, row in self.iter_rows()])
    
    def as_pandas(self, **kwargs) -> "pandas.DataFrame":  # type: ignore # noqa: F821
        """
        Return the table as a Pandas DataFrame.

        Returns:
            pandas.DataFrame: A Pandas DataFrame containing the data from the table.
        """
        return self.as_polars(**kwargs).to_pandas()
    
    def write_json(self, path: Path, **kwargs):
        self.as_polars(**kwargs).write_json(path)


class DataTable(Table):
    pass
