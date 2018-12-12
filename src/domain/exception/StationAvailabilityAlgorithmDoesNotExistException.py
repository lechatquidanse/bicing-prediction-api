import uuid


class StationAvailabilityAlgorithmDoesNotExistException(Exception):
    MESSAGE = 'Station with station_id %s does not exist'

    def __init__(self, message: str):
        super(self.__class__, self).__init__(message)

    @classmethod
    def with_station_id(cls, station_id: uuid):
        message = cls.MESSAGE % str(station_id)
        return cls(message)
