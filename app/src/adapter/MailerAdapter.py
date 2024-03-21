import boto3
import smtplib
from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from app.src.adapter.helper.os_helper import OsHelper
from app.src.util.SingletonMeta import SingletonMeta


class MailerAdapter(metaclass=SingletonMeta):
    _MAIL_SENDER = "rm349538@fiap.com.br"
    _HTML_MESSAGE_TEMPLATE = Template("<html><body><p>$message</p></body></html>")
    _ses_client = None

    def __init__(self):
        self._ses_client = MailerAdapter.__get_ses()

    @staticmethod
    def __get_ses():
        try:
            return boto3.client("ses")
        except Exception as e:
            raise Exception("failed to get ses client.", e)

    def send(self, destination, subject, message, attachment_name, attachment_data):

        # build message
        msg = MIMEMultipart("mixed")
        msg["From"] = self._MAIL_SENDER
        msg["To"] = destination
        msg["Subject"] = subject

        # build message body
        msg_body = MIMEMultipart("alternative")
        plain_message = MIMEText(message, "plain")
        html_message = MIMEText(self._HTML_MESSAGE_TEMPLATE.substitute({"message": message}), "html")
        msg_body.attach(plain_message)
        msg_body.attach(html_message)
        msg.attach(msg_body)

        # build attachment
        attachment = MIMEApplication(attachment_data)
        attachment.add_header("Content-Disposition", "attachment", filename=attachment_name)
        msg.attach(attachment)

        try:
            server = smtplib.SMTP("email-smtp.us-east-2.amazonaws.com", 587)
            server.starttls()
            server.login(OsHelper.get_required_env("user"), OsHelper.get_required_env("pass"))

            response = server.sendmail(self._MAIL_SENDER, destination, msg.as_string())

            print(response)
        except Exception as e:
            print("failed to send mail.", e)
            raise Exception("failed to send mail.", e)
