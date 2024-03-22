import boto3
from botocore.exceptions import ClientError
from io import BytesIO
from app.src.adapter.helper.os_helper import OsHelper
from app.src.util.SingletonMeta import SingletonMeta


class StorageAdapter(metaclass=SingletonMeta):
    def __init__(self):
        self.s3_client = StorageAdapter.__get_s3_client(
            OsHelper.get_required_env("BOTO3_USERNAME"),
            OsHelper.get_required_env("BOTO3_PASSWORD")
        )
        self.bucket_name = OsHelper.get_required_env("POINT_REPORT_BUCKET_NAME")

    @staticmethod
    def __get_s3_client(username, password):
        try:
            return boto3.client(
                's3',
                aws_access_key_id=username,
                aws_secret_access_key=password
            )

        except Exception as e:
            raise Exception("failed to get s3 client.", e)

    def get_file(self, file_name):
        bytes_data = BytesIO()

        try:
            self.s3_client.download_fileobj(self.bucket_name, file_name, bytes_data)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return None

        bytes_data.seek(0)
        data = bytes_data.read()

        return data

    def save_file(self, file_name, data):
        bytes_data = BytesIO(data.encode('iso-8859-1'))
        self.s3_client.upload_fileobj(bytes_data, self.bucket_name, file_name)
