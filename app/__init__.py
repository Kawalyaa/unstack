from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from instance.config import app_config
from app.api.v2.views.auth_views import auth as v2
from app.api.v2.views.question_views import question as quest
from app.api.v2.views.answer_views import answer as ans


def creat_app(config_name="development"):
    """This method creats app with configuration in the instance folder"""
    # We will be using the config variable to determine the database

    app = Flask(__name__, instance_relative_config=True)
    """using instance_relative_config will load config file from instance folder when app created"""
    """Loading the configurations from config.py contained in the instance folder"""

    app.config['SWAGGER'] = {'uiversion': 2, 'title': 'UNSTACK',
                             'description': "is a web based app that enables users to \
                             ask questions on the platform and get answers.",
                             'basePath': '', 'version': '2.0.1'}

    Swagger(app)

    CORS(app)
    app.register_blueprint(v2)
    app.register_blueprint(quest)
    app.register_blueprint(ans)
    """Registering blueprint to the app"""

    app.config.from_object(app_config["development"])
    """We are loading the default configuration"""

    app.config.from_pyfile('config.py')
    return app
