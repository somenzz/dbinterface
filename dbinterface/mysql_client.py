from .database_interface import DataBaseInterface
import pymysql.cursors
import pymysql

from .mixins import ExportMixin


class MysqlClient(ExportMixin, DataBaseInterface):
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
        self.connection.close()

    def is_active(self):
        return self.connection.open

    def get_tables(self, schema = None):
        """
        获取某个数据库表的表名列表
        返回数据格式为 list[dict] -> [{'schema','name','type','remarks'}]
        """
        result = []
        with self.connection.cursor() as cursor:
            sql = "select TABLE_SCHEMA,TABLE_NAME,TABLE_TYPE,TABLE_COMMENT from information_schema.tables"
            if schema:
                sql = "select TABLE_SCHEMA,TABLE_NAME,TABLE_TYPE,TABLE_COMMENT " \
                      "from information_schema.tables " \
                      "where TABLE_SCHEMA = %s "
                print(sql)
                cursor.execute(sql, (schema,))
            else:

                cursor.execute(sql, ())
            for row in cursor.fetchall():
                result.append({
                    'schema':row['TABLE_SCHEMA'],
                    'name': row['TABLE_NAME'],
                    'type': row['TABLE_TYPE'],
                    'remarks': row['TABLE_COMMENT'],
                })


        return result


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

    def write(self, sql: str, params: tuple) -> int:
        with self.connection.cursor() as cursor:
            rows_affected = cursor.execute(sql, params)
            self.connection.commit()
            return rows_affected

    def write_many(self, sql: str, params: tuple) -> int:
        """
        This method improves performance on multiple-row INSERT and REPLACE.
        Otherwise it is equivalent to looping over args with execute().
        """

        with self.connection.cursor() as cursor:
            rows_affected = cursor.executemany(sql, params)
            self.connection.commit()
            return rows_affected
