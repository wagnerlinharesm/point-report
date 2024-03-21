from string import Template
from app.src.adapter.StorageAdapter import StorageAdapter
from app.src.util.SingletonMeta import SingletonMeta
from app.src.adapter.WorkerAdapter import WorkerAdapter
from app.src.adapter.PointAdapter import PointAdapter
from app.src.adapter.MailerAdapter import MailerAdapter


class PointReportUseCase(metaclass=SingletonMeta):
    _MAIL_TITLE_TEMPLATE = Template("Ponto Eletrônico - Report $month/$year")
    _MAIL_TEXT_TEMPLATE = Template("Segue em anexo report de ponto eletrônico p/ o período de $month/$year.")
    _FILE_NAME_TEMPLATE = Template("$year/$month/$username.txt")
    _ATTACHMENT_NAME_TEMPLATE = Template("ponto-eletronico-report-$month-$year.txt")

    _worker_adapter = WorkerAdapter()
    _point_adapter = PointAdapter()
    _mailer_adapter = MailerAdapter()
    _storage_adapter = StorageAdapter()

    def execute(self, username, month, year):
        print("worker")
        worker = self.__find_worker(username)
        print("points")
        points = self._point_adapter.find_all(worker.username, month, year)
        print("report")
        report = self.__find_report(worker, points, month, year)
        print("send", report)
        self.__send_report(report, worker, month, year)
        print("end")

    def __find_worker(self, username):
        worker = self._worker_adapter.find_one(username)

        if worker is None:
            raise Exception("Worker '", username, "' not found.")

        return worker

    def __find_report(self, worker, points, month, year):
        file_name = self._FILE_NAME_TEMPLATE.substitute({
            "year": year,
            "month": month,
            "username": worker.username
        })

        report = self._storage_adapter.get_file(file_name)
        if report is None:
            report = self.__generate_report(worker, points, month, year)
            self._storage_adapter.save_file(file_name, report)

        return report

    def __generate_report(self, worker, points, month, year):
        return "abcdef" # mock

    def __send_report(self, report, worker, month, year):
        title = self._MAIL_TITLE_TEMPLATE.substitute({
            "month": month,
            "year": year,
        })

        message = self._MAIL_TEXT_TEMPLATE.substitute({
            "month": month,
            "year": year,
        })

        attachment_name = self._ATTACHMENT_NAME_TEMPLATE.substitute({
            "month": month,
            "year": year,
        })

        self._mailer_adapter.send(
            worker.mail,
            title,
            message,
            attachment_name,
            report
        )
