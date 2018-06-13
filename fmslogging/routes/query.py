from flask import Blueprint
from fmslogging.model import Service, LogMessage, LogLevel
from fmslogging.routes.route_helpers import error_response, query_response, get_query_date_range


query = Blueprint('query', __name__)


@query.route("/query/service/<string:label>/<string:date_str>", methods=["GET"])
@query.route("/query/service/<string:label>", defaults={'date_str': None}, methods=["GET"])
def route_query_service(label, date_str):
    service = Service.query.filter_by(label=label).first()
    if not service:
        return error_response(400, "Invalid request: bad service {}".format(label))
    if date_str:
        dates = get_query_date_range(date_str)
        if not dates:
            return error_response(400, "Invalid request: bad date format {}".format(date_str))
        results = LogMessage.query.filter_by(service=service).filter(
            LogMessage.log_date >= dates[0]
        ).filter(
            LogMessage.log_date <= dates[1]
        ).all()
    else:
        results = LogMessage.query.filter_by(service=service).all()
    return query_response(results)


@query.route("/query/level/<string:label>/<string:date_str>", methods=["GET"])
@query.route("/query/level/<string:label>", defaults={'date_str': None}, methods=["GET"])
def route_query_level(label, date_str):
    level = LogLevel.query.filter_by(label=label.lower()).first()
    if not level:
        return error_response(400, "Invalid request: bad log level {}".format(label))
    if date_str:
        dates = get_query_date_range(date_str)
        if not dates:
            return error_response(400, "Invalid request: bad date format {}".format(date_str))
        results = LogMessage.query.filter_by(level=level).filter(
            LogMessage.log_date >= dates[0]
        ).filter(
            LogMessage.log_date <= dates[1]
        ).all()
    else:
        results = LogMessage.query.filter_by(level=level).all()
    return query_response(results)


@query.route("/query/date/<string:date_str>", methods=["GET"])
def route_query_date(date_str):
    dates = get_query_date_range(date_str)
    if not dates:
        return error_response(400, "Invalid request: bad date format {}".format(date_str))
    results = LogMessage.query.filter(
        LogMessage.log_date >= dates[0]
    ).filter(
        LogMessage.log_date <= dates[1]
    ).all()
    return query_response(results)
