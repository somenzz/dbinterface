from abc import ABCMeta, abstractmethod


class DataBaseInterface(metaclass=ABCMeta):

    @abstractmethod
    def init(self, host, port, user, pwd, database, **kwargs):
        """
        数据库的参数， kwargs 可用于具体数据库的个性化的参数
        """
        pass

    @abstractmethod
    def connect(self):
        """
        连接数据库
        """
        pass

    @abstractmethod
    def is_active(self) -> bool:
        """
        数据库是否已经连接
        """
        pass

    @abstractmethod
    def get_tables(self, schema: str = None) -> list:
        """
        获取某个数据库表的表名列表，schema 为 None 时查询所有。
        返回数据格式为 list[dict] -> [{'schema','name','type','remarks'}]
        """
        pass

    @abstractmethod
    def read(self, sql: str, params: tuple) -> tuple:
        """
        读取数据，只用于读取，返回 tuple 的迭代器
        """
        pass

    @abstractmethod
    def read_map(self, sql: str, params: tuple) -> dict:
        """
        读取数据，只用于读取，返回 dict 的迭代器
        """
        pass

    @abstractmethod
    def write(self, sql: str, params: tuple) -> int:
        """
        更新数据，返回受影响的行数
        """
        pass

    @abstractmethod
    def write_many(self, sql: str, params: tuple) -> int:
        """
        批量更新数据，返回受影响的行数
        """
        pass

    @abstractmethod
    def export(
        self,
        sql: str,
        params: tuple,
        file_path: str,
        encoding: str,
        delimeter: str,
        quote: str,
        all_col_as_str: bool = True,
    ) -> int:
        """
        导出数据到文件到本地，返回导出的行数
        """
        pass
