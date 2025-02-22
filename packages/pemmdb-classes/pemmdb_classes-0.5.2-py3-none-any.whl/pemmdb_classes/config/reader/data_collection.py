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

from pydantic import BaseModel, Field, computed_field, field_serializer
from pydantic.alias_generators import to_snake

from ... import version
from ...utils import dumploadable
from .sheet import SheetConfig


@dumploadable
class DataCollectionConfig(BaseModel):
    data_collection_name: str = Field(..., description="The name of the data collection.", examples=['ERAA2025-TYNDP2026_Data_Collection'])
    nickname: str = Field(..., description="The nickname of the data collection.", examples=['ERAA2025'])
    sheets: List[SheetConfig] = Field([], description="The list of available tables.")
    encrypted: bool = Field(..., description="Whether the data is encrypted.")

    def bumped_version(self, 
                       data_dir: str | Path, 
                       bump_type: Literal["major", "minor", "patch"] = "patch") -> str:
        return version.bump(self.version, bump_type)

    @property
    def versions(self) -> List[str]:
        path = Path(os.getenv('PEMMDB_STORE_DIR', './output')) / self.nickname
        if not path.is_dir():
            return []
        
        return version.sort([ d.name for d in path.iterdir() if d.is_dir() ])
    
    @property
    def version(self) -> str:
        if versions := self.versions:
            return versions[-1]
        
        return version.default()

    @property
    def is_empty(self) -> bool:
        return len(self.sheets) == 0
    