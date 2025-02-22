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

from datetime import datetime, timedelta
from functools import partial
from typing import List, Tuple

import polars as pl


def iterate_hours(start: datetime, delta: timedelta, end: datetime):
    """
    Generate all hours between start and end (inclusive of start, exclusive of end).
    """
    current = start
    while current <= end:
        yield current
        current += delta


def get_real_dt_as_dict(dt: datetime):
    return {'YEAR': dt.year, 'MONTH': dt.month, 'DAY': dt.day, 'HOUR': dt.hour+1}


def get_std_dt_as_dict(dt: datetime, year: int):
    return {'YEAR': year, 'MONTH': dt.month, 'DAY': dt.day, 'HOUR': dt.hour+1}


def get_calendar_between(start: datetime, end: datetime, year: int | None = None):
    if year is None:
        return [get_real_dt_as_dict(dt) for dt in iterate_hours(start, timedelta(hours=1), end)]
    else:
        return [get_std_dt_as_dict(dt, year) for dt in iterate_hours(start, timedelta(hours=1), end)]


get_real_calendar_between = partial(get_calendar_between, year=None)


def get_std_calendar_between(start: datetime, end: datetime):
    calendar = []
    for year in range(start.year, end.year+1):
        calendar.extend(get_calendar_between(datetime(2018, 1, 1, 0), datetime(2018, 12, 31, 23), year))
    return calendar


def get_index_for_timescale(timescale: str) -> Tuple[str]:
    match timescale:
        case 'Yearly':
            return ('YEAR',)
        case 'Monthly':
            return ('MONTH',)
        case 'Weekly':
            return ('WEEK',)
        case 'Daily':
            return ('DAY',)
        case 'HourlyDaily':
            return ('MONTH', 'DAY', 'HOUR')
        case _:
            raise ValueError(f"Invalid timescale: {timescale} to get index")


def get_calendar_for_timescale(timescale: str, **kwargs) -> pl.DataFrame:
    match timescale:
        case 'Yearly':
            # return a dataframe with a single column 'YEAR' from start_year to end_year
            start_year = kwargs.get('start_year', 2000)
            end_year = kwargs.get('end_year', 2050) + 1
            return pl.DataFrame({'YEAR': range(start_year, end_year)})
        case 'Monthly':
            # return a dataframe with a single column 'MONTH' from start_year to end_year
            return pl.DataFrame({'MONTH': range(1, 13)})
        case 'Weekly':
            # return a dataframe with a single column 'WEEK' from start_year to end_year
            return pl.DataFrame({'WEEK': range(1, 54)})
        case 'Daily':
            # return a dataframe with a single column 'DAY' from start_year to end_year
            return pl.DataFrame({'DAY': range(1, 366)})
        case 'HourlyDaily':
            # return a dataframe with a calendar based on 2018
            return pl.DataFrame(get_calendar_between(datetime(2018, 1, 1, 0), datetime(2018, 12, 31, 23))).drop(['YEAR'])
        case _:
            raise ValueError(f"Invalid timescale: {timescale} to get calendar")

