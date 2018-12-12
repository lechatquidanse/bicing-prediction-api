"""
Exception description when a station availability algorithm is not found
"""
import uuid


class StationAvailabilityAlgorithmDoesNotExistException(Exception):
    MESSAGE = 'Station with station_id %s does not exist'

    @classmethod
    def with_station_id(cls, station_id: uuid):
        message = cls.MESSAGE % str(station_id)
        return cls(message)
