from abc import ABCMeta, abstractmethod


class DataBaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def init(self, host, port, user, pwd, database, **kwargs):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def is_active(self) -> bool:
        pass

    @abstractmethod
    def get_tables(self, schema: str) -> list:
        pass

    @abstractmethod
    def read(self, sql: str, params: tuple) -> tuple:
        pass

    @abstractmethod
    def read_map(self, sql: str, params: tuple) -> dict:
        pass

    @abstractmethod
    def write(self, sql: str, params: tuple) -> tuple:
        pass

    @abstractmethod
    def write_many(self, sql: str, params: tuple) -> tuple:
        pass
