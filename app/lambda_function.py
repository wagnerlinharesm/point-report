from datetime import datetime

from app.src.core.usecase.point_report_use_case import PointReportUseCase


def handler(event, context):
    print("begin", event, context, "end")

    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    point_report_use_case = PointReportUseCase()
    point_report_use_case.execute("", current_month, current_year)
