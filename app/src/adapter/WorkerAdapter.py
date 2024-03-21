from app.src.core.domain.Worker import Worker
from app.src.util.SingletonMeta import SingletonMeta
from app.src.adapter.helper.database_helper import DatabaseHelper


class WorkerAdapter(metaclass=SingletonMeta):
    _db_helper = DatabaseHelper()

    def find_one(self, username):
        query = """
            select
            id_funcionario,
            email
            from funcionario
            where id_funcionario = %s
        """

        row_dict = self._db_helper.fetch_one(query, (username))

        if row_dict is None:
            return None

        return Worker(
            row_dict['id_funcionario'],
            row_dict['email'],
        )
