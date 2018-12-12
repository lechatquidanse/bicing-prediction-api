"""
Convert a value from a flask request to python ByDateTimeInPeriodFilterConverter object
"""
from datetime import datetime

from application.use_case.filter.ByDateTimeInPeriodFilter import ByDateTimeInPeriodFilter


class ByDateTimeInPeriodFilterConverter:
    QUERY_SEPARATOR = ','

    def to_python(self, value: str) -> ByDateTimeInPeriodFilter:
        if value is None:
            raise ValueError(
                'No filter query provided (for example filter=2018-02-12%2023:34:21,2018-08-12%2023:34:21,5T)')

        values = value.split(self.QUERY_SEPARATOR)

        if len(values) != 3:
            raise ValueError(
                'Filter is not well formatted (for example filter=2018-02-12%2023:34:21,2018-08-12%2023:34:21,5T)')

        return ByDateTimeInPeriodFilter(period_date_start=datetime.strptime(values[0], '%Y-%m-%d %H:%M:%S'),
                                        period_date_end=datetime.strptime(values[1], '%Y-%m-%d %H:%M:%S'),
                                        frequency=values[2])
