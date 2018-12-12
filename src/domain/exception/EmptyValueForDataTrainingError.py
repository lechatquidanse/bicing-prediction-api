import uuid


class EmptyValueForDataTrainingError(ValueError):
    MESSAGE = 'No values found for data training with station %s'

    def __init__(self, message: str):
        super(self.__class__, self).__init__(message)

    @classmethod
    def with_station_id(cls, station_id: uuid):
        message = cls.MESSAGE % str(station_id)
        return cls(message)
