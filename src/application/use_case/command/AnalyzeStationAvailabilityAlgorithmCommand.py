import uuid
from datetime import datetime


class AnalyzeStationAvailabilityAlgorithmCommand:
    def __init__(self, station_id: uuid, start_date: datetime, frequency: str):
        self._station_id = station_id
        self._start_date = start_date
        self._frequency = frequency

    def station_id(self) -> uuid:
        return self._station_id

    def start_date(self) -> datetime:
        return self._start_date

    def frequency(self) -> str:
        return self._frequency