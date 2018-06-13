from flask import Blueprint, request, jsonify
from fmslogging.model import Service, LogMessage, LogMessageBody, LogLevel
from fmslogging.database import database
from fmslogging.utility import ip_wild_card_check
from datetime import datetime


intake = Blueprint('intake', __name__)

# TODO figure out if we can do a cached version of the log levels to reduce queries
# TODO if that works, we might do the same for services since there would realistically be a small number of these


@intake.route("/insert", methods=["POST"])
def route_new_log():
    if not request.is_json:
        return jsonify(
            code=400, message="Invalid request, must be in JSON format"
        )
    json_data = request.get_json()
    if not json_data:
        return jsonify(
            code=400, message="Invalid request, malformed data: missing 'data' element"
        )
    if json_data.get('messages') is None:
        return jsonify(
            code=400, message="Invalid request, malformed data: missing 'messages' element"
        )
    if json_data.get('key') is None:
        return jsonify(
            code=403, message="Unauthorized"
        )
    service = Service.query.filter_by(key=json_data['key']).first()
    if not service:
        return jsonify(
            code=403, message="Unauthorized"
        )
    # verify the service came from a valid IP address
    if not ip_wild_card_check(request.remote_addr, service.ip_address):
        return jsonify(
            code=403, message="Unauthorized"
        )
    # alright, that's all the checks
    for message in json_data['messages']:
        # try to find the log level for this message
        log_level = LogLevel.query.filter_by(label=message['level'].lower()).first()
        if not log_level:
            log_level = LogLevel.query.get(1)  # use a default if that failed to locate a valid message
        msg_body = LogMessageBody(
            body=message['body']
        )
        database.session.add(msg_body)
        database.session.add(LogMessage(
            service=service,
            level=log_level,
            body=msg_body,
            log_date=datetime.strptime(message['timestamp'], "%Y-%m-%d %H:%M:%S")
        ))
    database.session.commit()
    return jsonify(
        code=200, message="Success"
    )
