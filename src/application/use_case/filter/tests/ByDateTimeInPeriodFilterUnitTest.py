import unittest
from datetime import datetime

from pandas._libs.tslibs.timestamps import Timestamp

from application.use_case.filter.ByDateTimeInPeriodFilter import ByDateTimeInPeriodFilter


class ByDateTimeInPeriodFilterUnitTest(unittest.TestCase):
    def test_it_can_return_as_date_time_index(self) -> None:
        item = ByDateTimeInPeriodFilter(period_date_start=datetime.strptime('2017/08/12 07:00:00', '%Y/%m/%d %H:%M:%S'),
                                        period_date_end=datetime.strptime('2017/08/12 08:00:00', '%Y/%m/%d %H:%M:%S'),
                                        frequency='5T')

        date_time_index = item.to_date_time_index()
        expected = [Timestamp('2017-08-12 07:00:00', freq='5T'), Timestamp('2017-08-12 07:05:00', freq='5T'),
                    Timestamp('2017-08-12 07:10:00', freq='5T'), Timestamp('2017-08-12 07:15:00', freq='5T'),
                    Timestamp('2017-08-12 07:20:00', freq='5T'), Timestamp('2017-08-12 07:25:00', freq='5T'),
                    Timestamp('2017-08-12 07:30:00', freq='5T'), Timestamp('2017-08-12 07:35:00', freq='5T'),
                    Timestamp('2017-08-12 07:40:00', freq='5T'), Timestamp('2017-08-12 07:45:00', freq='5T'),
                    Timestamp('2017-08-12 07:50:00', freq='5T'), Timestamp('2017-08-12 07:55:00', freq='5T'),
                    Timestamp('2017-08-12 08:00:00', freq='5T')]

        self.assertTrue(set(expected) == set(date_time_index.tolist()))
        self.assertEqual('5T', date_time_index.freq)

    def test_it_can_not_be_created_with_period_start_after_period_end(self) -> None:
        with self.assertRaises(AssertionError): ByDateTimeInPeriodFilter(
            period_date_start=datetime.strptime('2017/08/12 07:00:00',
                                                '%Y/%m/%d %H:%M:%S'),
            period_date_end=datetime.strptime('1998/08/12 08:00:00',
                                              '%Y/%m/%d %H:%M:%S'),
            frequency='5T')
