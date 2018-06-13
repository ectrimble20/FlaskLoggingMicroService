from datetime import datetime
from fmslogging.database import database


class Service(database.Model):
    __tablename__ = "service"
    id = database.Column(database.Integer, primary_key=True)
    label = database.Column(database.String(50), unique=True, nullable=False)
    ip_address = database.Column(database.String(12), nullable=False)
    key = database.Column(database.String(75), nullable=False)
    privileged = database.Column(database.Boolean, nullable=False, default=False)


class LogLevel(database.Model):
    __tablename__ = "log_level"
    id = database.Column(database.Integer, primary_key=True)
    label = database.Column(database.String(50), unique=True, nullable=False)


class LogMessageBody(database.Model):
    __tablename__ = "log_message_body"
    id = database.Column(database.Integer, primary_key=True)
    body = database.Column(database.Text, nullable=False)
    log_message = database.relationship("LogMessage", back_populates="body")


class LogMessage(database.Model):
    __tablename__ = "log_message"
    id = database.Column(database.Integer, primary_key=True)
    service_id = database.Column(database.Integer, database.ForeignKey('service.id'), nullable=False)
    service = database.relationship("Service")
    log_level_id = database.Column(database.Integer, database.ForeignKey('log_level.id'), nullable=False)
    level = database.relationship("LogLevel")
    log_message_body_id = database.Column(database.Integer, database.ForeignKey('log_message_body.id'), nullable=False)
    body = database.relationship("LogMessageBody", back_populates="log_message")
    log_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)   # from the message
    create_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)  # from the system
