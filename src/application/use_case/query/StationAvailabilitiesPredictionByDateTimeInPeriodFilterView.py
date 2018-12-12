import uuid

from pandas import DataFrame

from application.use_case.filter.ByDateTimeInPeriodFilter import ByDateTimeInPeriodFilter


class StationAvailabilitiesPredictionByDateTimeInPeriodFilterView:
    def __init__(self, station_id: uuid, filter: ByDateTimeInPeriodFilter, predictions: DataFrame):
        self._station_id = station_id
        self._filter = filter
        self._predictions = predictions

    def station_id(self) -> uuid:
        return self._station_id

    def filter(self) -> ByDateTimeInPeriodFilter:
        return self._filter

    def predictions(self) -> DataFrame:
        return self._predictions


