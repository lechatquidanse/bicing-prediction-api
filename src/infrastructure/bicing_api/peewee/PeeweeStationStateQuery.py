"""
Peewee Query to find useful information (stated_at datetime, number of bikes and slots) in bicing API data provider
"""
import uuid

from injector import inject

from infrastructure.bicing_api.peewee.PeeweeClient import PeeweeClient


class PeeweeStationStateQuery:
    INDEX_FIELD = 'stated_at'
    FEATURE_FIELD = 'bike'
    FIELDS = ['stated_at', 'bike', 'slot']

    @inject
    def __init__(self, client: PeeweeClient):
        self._client = client

    def query(self, station_id: uuid) -> list:
        query = ('SELECT '
                 'ss1.stated_at, '
                 'CAST(ss1.available_bike_number as FLOAT) as bike, '
                 'CAST(ss1.available_slot_number as FLOAT) as slot '
                 'FROM "station_state" ss1 '
                 'WHERE ss1.station_assigned_id=\'%s\'' % station_id)
        cursor = self._client.query(query)

        results = []
        for row in cursor.fetchall():
            results.append(row)

        return results
