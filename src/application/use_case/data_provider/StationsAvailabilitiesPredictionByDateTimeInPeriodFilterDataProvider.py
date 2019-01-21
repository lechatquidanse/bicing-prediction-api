"""
Data Provider to collect stations' availabilities predictions
"""
from application.use_case.data_provider.StationAvailabilitiesPredictionByDateTimeInPeriodFilterDataProvider import \
    StationAvailabilitiesPredictionByDateTimeInPeriodFilterDataProvider
from application.use_case.filter.ByDateTimeInPeriodFilter import ByDateTimeInPeriodFilter
from application.use_case.query.StationsAvailabilitiesPredictionByDateTimeInPeriodFilterView import \
    StationsAvailabilitiesPredictionByDateTimeInPeriodFilterView
from domain.exception.StationAvailabilityAlgorithmDoesNotExistException import \
    StationAvailabilityAlgorithmDoesNotExistException
from infrastructure.bicing_api.peewee.PeeweeLastStationStatesQuery import PeeweeLastStationStatesQuery


class StationsAvailabilitiesPredictionByDateTimeInPeriodFilterDataProvider:
    def __init__(self, client: PeeweeLastStationStatesQuery,
                 provider: StationAvailabilitiesPredictionByDateTimeInPeriodFilterDataProvider):
        self._client = client
        self._provider = provider

    def collection(self, station_ids: list,
                   by_filter: ByDateTimeInPeriodFilter) -> StationsAvailabilitiesPredictionByDateTimeInPeriodFilterView:

        data = self._client.query(station_ids)
        predictions = []

        for station_id in station_ids:
            try:
                predictions.append(self._provider.collection(station_id, by_filter))
            except StationAvailabilityAlgorithmDoesNotExistException:
                pass

        return StationsAvailabilitiesPredictionByDateTimeInPeriodFilterView(data, predictions, by_filter)
