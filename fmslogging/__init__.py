import logging
from flask import Flask
from fmslogging.config import Config
from fmslogging.database import database


def create_application(configuration=Config):
    application = Flask(__name__)
    with application.app_context():
        logging.basicConfig(filename=configuration.LOGGING_FILE, level=configuration.LOGGING_LEVEL)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)  # try to log the queries plz
        application.config.from_object(configuration)
        database.init_app(application)
        # load blue prints
        from fmslogging.routes.intake import intake
        from fmslogging.routes.query import query
        # register blue prints
        application.register_blueprint(intake)
        application.register_blueprint(query)

    return application
