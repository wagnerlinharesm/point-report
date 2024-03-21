import boto3
from app.src.util.SingletonMeta import SingletonMeta


class MailerAdapter(metaclass=SingletonMeta):
    _ses_client = None

    def __init__(self):
        _ses_client = MailerAdapter.__get_ses()

    @staticmethod
    def __get_ses():
        try:
            return boto3.client('ses')
        except Exception as e:
            raise Exception("failed to get ses client.", e)

    def send(self, sender, destination, subject, text):
        try:
            response = self._ses_client.send_email(
                Source=sender,
                Destination={
                    'ToAddresses': [destination]
                },
                Message={
                    'Subject': {'Data': subject},
                    'Body': {
                        'Text': {'Data': text},
                    }
                }
            )
            print(response)
        except Exception as e:
            print("failed to send mail.", e)
            raise Exception("failed to send mail.", e)
