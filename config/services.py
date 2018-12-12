import pickle

from injector import Binder
from peewee import PostgresqlDatabase

from application.process.manager.CreateStationAvailabilityAlgorithmsManager import \
    CreateStationAvailabilityAlgorithmsManager
from application.use_case.handler.CreateStationAvailabilityAlgorithmHandler import \
    CreateStationAvailabilityAlgorithmHandler
from application.use_case.data_provider.StationAvailabilitiesPredictionByDateTimeInPeriodFilterDataProvider import \
    StationAvailabilitiesPredictionByDateTimeInPeriodFilterDataProvider
from config.settings import BICING_API_DB_DATABASE, BICING_API_DB_USER, BICING_API_DB_PASSWORD, BICING_API_DB_HOST, \
    BICING_API_DB_PORT, PERSISTENCE_MODEL_FILE_SYSTEM_PATH

from domain.model.station_availability_algorithm.StationAvailabilityAlgorithmRepositoryInterface import \
    StationAvailabilityAlgorithmRepositoryInterface
from infrastructure.bicing_api.peewee.PeeweeClient import PeeweeClient
from infrastructure.bicing_api.peewee.PeeweeStationQuery import PeeweeStationQuery
from infrastructure.bicing_api.peewee.PeeweeStationStateQuery import PeeweeStationStateQuery
from infrastructure.data_mining.xgboost.XGBRegresser import XGBRegresser
from infrastructure.data_mining.xgboost.XGBoostDataTrainer import XGBoostDataTrainer
from infrastructure.persistence.file_system.StorageManager import StorageManager

from infrastructure.persistence.file_system.repository.FileSystemStationAvailabilityAlgorithmRepository import \
    FileSystemStationAvailabilityAlgorithmRepository
from infrastructure.request.flask.ByDateTimeInPeriodFilterConverter import ByDateTimeInPeriodFilterConverter
from user_interface.rest.flask.response.FlaskPredictByStationIdResponse import FlaskPredictByStationIdResponse


def configure(binder: Binder) -> Binder:
    ## User Interface ::
    ### REST ::
    binder.bind(FlaskPredictByStationIdResponse, FlaskPredictByStationIdResponse())

    ## Infrastructure ::
    ### Bicing API ::
    binder.bind(PostgresqlDatabase,
                to=PostgresqlDatabase(BICING_API_DB_DATABASE, user=BICING_API_DB_USER, password=BICING_API_DB_PASSWORD,
                                      host=BICING_API_DB_HOST, port=BICING_API_DB_PORT))
    binder.bind(PeeweeClient, to=PeeweeClient(binder.injector.get(PostgresqlDatabase)))
    binder.bind(PeeweeStationQuery, to=PeeweeStationQuery(binder.injector.get(PeeweeClient)))
    binder.bind(PeeweeStationStateQuery, to=PeeweeStationStateQuery(binder.injector.get(PeeweeClient)))
    ### Persistence ::
    binder.bind(StationAvailabilityAlgorithmRepositoryInterface,
                to=FileSystemStationAvailabilityAlgorithmRepository(pickle, PERSISTENCE_MODEL_FILE_SYSTEM_PATH, StorageManager()))
    ### Data Mining ::
    binder.bind(XGBRegresser, to=XGBRegresser())
    binder.bind(XGBoostDataTrainer, to=XGBoostDataTrainer(binder.injector.get(XGBRegresser)))
    ### Request ::
    binder.bind(ByDateTimeInPeriodFilterConverter, to=ByDateTimeInPeriodFilterConverter())

    ## Application ::
    ### Use Case ::
    #### Handler ::
    binder.bind(CreateStationAvailabilityAlgorithmHandler,
                to=CreateStationAvailabilityAlgorithmHandler(binder.injector.get(PeeweeStationStateQuery),
                                                             binder.injector.get(XGBoostDataTrainer),
                                                             binder.injector.get(
                                                                 StationAvailabilityAlgorithmRepositoryInterface)))
    ### Process ::
    #### Manager ::
    binder.bind(CreateStationAvailabilityAlgorithmsManager,
                to=CreateStationAvailabilityAlgorithmsManager(
                    binder.injector.get(PeeweeStationQuery),
                    binder.injector.get(CreateStationAvailabilityAlgorithmHandler)))
    #### Data Provider ::
    binder.bind(StationAvailabilitiesPredictionByDateTimeInPeriodFilterDataProvider,
                to=StationAvailabilitiesPredictionByDateTimeInPeriodFilterDataProvider(
                    binder.injector.get(StationAvailabilityAlgorithmRepositoryInterface)))

    return binder
