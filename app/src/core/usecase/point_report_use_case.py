from app.src.util.SingletonMeta import SingletonMeta
from app.src.adapter.WorkerAdapter import WorkerAdapter
from app.src.adapter.PointAdapter import PointAdapter
from app.src.adapter.MailerAdapter import MailerAdapter


class PointReportUseCase(metaclass=SingletonMeta):
    _worker_adapter = WorkerAdapter()
    _point_adapter = PointAdapter()
    _mailer_adapter = MailerAdapter()

    def execute(self, username, month, year):
        worker = self.__find_worker(username)
        points = self._point_adapter.find_all(worker.username, month, year)

        self._mailer_adapter.send(
            "test@test.com",
            worker.mail,
            "title",
            "body :)"
        )

        print(worker.username, worker.username)
        print(worker)
        print(points)

    def __find_worker(self, username):
        worker = self._worker_adapter.find_one(username)

        if worker is None:
            raise Exception("Worker '", username, "' not found.")

        return worker
