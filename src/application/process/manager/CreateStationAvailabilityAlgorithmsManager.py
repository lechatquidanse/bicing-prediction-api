"""
Manager to create Station Availability Algorithm model for each stations
"""
from datetime import datetime

from injector import inject

from application.use_case.command.CreateStationAvailabilityAlgorithmCommand import \
    CreateStationAvailabilityAlgorithmCommand
from application.use_case.handler import CreateStationAvailabilityAlgorithmHandler
from infrastructure.bicing_api.peewee.PeeweeStationQuery import PeeweeStationQuery


class CreateStationAvailabilityAlgorithmsManager:
    @inject
    def __init__(self, query: PeeweeStationQuery, handler: CreateStationAvailabilityAlgorithmHandler):
        self._query = query
        self._handler = handler

    def manage(self, start_date: datetime, frequency: str):
        station_ids = self._query.query()

        for station_id in station_ids:
            try:
                self._handler.handle(CreateStationAvailabilityAlgorithmCommand(station_id, start_date, frequency))
            except ValueError:
                pass
