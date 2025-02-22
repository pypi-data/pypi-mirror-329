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
from typing import Optional, Union

import polars as pl
from pydantic import Field, field_validator, model_validator

from ..raw import Raw
from .timescales import get_real_calendar_between, get_std_calendar_between


class Point(Raw, extra="ignore"):
    value: int | float | str = Field(..., alias="VALUE", description='The value of the point', examples=['1'], frozen=True)


class YearlyPoint(Point):
    year: int = Field(..., alias="YEAR", description='The year of the point', examples=['2024'], frozen=True)

    @staticmethod
    def default_calendar(start: Optional[datetime], end: Optional[datetime], real: bool = False) -> pl.DataFrame:
        """
        Return a polars DataFrame with a full calendar of years from start to end
        """
        if start is None or end is None:
            raise ValueError('Start and end must be provided')
        return pl.DataFrame({'YEAR': pl.arange(start.year, end.year)})


class MonthlyPoint(Point):
    month: int = Field(..., alias="MONTH", description='The month of the point', examples=['1'], frozen=True)

    @field_validator('month')
    def validate_month(cls, v):
        if not (1 <= v <= 12):
            raise ValueError('Month must be between 1 and 12')
        return v

    @staticmethod
    def default_calendar(start: Optional[datetime], end: Optional[datetime], real: bool = False) -> pl.DataFrame:
        """
        Return a polars DataFrame with a full calendar of 12 months
        """
        return pl.DataFrame({'MONTH': pl.arange(1, 12)})


class DailyPoint(Point):
    day: int = Field(..., alias="DAY", description='The day of the point', examples=['1'], frozen=True)

    @field_validator('day')
    def validate_day(cls, v):
        if not (1 <= v <= 367):
            raise ValueError('Day must be between 1 and 367')
        return v

    @staticmethod
    def default_calendar(start: Optional[datetime], end: Optional[datetime], real: bool = False) -> pl.DataFrame:
        """
        Return a polars DataFrame with a full calendar of 366 days
        """
        return pl.DataFrame({'DAY': pl.arange(1, 366)})


class HourlyPoint(Point):
    hour: int = Field(..., alias="HOUR", description='The hour of the point', examples=['1'], frozen=True)

    @field_validator('hour')
    def validate_hour(cls, v):
        if not (1 <= v <= 24):
            raise ValueError('Hour must be between 1 and 24')
        return v

    @staticmethod
    def default_calendar(start: Optional[datetime], end: Optional[datetime], real: bool = False) -> pl.DataFrame:
        """
        Return a polars DataFrame with a full calendar of 24 hours
        """
        return pl.DataFrame({'HOUR': pl.arange(1, 24)})


class WeeklyPoint(Point):
    week: int = Field(..., alias="WEEK", description='The week of the point', examples=['1'], frozen=True)

    @field_validator('week')
    def validate_week(cls, v):
        if not (1 <= v <= 53):
            raise ValueError('Week must be between 1 and 53')
        return v

    @staticmethod
    def default_calendar(start: Optional[datetime], end: Optional[datetime], real: bool = False) -> pl.DataFrame:
        """
        Return a polars DataFrame with a full calendar of 53 weeks
        """
        return pl.DataFrame({'WEEK': pl.arange(1, 53)})


class HourlyDailyPoint(MonthlyPoint, DailyPoint, HourlyPoint):
    @model_validator(mode='before')
    def validate_hourly_daily_point(cls, v):
        if not isinstance(v, dict):
            raise ValueError('HourlyDailyPoint must be a dictionary')
        
        if 'MONTH' not in v or 'DAY' not in v or 'HOUR' not in v:
            raise ValueError('HourlyDailyPoint must contain MONTH, DAY and HOUR')
        
        try:
            datetime(2018, v['MONTH'], v['DAY'], v['HOUR'] - 1)
        except ValueError as e:
            raise ValueError(f"Invalid datetime: {e}") from e
        
        return v
    
    @staticmethod
    def default_calendar(start: Optional[datetime], end: Optional[datetime], real: bool = False) -> pl.DataFrame:
        """
        Return a polars DataFrame with a full calendar
        """
        # return a polars DataFrame with 4 columns: YEAR, MONTH, DAY, HOUR
        start_dt = start or datetime(2018, 1, 1, 0)
        end_dt = end or datetime(2018, 12, 31, 23)
        if real:
            # from start to end as datetime
            return pl.DataFrame(get_real_calendar_between(start_dt, end_dt))
        else:
            return pl.DataFrame(get_std_calendar_between(start_dt, end_dt))


PointType = Union[YearlyPoint, MonthlyPoint, DailyPoint, HourlyPoint, HourlyDailyPoint]


