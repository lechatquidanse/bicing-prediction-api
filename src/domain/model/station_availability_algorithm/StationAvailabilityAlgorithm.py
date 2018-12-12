import uuid

from numpy.ma import array
from pandas import DataFrame

# @todo avoid xgboost dependency
from xgboost import Booster, DMatrix


class StationAvailabilityAlgorithm:
    def __init__(self, station_id: uuid, training_data_set: DataFrame, model: Booster):
        self._station_id = station_id
        self._training_data_set = training_data_set
        self._model = model

    def predict(self, data_set: DataFrame) -> array:
        return self._model.predict(DMatrix(data_set))

    def station_id(self) -> uuid:
        return self._station_id

    def training_data_set(self) -> DataFrame:
        return self._training_data_set

    def model(self) -> Booster:
        return self._model

    def __eq__(self, other):
        if isinstance(other, StationAvailabilityAlgorithm):
            return self._station_id == self._station_id \
                   and self._training_data_set.equals(other._training_data_set) \
                   and self._model.get_dump() == other._model.get_dump()
        return False
