#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ['Christophe Druet']
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

# Standard library imports
from pathlib import Path
from typing import Literal, Optional, Self

from pydantic import BaseModel, Field, field_validator, model_validator

from ...utils.dumploadable import dumploadable
from .data_collection import DataCollection


@dumploadable
class DownloaderConfig(BaseModel, validate_assignment=True):
    """
    A class to handle the queries configuration for the PEMMDB client.
    """
    base_url: str = Field(..., description="The server to connect to.")
    server_type: Literal["pemmdb", "fuseki"] = Field(..., description="The type of server (pemmdb or fuseki).")
    credentials: bool = Field(True, description="Indicates if credentials are required to connect to the server.")
    queries_dir: Optional[str] = Field(None, description="The path to the PEMMDB model where the queries (as SPARQL files) should be stored.")
    classes_dir: Optional[str] = Field(None, description="The relative path to the directory containing the classes if local.")
    classes_modules: Optional[str] = Field(None, description="The module containing the classes if local.")
    default_data_path: Optional[str] = Field(None, description="The path to the default data to fill gaps if required.")
    
    data_collection: DataCollection = Field(..., description="The data collection.")
    
    @field_validator('queries_dir')
    def validate_queries_dir(cls, value) -> str:
        if value is not None:
            path = Path(value)
            if not path.is_relative_to('.'):
                raise ValueError('queries_dir must be a relative path.')
        return value

    @field_validator('classes_dir')
    def validate_classes_dir(cls, value) -> str:
        if value is not None:
            path = Path(value)
            if not path.is_relative_to('.'):
                raise ValueError('classes_dir must be a relative path.')
        return value

    @field_validator('default_data_path')
    def validate_default_data_path(cls, value) -> str:
        if value is not None:
            path = Path(value)
            if not path.is_relative_to('.'):
                raise ValueError('default_data_path must be a relative path.')
            if not path.exists():
                raise FileNotFoundError(f'default_data_path "{path.resolve()}" does not exist.')
        return value

    @model_validator(mode='after')
    def verify_queries_dir_is_set_if_fuseki(self) -> Self:
        if self.server_type == 'fuseki':
            if self.queries_dir is None:
                raise ValueError('queries_dir must be defined when server_type is "fuseki".')
            
            dir_path = Path(self.queries_dir)

            if self.data_collection.queries and not dir_path.exists():
                raise FileNotFoundError(f'queries_dir "{dir_path.resolve()}" does not exist.')

            missing_files = [
                query.relpath for query in self.data_collection.queries
                if not (dir_path / query.relpath).exists()
            ]
            
            if missing_files:
                raise FileNotFoundError("The following subquery files are missing:\n" +
                                        "\n".join(str(dir_path / file) for file in missing_files))
            
        return self
