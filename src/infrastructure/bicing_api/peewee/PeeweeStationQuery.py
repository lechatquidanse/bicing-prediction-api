import uuid

from injector import inject
from infrastructure.bicing_api.peewee.PeeweeClient import PeeweeClient


class PeeweeStationQuery:
    @inject
    def __init__(self, client: PeeweeClient):
        self._client = client

    def query(self) -> list:
        cursor = self._client.query('SELECT s1.station_id FROM "station" s1 ')

        results = []
        for row in cursor.fetchall():
            results.append(uuid.UUID(row[0]))

        return results
