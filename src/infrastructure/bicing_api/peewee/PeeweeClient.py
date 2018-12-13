"""
Peewee Client to connect and query to bicing api data provider
"""
from typing import Any

from peewee import PostgresqlDatabase


class PeeweeClient:
    def __init__(self, db_client: PostgresqlDatabase):
        self._db_client = db_client


    def query(self, query: str, params=None) -> Any:
        if self._db_client.is_closed() is True:
            self._db_client.connect()

        results = self._db_client.execute_sql(query, params)

        return results
