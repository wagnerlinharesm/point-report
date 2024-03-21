from app.src.util.SingletonMeta import SingletonMeta


class StorageAdapter(metaclass=SingletonMeta):
    def get_file(self, file_name):
        print("mock get [not found]")
        return None


    def save_file(self, file_name, bytes):
        print("mock save")
