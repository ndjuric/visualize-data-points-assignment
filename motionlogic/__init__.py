import logging
import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
migrate = Migrate()

# Import all models so that they are registered with SQLAlchemy
from motionlogic.models import opencellid


def create_app():
    """ Bootstrap function to initialise the Flask app and config """
    app = Flask(__name__)

    app.config['CORS_HEADERS'] = 'Content-Type'

    env = os.getenv('MOTIONLOGIC_ENV', 'Dev')
    app.config.from_object('motionlogic.config.{0}Config'.format(env))

    db.init_app(app)
    migrate.init_app(app, db)

    app.logger.debug('Initialising Blueprints...')
    from .web import main as main_blueprint
    from .web import swagger as swagger_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(swagger_blueprint)

    initialise_logger(app)
    app.logger.info('Starting...')

    init_flask_restful_routes(app)

    return app


def initialise_logger(app):
    log_dir = app.config['LOG_DIR']
    log_level = app.config['LOG_LEVEL']

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(log_dir + '/motionlogic.log', 'a', 2 * 1024 * 1024, 3)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )

    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)


def init_flask_restful_routes(app):
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

    from motionlogic.api.swagger_docs_api import SwaggerDocsAPI
    from motionlogic.api.cell_tower_api import CellTowerAPI
    from motionlogic.api.tile_png_api import TilePngAPI

    api.add_resource(CellTowerAPI, '/api/v1/cell_towers/<string:bounds>', endpoint="get cell towers", methods=['GET'])
    api.add_resource(TilePngAPI, '/api/v1/get_png/<string:bounds>', endpoint="gen png", methods=['GET'])
    api.add_resource(SwaggerDocsAPI, '/api/docs')
