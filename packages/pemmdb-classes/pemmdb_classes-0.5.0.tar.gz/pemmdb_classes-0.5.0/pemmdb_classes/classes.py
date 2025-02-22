#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ["Christophe Druet"]
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

import importlib
from collections import namedtuple
from typing import Optional

from loguru import logger  # noqa I001
from pydantic.alias_generators import to_snake


ModelClasses = namedtuple('ModelClasses', ['main', 'raw', 'point'])


def get_model_classes(data_collection_nickname: str, config) -> Optional[ModelClasses]:
    """
    Retrieve model classes based on the provided configuration.

    :param config: The configuration object containing class information.
    :type config: Query
    :param target: The target type of model class to retrieve ('raw' or 'point').
    :type target: Literal['raw', 'point']
    :return: An instance of ModelClasses containing the requested classes.
    :rtype: ModelClasses
    :raises ImportError: If the specified module cannot be imported.
    :raises AttributeError: If the specified class does not exist in the module.
    """
    # convert the class name to a module name, from CamelCase to snake_case
    root_module_name = f'pemmdb_model_{data_collection_nickname.lower()}'
    logger.debug(f"Importing classes from {root_module_name}")

    if config.pemmdb_class is not None:
        try:
            module_name = to_snake(config.pemmdb_class)
            logger.debug(f"Importing class {module_name} from {root_module_name}")

            # import the module
            module = importlib.import_module(f'{root_module_name}.classes.{module_name}')
            return ModelClasses(
                main=getattr(module, config.pemmdb_class),
                raw=getattr(module, f'Raw{config.pemmdb_class}', None),
                point=getattr(module, f'{config.pemmdb_class}Point', None)
            )
        except ImportError as e:
            logger.error(f"Error importing class {module_name} from {root_module_name}: {e}")
            pass

    return None