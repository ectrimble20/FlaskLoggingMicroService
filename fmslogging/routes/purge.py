from flask import Blueprint
from fmslogging.model import Service, LogMessage, LogLevel
from fmslogging.routes.route_helpers import error_response, query_response, get_query_date_range


purge = Blueprint('purge', __name__)


@purge.route("/purge/<string:service_name>/<string:date_str>", methods=["POST"])
def route_purge_service_logs(service_name, date_str):
    pass
