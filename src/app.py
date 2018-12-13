"""
Flask Application
"""
import connexion
from flask_injector import FlaskInjector

from config.services import configure
from config.settings import DEBUG_MODE

if __name__ == '__main__':
    APP = connexion.App(__name__, specification_dir='../features/swagger')
    APP.add_api('indexer.yaml')
    FlaskInjector(app=APP.app, modules=[configure])

    APP.run(port=9090, debug=DEBUG_MODE)
