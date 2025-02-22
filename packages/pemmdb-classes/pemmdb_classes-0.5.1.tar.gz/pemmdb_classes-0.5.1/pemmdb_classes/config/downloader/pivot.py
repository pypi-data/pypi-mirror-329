#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ['Christophe Druet']
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

# Standard library imports
from typing import List, Optional, Self

from pydantic import BaseModel, Field, model_validator


class Pivot(BaseModel):
    """
    A class to handle the pivot for the queries.

    - columns: What becomes the new columns headers.
    - indexes: What remains and is used to group things together.
    - values: what values get into the new columns.
    """
    columns: Optional[List[str]] = Field(None, description="The column(s) whose values will be used as the new columns.")
    indexes: Optional[List[str]] = Field(None, description="The column(s) that remain from the input to the output.")
    values: Optional[List[str]] = Field(['VALUE'], description="The existing column(s) of values which will be moved under the new columns from index.")

    @model_validator(mode='after')
    def validate_pivot(self) -> Self:
        # At least two of the three properties must be defined
        if sum(1 for x in [self.columns, self.indexes, self.values] if x is not None) < 2:
            raise ValueError('At least two of on, indexes or values must be defined for a valid pivot.')
        return self
