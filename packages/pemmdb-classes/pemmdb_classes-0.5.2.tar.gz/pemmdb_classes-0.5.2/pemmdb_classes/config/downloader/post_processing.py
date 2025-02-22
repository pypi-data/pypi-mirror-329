#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ['Christophe Druet']
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

# Standard library imports
from typing import List, Optional

from pydantic import BaseModel, Field

from .pivot import Pivot


class PostProcessing(BaseModel):
    """
    A class to handle the post-processing for the queries.
    """
    drop_columns: Optional[List[str]] = Field(None, description="The columns to drop for the query.")
    pivot: Optional[Pivot] = Field(None, description="The pivot for the query.")
