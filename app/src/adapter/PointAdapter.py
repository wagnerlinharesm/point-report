from app.src.util.SingletonMeta import SingletonMeta
from app.src.adapter.helper.database_helper import DatabaseHelper
from app.src.core.domain.Point import Point
from app.src.core.domain.PointPeriod import PointPeriod


class PointAdapter(metaclass=SingletonMeta):
    _db_helper = DatabaseHelper()

    def find_month_points(self, worker, month, year):
        query = """
            SELECT 
                p."data",
                p.horas_trabalhadas,
                sp.situacao,
                pp.hora_entrada,
                pp.hora_saida,
                pp.horas_periodo 
            FROM ponto p
            INNER JOIN periodo_ponto pp 
            ON p.id_ponto = pp.id_ponto
            INNER JOIN situacao_ponto sp
            ON p.id_situacao_ponto = sp.id_situacao_ponto 
            WHERE EXTRACT(MONTH FROM p.data) = %s
            AND EXTRACT(YEAR FROM p.data) = %s
            AND p.id_funcionario = %s
            ORDER BY p.data ASC
        """

        rows_dict = self._db_helper.fetch_all(query, (month, year, worker))

        if len(rows_dict) == 0:
            return []

        points = []
        current_point = None
        for row_dict in rows_dict:
            row_date = row_dict['data']
            if current_point is None or current_point.date != row_date:
                current_point = Point(
                    row_dict['situacao'],
                    row_dict['data'],
                    row_dict['horas_trabalhadas']
                )

                points.append(current_point)

                period = PointPeriod(
                    row_dict['hora_entrada'],
                    row_dict['hora_saida'],
                    row_dict['horas_periodo']
                )

                current_point.add_period(period)

        return points
