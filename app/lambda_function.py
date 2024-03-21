from datetime import datetime

from app.src.core.usecase.point_report_use_case import PointReportUseCase
from app.src.util.JwtUtil import JwtUtil


def handler(event, _):
    print("begin")
    username = get_username(event)
    print(username)

    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    point_report_use_case = PointReportUseCase()
    point_report_use_case.execute(username, current_month, current_year)
    print("end")


def get_username(event):
    jwt_token = get_jwt_token(event)
    jwt_util = JwtUtil(jwt_token)

    return jwt_util.get_attribute("cognito:username")


def get_jwt_token(event):
    authorization = get_body(event)
    split_authorization = authorization.split()

    if len(split_authorization) == 1:
        return split_authorization[0]
    elif len(split_authorization) == 2:
        return split_authorization[1]

    raise Exception('invalid authorization.')


def get_body(event):
    records = event.get('Records', [])

    if len(records) == 0:
        raise Exception('missing record.')

    if len(records) > 1:
        raise Exception('multiple records.')

    body = records[0].get('body')

    if body is None:
        raise Exception('missing body.')

    return body
