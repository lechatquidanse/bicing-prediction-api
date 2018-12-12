import connexion
from flask_injector import FlaskInjector

from config.services import configure

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='../features/swagger')
    app.add_api('indexer.yaml')
    injector = FlaskInjector(app=app.app, modules=[configure])

    app.run(port=9090, debug=True)
