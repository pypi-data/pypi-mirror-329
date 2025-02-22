#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ["Christophe Druet"]
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from .utils import clean_string


raw_model_config = ConfigDict(
    frozen=True, # Once instantiated properties cannot be changed
    extra="allow", # Forbidden extra properties so that an error is raised when SparQL queries return extra properties
    populate_by_name=True, # Allows using either alias or field name for creation
    use_enum_values=True, # Use enum values for fields
    alias_generator = lambda field: field.upper(), # Custom alias in uppercase as this is the expected format for headers in PEMMDB CSV files
    validate_default=True, # Validate default values as they are stored as strings in the PEMMDB model
    hide_input_in_errors=True, # Hide input in errors as some data can be confidential
)


class Raw(BaseModel):
    """
    The base class for all data to be collected.
    """
    model_config = raw_model_config

    __data_collection__ = "Unspecified"
    __sheet_name__ = "Raw data"
    __query_id__ = "unknown"
    __filename__ = "unknown"

    @classmethod
    def data_collection(cls) -> str:
        return cls.__data_collection__

    @classmethod
    def sheet_name(cls) -> str:
        return cls.__sheet_name__
    
    @classmethod
    def file_uuid(cls) -> str:
        return cls.__filename__

    @model_validator(mode='before')
    def clean_strings(cls, values):
        """
        Clean strings from unwanted characters like '–' (instead of '-')
        """
        for k, v in values.items():
            if isinstance(v, str):
                values[k] = clean_string(v)
        
        return values
