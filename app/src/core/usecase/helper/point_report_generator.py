from string import Template
from app.src.util.SingletonMeta import SingletonMeta

class PointReportGenerator(metaclass=SingletonMeta):
    def generate(self, worker, points, month, year):
        return PointReportGenerator.__build_html(worker, points, month, year)

    @staticmethod
    def __build_html(worker, points, month, year):
        html_template = """
            <!DOCTYPE html>
            <html lang="en">
            $head
            $body
            </html>
        """

        title = Template("$username - $month/$year").substitute({
            "username": worker.username,
            "month": month,
            "year": year
        })

        head = PointReportGenerator.__build_head("title")
        body = PointReportGenerator.__build_body("title", points)

        return Template(html_template).substitute({
            "head": head,
            "body": body,
        })

    @staticmethod
    def __build_head(title):
        head_template = """
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>$title</title>
                <style>
                    table {
                        border-collapse: collapse;
                        width: 50%;
                        margin-bottom: 20px;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
        """

        return Template(head_template).substitute({
            "title": title
        })

    @staticmethod
    def __build_body(title, points):
        body_template = """
            <body>
            <h2>$title</h2>
            $elements
            </body>
        """

        elements = PointReportGenerator.__build_points(points)

        return Template(body_template).substitute({
            "title": title,
            "elements": elements
        })

    @staticmethod
    def __build_points(points):
        html_points = ""

        for point in points:
            html_points += PointReportGenerator.__build_point(point)

        return html_points

    @staticmethod
    def __build_point(point):
        element_template = """
            <table>
                <thead>
                    <tr>
                        <th colspan="3">Ponto</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>Dia</b></td>
                        <td><b>Situação</b></td>
                        <td><b>Horas trabalhadas</b></td>
                    </tr>
                    <tr>
                        <td><b>$date</b></td>
                        <td><b>$situation</b></td>
                        <td><b>$work_time</b></td>
                    </tr>
                </tbody>
                <thead>
                    <tr>
                        <th colspan="3">Períodos</th>
                    </tr>
                </thead>
                <tbody>
                    $point_periods
                </tbody>
            </table>
        """

        point_periods = PointReportGenerator.__build_point_periods(point.periods)

        return Template(element_template).substitute({
            "date": point.date,
            "situation": point.situation,
            "work_time": point.work_time,
            "point_periods": point_periods
        })

    @staticmethod
    def __build_point_periods(point_periods):
        html_point_periods = """
            <tr>
                <td><b>Entrada</b></td>
                <td><b>Saida</b></td>
                <td><b>Horas trabalhadas</b></td>
            </tr>
        """

        for point_period in point_periods:
            html_point_periods += PointReportGenerator.__build_point_period(point_period)

        return html_point_periods

    @staticmethod
    def __build_point_period(point_period):
        point_period_template = """
            <tr>
                <td>$begin_time</td>
                <td>$end_time</td>
                <td>$work_time</td>
            </tr>
        """

        return Template(point_period_template).substitute({
            "begin_time": point_period.begin_time,
            "end_time": point_period.end_time,
            "work_time": point_period.work_time
        })
