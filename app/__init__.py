from flask import Flask
# from flasgger import Swagger
from flask_cors import CORS
from instance.config import app_config
from app.api.v2.views.auth_views import auth as v2
from app.api.v2.views.question_views import question as quest


def creat_app(config_name):
    """This method creats app with configuration in the instance folder"""
    # We will be using the config variable to determine the database

    app = Flask(__name__, instance_relative_config=True)
    """using instance_relative_config will load config file from instance folder when app created"""
    """Loading the configurations from config.py contained in the instance folder"""
    CORS(app)
    app.register_blueprint(v2)
    app.register_blueprint(quest)
    """Registering blueprint to the app"""

    app.config.from_object(app_config[config_name])
    """We are loading the default configuration"""

    app.config.from_pyfile('config.py')
    return app
