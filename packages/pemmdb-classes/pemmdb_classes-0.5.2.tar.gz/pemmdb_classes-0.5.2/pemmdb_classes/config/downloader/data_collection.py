#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ['Christophe Druet']
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

# Standard library imports
from typing import List, Optional

import pendulum
from pydantic import BaseModel, Field, field_validator

from .query import Query


class DataCollection(BaseModel, validate_assignment=True):
    """
    A class to handle the data collection.
    """
    name: str = Field(..., description="The name of the data collection.")
    nickname: Optional[str] = Field(None, description="The nickname of the data collection.")
    timestamp: Optional[str] = Field(pendulum.now("Europe/Brussels").to_iso8601_string(), description="A timestamp for the data collection.")
    queries: List[Query] = Field([], description="The list of queries in the data collection.")

    def __str__(self) -> str:
        text = f'{self.name} ({self.timestamp})'
        for query in self.queries:
            text += f'\n - {str(query)}'
        return text

    @field_validator('queries')
    def validate_queries(cls, value) -> List[Query]:
        queries = { query.id: query for query in value } # so that the last query with the same id overwrites the previous one
        return sorted(list(queries.values()), key=lambda x: x.id)
