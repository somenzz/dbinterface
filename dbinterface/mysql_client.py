from .database_interface import DataBaseInterface
import pymysql.cursors
import pymysql


class MysqlClient(DataBaseInterface):
    def init(self, host, port, user, pwd, database, **kwargs):
        self.host = host
        self.user = user
        self.password = pwd
        self.port = port
        self.charset = "utf8" if not kwargs else kwargs.get("charset", "utf8")
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            database=self.database,
            password=self.password,
            charset=self.charset,
            cursorclass=pymysql.cursors.SSDictCursor,
        )

    def close(self):
        self.db.close()

    def is_active(self):
        pass

    def get_tables(self):
        pass

    def read(self, sql, params=()):  # pymysql.execute(sql)
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            row = cursor.fetchone()
            while row:
                yield tuple(row.values())
                row = cursor.fetchone()

    # def fetch(self, sql, params=()):  # pymysql.execute(sql)
    #     with self.connection.cursor() as cursor:
    #         cursor.execute(sql, params)
    #         row = cursor.fetchone()
    #         while row:
    #             yield tuple(row.values())
    #             row = cursor.fetchone()

    def read_map(self, sql, params=()):  # pymysql.execute(sql)
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            row = cursor.fetchone()
            while row:
                yield row
                row = cursor.fetchone()

    def write(self, sql: str, params: tuple) -> tuple:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            self.connection.commit()

    def write_many(self, sql: str, params: tuple) -> tuple:
        pass
