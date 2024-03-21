from app.src.adapter.PointAdapter import PointAdapter


class PointReportUseCase(metaclass=SingletonMeta):
    _point_adapter = PointAdapter()

    def execute(self, worker, month, year):
        data = self._point_adapter.find_month_points(worker, month, year)
        print(data)
