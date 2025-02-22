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

from datetime import datetime
from typing import List, Optional, Union

import polars as pl
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from .points import PointType


curve_model_config = ConfigDict(
    # frozen=True, # Once instantiated properties cannot be changed
    extra="forbid", # Forbidden extra properties so that an error is raised when SparQL queries return extra properties
    populate_by_name=True, # Allows using either alias or field name for creation
    use_enum_values=True, # Use enum values for fields
    alias_generator = lambda field: field.upper(), # Custom alias in uppercase as this is the expected format for headers in PEMMDB CSV files
    # validate_default=True, # Validate default values as they are stored as strings in the PEMMDB model
    # hide_input_in_errors=True, # Hide input in errors as some data can be confidential
)


class Curve(BaseModel):
    """
    A curve is a collection of points
    """
    model_config = curve_model_config

    zone: str = Field(..., 
        description='The zone from which the data originates', 
        example='Belgium, BE00, BE', 
        frozen=True)
    id: Optional[str] = Field(None, 
        description='The ID of the curve', 
        example='Reserve Requirements', 
        frozen=True)
    label: str = Field(..., 
        description='The label of the curve', 
        example='FCR_BATT', 
        frozen=True)
    points: List[PointType] = Field(default_factory=list, 
        description='The points of the curve',
        frozen=True)
    
    real: bool = Field(False, 
        description='Whether the timeline follows real datetime or a standard year', 
        example='False')

    _df: Optional[pl.DataFrame] = PrivateAttr(default=None)
    _expanded_df: Optional[pl.DataFrame] = PrivateAttr(default=None)

    def as_polars(self, **kwargs) -> pl.DataFrame:
        """
        Return a polars DataFrame with the points of the curve
        """
        # Create a polars DataFrame from the points
        if self._df is None:
            self._df = pl.DataFrame([p.model_dump(by_alias=True) for p in self.points])

            # If the DataFrame has a column named 'YEARS' (list of years covered by the point), explode it into individual rows
            if 'YEARS' in self._df.columns:
                self._df = self._df.explode('YEARS').rename({'YEARS': 'YEAR'})

        # Get expand from kwargs and use it to forward fill the polars DataFrame
        expand = kwargs.pop('expand', False)

        if expand and self._expanded_df is None:
            self._expanded_df = self._df.clone()
            start_year = self._expanded_df['YEAR'].min() if 'YEAR' in self._expanded_df.columns else 2018
            end_year = self._expanded_df['YEAR'].max() if 'YEAR' in self._expanded_df.columns else 2018
            # Get a full "calendar" depending on the type of point
            calendar = self.points[0].default_calendar(datetime(start_year, 1, 1, 0), 
                                                       datetime(end_year, 12, 31, 23), 
                                                       self.real)
            self._expanded_df = self._expanded_df.select(calendar.columns + ['VALUE']).join(calendar, on=calendar.columns, how='right')
            # Filling gaps with previous value to create a time serie
            self._expanded_df = self._expanded_df.fill_null(strategy='forward')
            # Filling gaps for previous index in case the first value didn't correspond to the index start
            self._expanded_df = self._expanded_df.fill_null(strategy='backward')

        df = self._expanded_df if expand else self._df

        # Get selectors from kwargs and use them to filter data when value in a column is equal to a value in kwargs
        selectors = [k for k in kwargs.keys() if k in df.columns]
        if selectors:
            # for each selector, filter df when value in a column is equal to a value in kwargs
            for selector in selectors:
                df = df.filter(pl.col(selector) == kwargs[selector])

        return df.rename({'VALUE': self.label})
    
    def as_pandas(self, **kwargs) -> 'pandas.DataFrame':
        return self.as_polars(**kwargs).to_pandas()
