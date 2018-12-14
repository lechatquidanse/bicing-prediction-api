"""
CLI command to generate model for each station to predict station's availabilities
"""
from datetime import datetime

import connexion
from flask_injector import FlaskInjector

from application.process.manager.CreateStationAvailabilityAlgorithmsManager import \
    CreateStationAvailabilityAlgorithmsManager
from config.services import configure
from config.settings import DEBUG_MODE

if __name__ == '__main__':
    APP = connexion.App(__name__)
    APP.debug = DEBUG_MODE
    INJECTOR = FlaskInjector(app=APP.app, modules=[configure])

    MANAGER = INJECTOR.injector.get(CreateStationAvailabilityAlgorithmsManager)

    MANAGER.manage(datetime.strptime('2018-11-20 20:00:00', '%Y-%m-%d %H:%M:%S'), '5T')
