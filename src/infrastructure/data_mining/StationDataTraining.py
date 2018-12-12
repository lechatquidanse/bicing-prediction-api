"""
Representation of station data used for data mining training
"""
from datetime import datetime

from pandas import DataFrame

from infrastructure.data_mining.StationData import StationData


class StationDataTraining(StationData):
    def __init__(self, records: list, columns: list, feature_column: str, indexed_column: str, frequency: str,
                 test_start_date: datetime):
        self._records = records
        self._columns = columns
        self._indexed_column = indexed_column
        self._feature_column = feature_column
        self._frequency = frequency
        self._test_start_date = test_start_date

    # @todo check for data_frame_test if necessary
    def data_frame(self) -> DataFrame:
        data_frame = self._date_transform(self._averaged_data_frame())
        data_frame.dropna(inplace=True)

        # data_frame_test = data_frame[test_start_date:].iloc[:-1, :]
        return data_frame[:self._test_start_date]
        # return data_frame_test, data_frame_train

    def _data_frame(self) -> DataFrame:
        return DataFrame.from_records(data=self._records, columns=self._columns, index=self._indexed_column)

    def _averaged_data_frame(self) -> DataFrame:
        data_frame = self._data_frame()

        return DataFrame(data_frame[self._feature_column].resample(self._frequency).mean())

    def frequency(self) -> str:
        return self._frequency
