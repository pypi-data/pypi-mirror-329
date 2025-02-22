#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ['Christophe Druet']
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

# Standard library imports
from pathlib import Path
from typing import Self

from loguru import logger


def dumploadable(cls):
    def dump_to(self, path: str | Path) -> Self:
        path = Path(path)
        match path.suffix.lower():
            case '.toml':
                from toml import dump
            case '.json':
                from json import dump
            case '.yaml' | '.yml':
                from yaml import dump
            case _:
                raise ValueError(f'Unsupported file extension for {path}.')

        with open(path, 'w') as f:
            dump(self.model_dump(exclude_none=True), f)

        return self

    def as_json(self) -> str:
        return self.model_dump_json(exclude_none=True)

    @classmethod
    def load_from(cls, path: str | Path) -> Self:
        path = Path(path)
        match path.suffix.lower():
            case '.toml':
                from tomllib import load
            case '.json':
                from json import load
            case '.yaml' | '.yml':
                from yaml import safe_load as load
            case _:
                raise ValueError(f'Unsupported file extension for {path}.')
            
        with open(path, 'rb') as f:
            config = load(f)
            return cls(**config)
        
    def _add_method(name, func):
        if hasattr(cls, name):
            raise AttributeError(f"Method '{name}' already exists in class '{cls.__name__}'.")
        setattr(cls, name, func)

    _add_method('dump_to', dump_to)
    _add_method('load_from', load_from)
    _add_method('as_json', as_json)

    return cls
