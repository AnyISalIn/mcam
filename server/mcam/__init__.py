import logging

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_restful import Api
from flask_rq2 import RQ

db = MongoEngine()
rq = RQ()
cors = CORS()

from mcam.config import config

app = Flask(__name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(api_bp)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    rq.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(logging.DEBUG)
    app.logger.debug('this will show in the log')

    app.register_blueprint(api_bp)

    import mcam.provider
    import mcam.template
    import mcam.instance

    return app
