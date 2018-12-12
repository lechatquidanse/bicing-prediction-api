from pandas import DataFrame, DatetimeIndex, concat

from infrastructure.data_mining.StationData import StationData


class StationDataPrediction(StationData):
    def __init__(self, datetime_index: DatetimeIndex, training_data_set: DataFrame):
        self._datetime_index = datetime_index
        self._training_data_set = training_data_set

    def data_frame(self) -> DataFrame:
        data_frame = self._datetime_index.to_frame()
        data_frame = data_frame.drop(0, axis=1)
        data_frame = concat([self._training_data_set, data_frame], axis=0)
        data_frame['bike'].fillna(0.0, inplace=True)
        data_frame = data_frame.drop('bike', axis=1)
        data_frame.fillna(0)

        data_frame = self._date_transform(data_frame)
        data_frame = data_frame['2018-12-18 06:00:00':]

        return data_frame.loc[:,~data_frame.columns.duplicated()]

