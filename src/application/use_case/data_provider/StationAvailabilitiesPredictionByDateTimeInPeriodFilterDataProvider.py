"""
Data Provider to collect a station's availabilties predictions
"""
import uuid

from application.use_case.filter.ByDateTimeInPeriodFilter import ByDateTimeInPeriodFilter
from application.use_case.query.StationAvailabilitiesPredictionByDateTimeInPeriodFilterView import \
    StationAvailabilitiesPredictionByDateTimeInPeriodFilterView
from domain.exception.StationAvailabilityAlgorithmDoesNotExistException import \
    StationAvailabilityAlgorithmDoesNotExistException
from domain.model.station_availability_algorithm.StationAvailabilityAlgorithmRepositoryInterface import \
    StationAvailabilityAlgorithmRepositoryInterface
from infrastructure.data_mining.StationDataPrediction import StationDataPrediction


class StationAvailabilitiesPredictionByDateTimeInPeriodFilterDataProvider:
    def __init__(self, repository: StationAvailabilityAlgorithmRepositoryInterface):
        self._repository = repository

    def collection(self, station_id: uuid,
                   by_filter: ByDateTimeInPeriodFilter) -> StationAvailabilitiesPredictionByDateTimeInPeriodFilterView:
        station_availability_algorithm = self._repository.find_by_station_id(station_id)

        if station_availability_algorithm is None:
            raise StationAvailabilityAlgorithmDoesNotExistException.with_station_id(station_id)

        prediction_data_set = StationDataPrediction(by_filter.to_date_time_index(),
                                                    station_availability_algorithm.training_data_set())

        predictions = station_availability_algorithm.predict(prediction_data_set.data_frame())

        return StationAvailabilitiesPredictionByDateTimeInPeriodFilterView(station_id, by_filter, predictions)
