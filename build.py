from fmslogging import create_application
from fmslogging.config import Config
from fmslogging.database import database

"""
NOTE THIS WILL DROP THE EXISTING DATABASE AND ALL DATA IN IT

This is designed to completely rebuild the data structure and should be considered
only useful for TESTING purposes.  This is kept up-to-date with the current model.

I plan to add in an UPDATE model at some point, but until I finish this product, this
is what we've got to work with.
"""
if __name__ == '__main__':
    test_config = Config()
    # TODO change this to your database string
    Config.SQLALCHEMY_DATABASE_URI = "mysql://remote_read_write:rrw4th1s@192.168.1.170:3306/flaskms_logging"
    app = create_application(test_config)
    with app.app_context():
        database.drop_all()
        from fmslogging.model import Service, LogLevel, LogMessage, LogMessageBody
        database.create_all()
        # create the log levels
        # TODO if you'd like different log levels, you can edit these and add/remove/replace as you please.
        database.session.add(LogLevel(id=1, label="not_set"))
        database.session.add(LogLevel(id=2, label="debug"))
        database.session.add(LogLevel(id=3, label="info"))
        database.session.add(LogLevel(id=4, label="warning"))
        database.session.add(LogLevel(id=5, label="error"))
        database.session.add(LogLevel(id=6, label="critical"))
        # create a test service
        # TODO you can change this to whatever you'd like as a "default" service on creation.
        database.session.add(Service(label="test_service", key="test_key", ip_address="192.168.%", privileged=True))
        # commit the session
        database.session.commit()
