from string import Template

from app.src.util.SingletonMeta import SingletonMeta
from app.src.adapter.StorageAdapter import StorageAdapter
from app.src.adapter.WorkerAdapter import WorkerAdapter
from app.src.adapter.PointAdapter import PointAdapter
from app.src.adapter.MailerAdapter import MailerAdapter
from app.src.core.usecase.helper.point_report_generator import PointReportGenerator


class PointReportUseCase(metaclass=SingletonMeta):
    _MAIL_TITLE_TEMPLATE = Template("Ponto Eletrônico - Report $month/$year")
    _MAIL_TEXT_TEMPLATE = Template("Segue em anexo report de ponto eletrônico p/ o mês/ano de $month/$year.")
    _FILE_NAME_TEMPLATE = Template("$year/$month/$username.html")
    _ATTACHMENT_NAME_TEMPLATE = Template("ponto-eletronico-report-$month-$year.html")

    _worker_adapter = WorkerAdapter()
    _point_adapter = PointAdapter()
    _mailer_adapter = MailerAdapter()
    _storage_adapter = StorageAdapter()

    def execute(self, username, month, year):
        worker = self.__find_worker(username)
        points = self._point_adapter.find_all(worker.username, month, year)
        report = self.__find_report(worker, points, month, year)
        self.__send_report(report, worker, month, year)

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

        print("checking report cache.")
        report = self._storage_adapter.get_file(file_name)
        if report is None:
            print("cache missing.")
            report = PointReportGenerator.generate_pdf(worker, points, month, year)
            self._storage_adapter.save_file(file_name, report)
        else:
            print("cache hit.")

        return report

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
