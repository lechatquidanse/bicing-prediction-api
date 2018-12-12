import datetime

from pandas import DatetimeIndex
from assertpy import assert_that

class ByDateTimeInPeriodFilter:
    def __init__(self,period_date_start: datetime, period_date_end: datetime, frequency: str):
        self._validate(period_date_start, period_date_end, frequency)

        self._period_date_start = period_date_start
        self._period_date_end = period_date_end
        self._frequency = frequency

    def to_date_time_index(self):
        return DatetimeIndex(start=self._period_date_start, end=self._period_date_end, freq=self._frequency)

    @staticmethod
    def _validate(period_date_start: datetime, period_date_end: datetime, frequency: str):
        assert_that(period_date_end).is_after(period_date_start)
