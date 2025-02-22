#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ['Christophe Druet']
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

# Standard library imports
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field

from .post_processing import PostProcessing


# Define a new type for skip categories
QueryType = Literal["table", "curve", "index", "class"]


class Query(BaseModel, validate_assignment=True):
    """
    A class to handle queries.
    """
    name: Optional[str] = Field(None, description="The name of the query.")
    id: Optional[str] = Field(None, description="The unique identifier for the query.")
    type: QueryType = Field(..., description="The type of the query.")
    folder: Optional[str] = Field(None, description="The folder for the query.")
    pemmdb_class: Optional[str] = Field('Raw', description="The name of the Pydantic model class associated with this query.")
    timescale: Optional[str] = Field(None, description="The timescale for the query.")
    endpoint: str = Field("dataretrieval/queries/run", exclude=True, description="The endpoint for the query.")
    post_processing: Optional[PostProcessing] = Field(None, description="The post-processing for the (sub)query.")

    @property
    def _dir(self) -> Path:
        return Path('.', self.folder) if self.folder is not None else Path('.') 

    @property
    def relpath(self) -> Path:
        if self.id is None:
            raise ValueError("Query ID cannot be None")
        return (self._dir / self.id).with_suffix('.sparql')
    
    @property
    def sheet_name(self) -> str:
        if self.name is None:
            raise ValueError("Query name cannot be None")
        return self.name
