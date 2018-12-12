from datetime import datetime

import connexion
from flask_injector import FlaskInjector

from application.process.manager.CreateStationAvailabilityAlgorithmsManager import \
    CreateStationAvailabilityAlgorithmsManager
from config.services import configure

if __name__ == '__main__':
    app = connexion.App(__name__)
    injector = FlaskInjector(app=app.app, modules=[configure])

    manager = injector.injector.get(CreateStationAvailabilityAlgorithmsManager)

    start_date = datetime.strptime('2018-11-20 20:00:00', '%Y-%m-%d %H:%M:%S')

    manager.manage(start_date, '5T')