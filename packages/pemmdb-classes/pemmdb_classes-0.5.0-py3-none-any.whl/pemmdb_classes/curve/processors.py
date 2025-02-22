#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-YYYY ENTSO-E - All rights reserved."
__credits__ = ['Christophe Druet']
__license__ = "MIT"
__version__ = "0.2.2"
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"
__status__ = "Dev"

import time
from functools import wraps
from typing import Optional

import polars as pl
from loguru import logger

from .timescales import get_calendar_for_timescale, get_index_for_timescale


# Decorator to log the execution of the methods


# Decorator to catch exceptions raised by the methods
def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise e
    return wrapper


# Decorator to log method execution
def log_method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.debug(f"Launching method: {func.__name__}")
        # logger.debug(args[0])
        result = func(*args, **kwargs)
        # logger.debug(f'Result of {func.__name__}: {result}')
        execution_time = time.time() - start_time
        logger.debug(f"Method {func.__name__} completed successfully in {execution_time:.4f} seconds.")
        return result
    return wrapper


@log_method
@exception_handler
def pivot(df: pl.DataFrame, timescale: str) -> pl.DataFrame:
    """
    Pivot the curve table based on CURVE_UID and the specified timescale. The result is a table
    with one column for each CURVE_UID. Can contains lots of empty cells depending on the original
    data.

    Args:
        df (pl.DataFrame): The input DataFrame containing curve data.
        timescale (str): The timescale to pivot the data on.

    Returns:
        pl.DataFrame: A pivoted DataFrame sorted by the specified index.
    """
    index = list(get_index_for_timescale(timescale))

    if df.unique('LABEL').shape[0] > 1:
        df = df.with_columns((pl.col('CURVE_UID') + ':' + pl.col('LABEL')).alias('CURVE_UID'))
    
    return df.pivot("CURVE_UID", index=index, values='VALUE').sort(index)


@log_method
@exception_handler
def fill_missing_values(df: pl.DataFrame, timescale: Optional[str] = None) -> pl.DataFrame:
    """
    Fill missing values in the curve table using forward and backward fill strategies. The result
    is a table with no missing values. The table is sorted by the specified index. If the index is
    representing a time series. There can be gaps depending on what was in the index.

    Args:
        df (pl.DataFrame): The input DataFrame containing curve data.
        timescale (Optional[str]): The timescale to consider for sorting (default is None).

    Returns:
        pl.DataFrame: A DataFrame with missing values filled.
    """
    sorted_df = df.clone()
    if timescale and 'CURVE_UID' in df.columns:
        index = ['CURVE_UID'] + list(get_index_for_timescale(timescale))
        sorted_df = sorted_df.sort(index)

    return sorted_df.fill_null(strategy='forward').fill_null(strategy='backward')

@log_method
@exception_handler
def merge_calendar(df: pl.DataFrame, timescale: str) -> pl.DataFrame:
    """
    Merge the calendar data with the curve table based on the specified timescale. The result is
    a table with the full time series. There can be gaps depending on what was in the original data.

    Args:
        df (pl.DataFrame): The input DataFrame containing curve data.
        timescale (str): The timescale to merge the calendar data on.

    Returns:
        pl.DataFrame: A DataFrame with the calendar data merged.
    """
    calendar = get_calendar_for_timescale(timescale)

    return calendar.join(df, on=list(get_index_for_timescale(timescale)), how='left')


@log_method
def synchronize(df: pl.DataFrame, timescale: str) -> pl.DataFrame:
    """
    Synchronize the curve table by filling missing values after pivoting. The result is a table
    with no missing values. The table is sorted by the specified index. If the index is
    representing a time series, there can be gaps depending on what was in the original data.

    Args:
        df (pl.DataFrame): The input DataFrame containing curve data.
        timescale (str): The timescale to synchronize the data on.

    Returns:
        pl.DataFrame: A synchronized DataFrame with missing values filled.
    """
    return fill_missing_values(pivot(df, timescale), timescale)


@log_method
def expand(df: pl.DataFrame, timescale: str) -> pl.DataFrame:
    """
    Expand the curve table by merging calendar data and filling missing values. The result is a
    table with the full time series with no missing values.

    Args:
        df (pl.DataFrame): The input DataFrame containing curve data.
        timescale (str): The timescale to expand the data on.

    Returns:
        pl.DataFrame: An expanded DataFrame with calendar data merged and missing values filled.
    """
    return fill_missing_values(merge_calendar(pivot(df, timescale), timescale), timescale)


@log_method
@exception_handler
def index(df: pl.DataFrame) -> pl.DataFrame:
    """
    Create an index for the curve table by counting occurrences of each unique combination of columns.

    Args:
        df (pl.DataFrame): The input DataFrame containing curve data.

    Returns:
        pl.DataFrame: A DataFrame with the count of occurrences for each unique combination of columns.
    """
    index_columns = [col for col in df.columns if col not in ['VALUE', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'WEEK'] ]

    if df.unique('LABEL').shape[0] > 1:
        df = df.with_columns((pl.col('CURVE_UID') + ':' + pl.col('LABEL')).alias('CURVE_UID'))

    indexed_df = df.group_by(index_columns).agg(pl.col("VALUE").count().alias('COUNT'))
    return indexed_df.sort('CURVE_UID')
