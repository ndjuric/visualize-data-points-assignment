import logging
import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
migrate = Migrate()

from backend.models import opencellid


def create_app():
    app = Flask(__name__)

    app.config['CORS_HEADERS'] = 'Content-Type'

    env = os.getenv('backend_ENV', 'Dev')
    app.config.from_object('backend.config.{0}Config'.format(env))

    db.init_app(app)
    migrate.init_app(app, db)

    app.logger.debug('Initialising Blueprints...')
    from .web import main as main_blueprint
    from .web import swagger as swagger_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(swagger_blueprint)

    init_logger(app)
    app.logger.info('Starting...')

    init_routes(app)

    return app


def init_logger(app):
    log_dir = app.config['LOG_DIR']
    log_level = app.config['LOG_LEVEL']

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(log_dir + '/backend.log', 'a', 2 * 1024 * 1024, 3)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )

    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)


def init_routes(app):
    app.logger.info('Initialising API Routes')
    api = Api(app)
    CORS(
        app,
        origins="http://localhost:1990",
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Credentials"
        ],
        supports_credentials=True
    )

    from backend.api.swagger_docs_api import SwaggerDocsAPI
    from backend.api.cell_tower_api import CellTowerAPI

    api.add_resource(CellTowerAPI, '/api/v1/cell_towers/<string:bounds>', endpoint="get cell towers", methods=['GET'])
    api.add_resource(SwaggerDocsAPI, '/api/docs')
