"""
Peewee Client to connect and query to bicing api data provider
"""
from typing import Any

from peewee import PostgresqlDatabase


class PeeweeClient():
    def __init__(self, db_client: PostgresqlDatabase):
        self._db_client = db_client

        self._db_client.connect()

    def query(self, query: str, params=None) -> Any:
        return self._db_client.execute_sql(query, params)
