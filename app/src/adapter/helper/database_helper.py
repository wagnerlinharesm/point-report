import psycopg2
from app.src.util.SingletonMeta import SingletonMeta
from app.src.adapter.helper.os_helper import OsHelper


class DatabaseHelper(metaclass=SingletonMeta):
    _connection = None

    def __init__(self):
        self._connection = self.__connect(
            OsHelper.get_required_env("POINT_DB_HOST"),
            OsHelper.get_required_env("POINT_DB_DATABASE"),
            OsHelper.get_required_env("POINT_DB_USERNAME"),
            OsHelper.get_required_env("POINT_DB_PASSWORD")
        )

    def __del__(self):
        if self._connection:
            self._connection.close()
            print("db connection closed.")

    @staticmethod
    def __connect(host, database, user, password):
        try:
            connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )

            connection.autocommit = True

            return connection

        except psycopg2.Error as e:
            print("Error connecting to database.", e)
            raise Exception("Error connecting to database.", e)

    @staticmethod
    def __rows_to_dict(cursor, rows):
        rows_dict = []

        column_names = [desc[0] for desc in cursor.description]

        for row in rows:
            row_dict = dict(zip(column_names, row))
            rows_dict.append(row_dict)

        return rows_dict

    def fetch_all(self, query, params=None):
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return self.__rows_to_dict(cursor, rows)

        except psycopg2.Error as e:
            print("Error executing query '", query, "' with parameters '", params, "'.", e)
            raise Exception("Error executing query.", e)


