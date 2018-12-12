"""
Exception description when no data expected for a model training are found
"""
import uuid


class EmptyValueForDataTrainingError(ValueError):
    MESSAGE = 'No values found for data training with station %s'

    @classmethod
    def with_station_id(cls, station_id: uuid):
        message = cls.MESSAGE % str(station_id)
        return cls(message)
