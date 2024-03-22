import json
import base64

from app.src.core.usecase.point_report_use_case import PointReportUseCase
from app.src.util.JwtUtil import JwtUtil


def handler(event, _):
    current_month, current_year = get_date(event)
    username = get_username(event)

    point_report_use_case = PointReportUseCase()
    point_report_use_case.execute(username, current_month, current_year)


def get_date(event):
    date_str = get_message_attribute(event, "body")
    date = json.loads(date_str)

    return date['month'], date['year']


def get_username(event):
    jwt_token = get_jwt_token(event)
    jwt_util = JwtUtil(jwt_token)

    return jwt_util.get_required_attribute("cognito:username")


def get_jwt_token(event):
    authorization = get_message_attribute(event, "authorization")
    split_authorization = authorization.split()

    if len(split_authorization) == 1:
        return split_authorization[0]
    elif len(split_authorization) == 2:
        return split_authorization[1]

    raise Exception("invalid authorization.")


def get_message_attribute(event, name):
    message = json.loads(event.get("Records", [])[0].get("body"))
    b64attribute = message[name]
    return base64.b64decode(b64attribute)
