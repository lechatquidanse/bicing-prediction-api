from injector import inject

from application.use_case.command import CreateStationAvailabilityAlgorithmCommand
from domain.exception.EmptyValueForDataTrainingError import EmptyValueForDataTrainingError
from domain.model.station_availability_algorithm.StationAvailabilityAlgorithm import StationAvailabilityAlgorithm
from domain.model.station_availability_algorithm import \
    StationAvailabilityAlgorithmRepositoryInterface
from infrastructure.bicing_api.peewee import PeeweeStationStateQuery
from infrastructure.data_mining.StationDataTraining import StationDataTraining
from infrastructure.data_mining.xgboost import XGBoostDataTrainer


class CreateStationAvailabilityAlgorithmHandler:
    @inject
    def __init__(self, query: PeeweeStationStateQuery, data_trainer: XGBoostDataTrainer,
                 repository: StationAvailabilityAlgorithmRepositoryInterface):
        self._query = query
        self._data_trainer = data_trainer
        self._repository = repository

    def handle(self, command: CreateStationAvailabilityAlgorithmCommand):
        station_id = command.station_id()
        records = self._query.query(station_id)

        if 0 == len(records):
            raise EmptyValueForDataTrainingError.with_station_id(station_id)

        station_data = StationDataTraining(records, self._query.FIELDS, self._query.FEATURE_FIELD, self._query.INDEX_FIELD,
                                   command.frequency(), command.start_date())

        training_data_set = station_data.data_frame()

        model = self._data_trainer.train(training_data_set)

        self._repository.save(StationAvailabilityAlgorithm(command.station_id(), training_data_set, model))
