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

import os
from pathlib import Path
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, computed_field
from pydantic.alias_generators import to_snake


class SheetConfig(BaseModel):
    sheet_name: str = Field(..., description="The name of the sheet in the Excel file.")
    sheet_type: Literal['table', 'curve'] = Field(..., description="The type of the table.")
    pemmdb_class: Optional[str] = Field('Raw', description="The name of the Pydantic model class to use to parse the data.")
    uuid: str = Field(..., description="The UUID of the file containing the data.")
    encrypted: bool = Field(..., description="Whether the data is encrypted.")

    @computed_field(description="The name of the Python file containing the Pydantic model class.")
    def class_filename(self) -> str:
        return f'{to_snake(self.pemmdb_class)}.py'
