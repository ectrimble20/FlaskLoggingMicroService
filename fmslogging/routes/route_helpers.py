from flask import request, jsonify
from datetime import datetime
from fmslogging.model import Service
from fmslogging.utility import ip_wild_card_check


def error_response(code, message):
    return jsonify(code=code, message=message)


def query_response(result_set):
    data_set = []
    for row in result_set:
        d = {
            "service": row.service.label,
            "level": row.level.label,
            "timestamp": row.log_date.strftime("%Y-%m-%d %H:%M:%S"),
            "body": row.body.body
        }
        data_set.append(d)
    return jsonify(
        code=200,
        message="Success",
        count=len(result_set),
        data=data_set
    )


def convert_date_str_to_datetime(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def get_query_date_range(date_str):
    try:
        date_start = date_str + " 00:00:00"
        date_end = date_str + " 23:59:59"
        return [datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S"), datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")]
    except ValueError:
        return None
