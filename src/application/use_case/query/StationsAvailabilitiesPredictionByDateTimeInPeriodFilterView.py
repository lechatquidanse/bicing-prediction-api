"""
View for query stations availabilities by filter
"""
from typing import Optional

from application.use_case.filter.ByDateTimeInPeriodFilter import ByDateTimeInPeriodFilter
from application.use_case.query.StationAvailabilitiesPredictionByDateTimeInPeriodFilterView import \
    StationAvailabilitiesPredictionByDateTimeInPeriodFilterView


class StationsAvailabilitiesPredictionByDateTimeInPeriodFilterView:
    def __init__(self, data: list, views: list, by_filter: ByDateTimeInPeriodFilter):
        self._data = data
        self._views = views
        self._by_filter = by_filter

    def data(self) -> {}:
        return self._data

    def views(self) -> list:
        return self._views

    def by_filter(self) -> ByDateTimeInPeriodFilter:
        return self._by_filter

    def find_predictions_by_station_id(self, station_id) -> Optional[
            StationAvailabilitiesPredictionByDateTimeInPeriodFilterView]:
        return next((view for view in self._views if view.station_id() == station_id), None)
