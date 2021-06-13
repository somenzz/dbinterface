# -*- coding:utf8 -*-

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import ISOLATION_LEVEL_READ_UNCOMMITTED
import sys
# from psycopg2.errors import UndefinedTable,InvalidSchemaName
from io import StringIO
from .database_interface import DataBaseInterface
from .mixins import ExportMixin


class PostgresClient(ExportMixin, DataBaseInterface):
    """
    postgresql client
    """

    def init(self, host, port, user, pwd, database, **kwargs):

        self.database = database
        self.user = user
        self.password = pwd
        self.host = host
        self.port = port
        self.connection = None
        self.cursor_count = 0

    def connect(self):
        self.connection = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        self.connection.set_client_encoding("utf-8")
        self.connection.set_session(isolation_level=ISOLATION_LEVEL_READ_UNCOMMITTED)

    def close(self):
        self.connection.close()

    # def exists(self, tabname):
    #     """
    #     仅传入表名，判断是否存在
    #     """
    #     assert "." in tabname
    #     # result = elk_prod.fetch_many(
    #     #     f"select * from sys.all_tables where table_name = %s ", (tabname.lower(),), 0
    #     # )
    #
    #     try:
    #         self.fetch_many(f"select * from {tabname}", parameters=(), nums=10)
    #     # except UndefinedTable :
    #     #    return False
    #     # except InvalidSchemaName:
    #     #    return False
    #     except Exception as e:
    #         return False
    #     return True

    def is_active(self):
        return False if self.connection.closed else True

    def get_tables(self, schema: str = None) -> list:
        """
        获取某个数据库表的表名列表
        返回数据格式为 list[dict] -> [{'schema','name','type','remarks'}]
        """
        result = []
        sql = "select table_schema, table_name, table_type, " \
              "cast(obj_description(relfilenode,'pg_class') as varchar) as comment " \
              "from information_schema.tables a " \
              "left join pg_class b  on a.table_name = b.relname "

        with self.connection.cursor(f"cusor{self.cursor_count}") as cur:
            if schema:
                sql = "select table_schema, table_name, table_type, " \
                      "cast(obj_description(relfilenode,'pg_class') as varchar) as comment " \
                      "from information_schema.tables a " \
                      "left join pg_class b  on a.table_name = b.relname " \
                      "where table_schema = %s "
                cur.execute(sql,(schema,))
            else:
                cur.execute(sql)

            for row in cur:
                result.append({
                    'schema': row[0],
                    'name': row[1],
                    'type': row[2],
                    'remarks': row[3],
                })

        return result




    def read(self, sql: str, params: tuple = ()) -> tuple:
        with self.connection.cursor(f"cursor{self.cursor_count}") as cur:
            self.cursor_count += 1
            cur.execute(sql, params)
            for row in cur:
                yield row

    def read_map(self, sql: str, params: tuple = ()) -> dict:
        cur = self.connection.cursor(f"cursor{self.cursor_count}", cursor_factory=DictCursor)
        cur.execute(sql, params)
        for row in cur:
            yield dict(row)

    def write(self, sql: str, params: tuple) -> tuple:
        with self.connection.cursor() as cur:
            cur.execute(sql,params)
            return cur.rowcount

    def write_many(self, sql: str, params: tuple) -> tuple:
        with self.connection.cursor() as cur:
            cur.executemany(sql, params)
            return cur.rowcount


    def copy_to_file(self, query, file_name, encoding="utf8", delimiter="\x02"):

        if delimiter.lower().startswith("0x"):
            delimiter = chr(int(delimiter, 16))

        copy_sql = f"""COPY (
{query}
) TO '{file_name}' WITH(encoding '{encoding}', delimiter '{delimiter}', null '', format 'text')"""
        with self.connection.cursor() as cur:
            cur.copy_expert(copy_sql, sys.stdout)
            return cur.rowcount

# def copy_from_memory(self, values, schema, tabName, columns=None):
#     # self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#     """
#     sql_insert = "insert in tab values(?,?)"
#     values =[()()()]
#     """
#     # with self.connection.cursor() as cur:
#     #     f = StringIO()
#     #     a = cur.copy_expert(sql,f,size = 8192)
#     #     f.seek(0)
#     #     print(f.read())
#
#     with StringIO() as w:
#         for value in values:
#             # print(value)
#             text = (
#                 "\x02".join(
#                     [
#                         ""
#                         if x is None
#                         else str(x)
#                         .replace("\n", "")
#                         .replace("\r", "")
#                         .replace("\\", "")
#                         for x in value
#                     ]
#                 )
#                 + "\n"
#             )
#             # print(text)
#             w.write(text)
#         w.seek(0)
#         with self.connection.cursor() as cur:
#             cur.copy_from(
#                 file=w,
#                 table=f"{schema}.{tabName}",
#                 sep="\x02",
#                 size=16384,
#                 columns=columns,
#             )
#             self.connection.commit()
# print(f"elk -> insert into {tabName}: {len(values)} rows")

# def insert_many_row(self, sql_insert, values):
#     """
#     sql_insert = "insert in tab values(?,?)"
#     values =[()()()]
#     """
#     with self.connection.cursor() as cursor:
#         cursor.executemany(sql_insert, values)
#     self.connection.commit()
#     print(f"elk -> insert {len(values)} rows")
#
# def get_table_cols_info(self, schema, tabname):
#     """
#     返回：
#         列信息
#         主键信息
#         外键信息
#         索引信息
#     """
#     colums = []
#     with self.connection.cursor() as cur:
#         cur.execute(
#             f"SELECT column_name FROM sys.all_tab_columns where table_name = '{tabname}' and owner = '{self.user}' order by column_id"
#         )
#         for x in cur:
#             colums.append(x[0])
#     if colums == []:
#         with self.connection.cursor() as cur:
#             cur.execute(
#                 f"SELECT column_name FROM sys.all_tab_columns where table_name = '{tabname}' and owner = 'omm' order by column_id"
#             )
#             for x in cur:
#                 colums.append(x[0])
#
#     return colums
#


    def copy_from_file(self, file_path, tabName, delimiter, encoding="utf-8", columns=None):

        if delimiter.lower().startswith("0x"):
            delimiter = chr(int(delimiter, 16))

        with open(file_path, "r", encoding = encoding) as reader:
            with self.connection.cursor() as cur:
                cur.copy_from(
                    file=reader, table=tabName, sep= delimiter , size=16384, columns=columns
                )
                self.connection.commit()
            return cur.rowcount