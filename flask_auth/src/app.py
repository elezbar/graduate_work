from flasgger import Swagger
from flask import Flask
from redis import Redis

from api import api_bp
from core.config import config
from db import cache
from utils.initial_db_data_command import utils_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(config.flask)

    app.register_blueprint(api_bp)
    app.register_blueprint(utils_bp)
    Swagger(app, template=config.flask.SWAGGER)
    cache.redis = Redis(host=config.cache.redis_host, port=config.cache.redis_port,
                        decode_responses=True)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
