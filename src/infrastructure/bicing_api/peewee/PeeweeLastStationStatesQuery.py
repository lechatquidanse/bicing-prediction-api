"""
Peewee Query to find useful information (status slots) in bicing API data provider
"""
import datetime

from injector import inject

from infrastructure.bicing_api.peewee.PeeweeClient import PeeweeClient


class PeeweeLastStationStatesQuery:
    @inject
    def __init__(self, client: PeeweeClient):
        self._client = client

    def query(self, station_ids: list) -> list:
        last_stated_at = self.last_stated_at()

        query = ('SELECT '
                 'ss1.station_assigned_id as station_id,'
                 'ss1.status, '
                 'CAST(ss1.available_slot_number as FLOAT) + CAST(ss1.available_bike_number as FLOAT) as total '
                 'FROM "station_state" ss1 '
                 'WHERE ss1.stated_at = \'%s\' '
                 'AND ss1.station_assigned_id IN (\'%s\') '
                 % (last_stated_at, '\',\''.join(station_ids)))

        cursor = self._client.query(query)

        results = []
        for row in cursor.fetchall():
            results.append(row)

        return results

    def last_stated_at(self) -> datetime:
        query = ('SELECT '
                 'ss1.stated_at '
                 'FROM "station_state" ss1 '
                 'ORDER BY ss1.stated_at DESC '
                 'LIMIT 1')

        cursor = self._client.query(query)

        for row in cursor.fetchall():
            return row[0]
