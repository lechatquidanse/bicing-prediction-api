"""
Unit test for FileSystemStationAvailabilityAlgorithmRepository
"""
import pickle
import unittest
import uuid

from pandas import DataFrame
from xgboost import Booster

from domain.model.station_availability_algorithm.StationAvailabilityAlgorithm import StationAvailabilityAlgorithm
from infrastructure.persistence.file_system.StorageManager import StorageManager
from infrastructure.persistence.file_system.repository.FileSystemStationAvailabilityAlgorithmRepository import \
    FileSystemStationAvailabilityAlgorithmRepository


class FileSystemStationAvailabilityAlgorithmRepositoryUnitTest(unittest.TestCase):
    MODEL_STORAGE_PATH_TEST = 'var/test/persistence/model/'

    def test_it_can_save(self) -> None:
        station_id = uuid.uuid4()

        station_availability_algorithm = StationAvailabilityAlgorithm(station_id, DataFrame(['data', 'frame', 'test']),
                                                                      Booster())

        self._repository.save(station_availability_algorithm)

        self.assertEqual(self._repository.find_by_station_id(station_id), station_availability_algorithm)

    def test_it_can_override_an_existing_one(self) -> None:
        station_id = uuid.uuid4()

        first = StationAvailabilityAlgorithm(station_id, DataFrame(['data_1', 'frame_1', 'test_1']), Booster())
        self._repository.save(first)

        override = StationAvailabilityAlgorithm(station_id, DataFrame(['data_2', 'frame_2', 'test_2']), Booster())
        self._repository.save(override)

        self.assertEqual(self._repository.find_by_station_id(station_id), override)

    def test_it_can_find_one_by_station_id(self) -> None:
        station_id = uuid.uuid4()
        station_availability_algorithm = StationAvailabilityAlgorithm(station_id, DataFrame(['data', 'frame', 'test']),
                                                                      Booster())

        self._repository.save(station_availability_algorithm)

        self.assertEqual(self._repository.find_by_station_id(station_id), station_availability_algorithm)

    def test_it_can_not_find_one_by_station_id_if_it_does_not_exist(self) -> None:
        station_availability_algorithm = StationAvailabilityAlgorithm(uuid.uuid4(),
                                                                      DataFrame(['data', 'frame', 'test']), Booster())

        self._repository.save(station_availability_algorithm)

        self.assertIsNone(self._repository.find_by_station_id(uuid.uuid4()))

    def setUp(self) -> None:
        super().setUp()

        self._storage_manager = StorageManager()
        self._repository = FileSystemStationAvailabilityAlgorithmRepository(pickle, self.MODEL_STORAGE_PATH_TEST,
                                                                            self._storage_manager)

    def tearDown(self) -> None:
        self._storage_manager.truncate_storage_location(self.MODEL_STORAGE_PATH_TEST)
        self._repository = None

        super().tearDown()
