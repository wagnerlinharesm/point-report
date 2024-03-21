from app.src.util.SingletonMeta import SingletonMeta
from app.src.adapter.WorkerAdapter import WorkerAdapter
from app.src.adapter.PointAdapter import PointAdapter


class PointReportUseCase(metaclass=SingletonMeta):
    _worker_adapter = WorkerAdapter()
    _point_adapter = PointAdapter()

    def execute(self, worker, month, year):
        worker = self._worker_adapter.find_one(worker)
        points = self._point_adapter.find_all(worker, month, year)
        print(worker.username, worker.username)
        print(worker)
        print(points)
