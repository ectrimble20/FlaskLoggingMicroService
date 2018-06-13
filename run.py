from fmslogging import create_application
from fmslogging.config import Config
from logging import DEBUG as DEFAULT_LOG_LEVEL

conf = Config()
Config.ENV = "development"
Config.DEBUG = True
Config.LOGGING_LEVEL = DEFAULT_LOG_LEVEL
Config.SQLALCHEMY_DATABASE_URI = "mysql://remote_read_write:rrw4th1s@192.168.1.170:3306/flaskms_logging"
Config.SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
Config.SQLALCHEMY_TRACK_MODIFICATIONS = False
app = create_application(conf)

if __name__ == '__main__':
    # app.run(debug=True, host="localhost")
    app.run(debug=True, host="192.168.1.3")
