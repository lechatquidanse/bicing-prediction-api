import uuid

from domain.model.station_availability_algorithm import StationAvailabilityAlgorithm

class StationAvailabilityAlgorithmRepositoryInterface:
    def save(self, station_availability_algorithm: StationAvailabilityAlgorithm): raise NotImplementedError

    def find_by_station_id(self, station_id: uuid): raise NotImplementedError
