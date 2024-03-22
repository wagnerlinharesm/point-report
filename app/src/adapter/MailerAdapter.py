import smtplib
from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from app.src.adapter.helper.os_helper import OsHelper
from app.src.util.SingletonMeta import SingletonMeta


class MailerAdapter(metaclass=SingletonMeta):
    _HTML_MESSAGE_TEMPLATE = Template("<html><body><p>$message</p></body></html>")

    def __init__(self):
        self._smtp_client = MailerAdapter.__get_smtp_client(
            OsHelper.get_required_env("SMTP_HOST"),
            OsHelper.get_required_env("SMTP_PORT"),
            OsHelper.get_required_env("SMTP_USERNAME"),
            OsHelper.get_required_env("SMTP_PASSWORD")
        )
        self._mail_sender = OsHelper.get_required_env("MAIL_SENDER")

    @staticmethod
    def __get_smtp_client(host, port, username, password):
        try:
            smtp_client = smtplib.SMTP(host, port)
            smtp_client.starttls()
            smtp_client.login(username, password)

            return smtp_client
        except Exception as e:
            raise Exception("failed to get smtp_client client.", e)

    def send(self, destination, subject, message, attachment_name, attachment_data):
        msg = MIMEMultipart("mixed")
        msg["From"] = self._mail_sender
        msg["To"] = destination
        msg["Subject"] = subject

        msg_body = MIMEMultipart("alternative")
        plain_message = MIMEText(message, "plain")
        html_message = MIMEText(self._HTML_MESSAGE_TEMPLATE.substitute({"message": message}), "html")
        msg_body.attach(plain_message)
        msg_body.attach(html_message)
        msg.attach(msg_body)

        attachment = MIMEApplication(attachment_data)
        attachment.add_header("Content-Disposition", "attachment", filename=attachment_name)
        msg.attach(attachment)

        try:
            self._smtp_client.sendmail(self._mail_sender, destination, msg.as_string())

        except Exception as e:
            print("failed to send mail.", e)
            raise Exception("failed to send mail.", e)
