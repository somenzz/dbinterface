# encoding=utf-8

import ibm_db_dbi
import ibm_db
from .database_interface import DataBaseInterface
from .mixins import ExportMixin


class Db2Client(ExportMixin, DataBaseInterface):
    def init(self, host, port, user, pwd, database, **kwargs):

        self.database = database
        self.hostname = host
        self.port = port
        self.uid = user
        self.pwd = pwd
        self.protocol = "TCPIP" if not kwargs else kwargs.get("protocol", "utf8")
        self.connection = None
        self.dbi_connection = None

    def connect(self):
        self.connection = ibm_db.connect(
            f"DATABASE={self.database};HOSTNAME={self.hostname};PORT={self.port};PROTOCOL={self.protocol};UID={self.uid};PWD={self.pwd};",
            "",
            "",
        )
        self.dbi_connection = ibm_db_dbi.Connection(self.connection)

    # def set_current_schema(self, schema):
    #     """
    #     https://github.com/ibmdb/python-ibmdb/wiki/APIs#ibm_dbset_option
    #     """
    #     # ibm_db.set_option(self.connection, {ibm_db.SQL_ATTR_CURRENT_SCHEMA : schema},1)
    #     self.dbi_connection.set_current_schema(schema)
    #     print("current schema is ", self.dbi_connection.get_current_schema())

    def close(self):
        ibm_db.close(self.connection)

    def is_active(self):
        return ibm_db.active(self.connection)

    def read(self, sql, params=()):

        cur = self.dbi_connection.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        while row:
            yield row
            row = cur.fetchone()
        cur.close()
        # stmt = ibm_db.prepare(self.connection, sql)
        # for index, param in enumerate(params):
        #     ibm_db.bind_param(stmt, index + 1, param)
        # ibm_db.execute(stmt)
        # row = ibm_db.fetch_tuple(stmt)
        # while row:
        #     yield (row)
        #     row = ibm_db.fetch_tuple(stmt)

    # def fetch(self, sql, params=None):
    #     cur = self.dbi_connection.cursor()
    #     cur.execute(sql, params)
    #     row = cur.fetchone()
    #     while row:
    #         yield row
    #         row = cur.fetchone()
    #     cur.close()
    #
    # def fetch_one(self, sql, params=None):
    #     cur = self.dbi_connection.cursor()
    #     cur.execute(sql, params)
    #     row = cur.fetchone()
    #     yield row

    def read_map(self, sql, params=()):
        """
        返回一个列表，元素是字典，键是列名，值是列值。
        """
        stmt = ibm_db.prepare(self.connection, sql)
        success = ibm_db.execute(stmt, params)
        # stmt = ibm_db.exec_immediate(self.connection,sql)
        if success:
            r = ibm_db.fetch_assoc(stmt)
            while r:
                yield r
                r = ibm_db.fetch_assoc(stmt)

    def write(self, sql, params):
        """
        sql_insert = "insert in tab values(?,?)"
        values =()
        """
        stmt = ibm_db.prepare(self.connection, sql)
        for index, param in enumerate(params):
            ibm_db.bind_param(stmt, index + 1, param)
        return ibm_db.execute(stmt)

    def write_many(self, sql, params):
        """
        sql_insert = "insert in tab values(?,?)"
        values =(()()())
        """
        stmt = ibm_db.prepare(self.connection, sql)
        rows_affected = ibm_db.execute_many(stmt, params)
        # row_count = ibm_db.num_rows(stmt)
        # rc = ibm_db.commit(self.connection)
        return rows_affected

    # def get_table_info(self, schema, tabname):
    #     """
    #     返回：
    #         列信息
    #         主键信息
    #         外键信息
    #         索引信息
    #     """
    #     tables_info = self.dbi_connection.tables(schema_name=schema, table_name=tabname)
    #     assert tables_info
    #
    #     tables_info = tables_info[0]
    #     columns_info = self.dbi_connection.columns(
    #         schema_name=schema, table_name=tabname
    #     )
    #
    #     ##print("列信息")
    #     # print(columns_info)
    #     cols = []
    #     for col in columns_info:
    #         cols.append(
    #             [
    #                 col["COLUMN_NAME"],
    #                 col["REMARKS"],
    #                 col["TYPE_NAME"],
    #                 col["COLUMN_SIZE"],
    #                 col["DECIMAL_DIGITS"],
    #                 col["IS_NULLABLE"],
    #             ]
    #         )
    #     ###print(cols)
    #     ###print("主键信息")
    #     primary_keys_info = self.dbi_connection.primary_keys(
    #         schema_name=schema, table_name=tabname
    #     )
    #     pks = {}
    #     for pk in primary_keys_info:
    #         if pk["PK_NAME"] in pks:
    #             pks[pk["PK_NAME"]] += "," + pk["COLUMN_NAME"]
    #         else:
    #             pks[pk["PK_NAME"]] = pk["COLUMN_NAME"]
    #     ##print(pks)
    #     ##print("外键信息")
    #     fks = {}
    #     foreign_keys_info = self.dbi_connection.foreign_keys(
    #         schema_name=schema, table_name=tabname
    #     )
    #     # [{'PKTABLE_CAT': None, 'PKTABLE_SCHEM': 'EDW', 'PKTABLE_NAME': 'ADVISE_INSTANCE', 'PKCOLUMN_NAME': 'START_TIME', 'FKTABLE_CAT': None, 'FKTABLE_SCHEM': 'EDW', 'FKTABLE_NAME': 'ADVISE_MQT', 'FKCOLUMN_NAME': 'RUN_ID', 'KEY_SEQ': 1, 'UPDATE_RULE': 3, 'DELETE_RULE': 0, 'FK_NAME': 'SQL170306104743460', 'PK_NAME': 'SQL170306104743210', 'DEFERRABILITY': 7}]
    #     for fk in foreign_keys_info:
    #         if fk["FK_NAME"] in fks:
    #             fks[fk["FK_NAME"]][0].append(fk["FKCOLUMN_NAME"])
    #             fks[fk["FK_NAME"]][2].append(fk["PKCOLUMN_NAME"])
    #         else:
    #             fks[fk["FK_NAME"]] = [
    #                 [fk["FKCOLUMN_NAME"]],
    #                 [fk["PKTABLE_NAME"]],
    #                 [fk["PKCOLUMN_NAME"]],
    #             ]
    #     ##print(fks)
    #     ##print("索引信息")
    #     ids = {}
    #     indexes_info = self.dbi_connection.indexes(
    #         schema_name=schema, unique=True, table_name=tabname
    #     )
    #     for index in indexes_info:
    #         if index["INDEX_NAME"] in ids:
    #             ids[index["INDEX_NAME"]] += "," + index["COLUMN_NAME"]
    #         else:
    #             ids[index["INDEX_NAME"]] = index["COLUMN_NAME"]
    #     # print(ids)
    #     return tables_info, cols, pks, fks, ids

    def get_tables(self, schema_name = None):
        """
        获取某个数据库表的表名列表
        返回数据格式为 list[dict] -> [{'schema','name','type','remarks'}]
        """
        tables_info = self.dbi_connection.tables(schema_name=schema_name)
        result = []
        for table in tables_info:
            result.append(
                {
                    'schema':table["TABLE_SCHEM"],
                    'name': table["TABLE_NAME"],
                    'type': table["TABLE_TYPE"],
                    'remarks': table["REMARKS"]
                }
            )
        return result

    # def get_table_names(self, schema_name=None):
    #     """
    #     'TABLE_SCHEM': 'SYSCAT', 'TABLE_NAME': 'VARIABLEAUTH', 'TABLE_TYPE': 'VIEW', 'REMARKS': None
    #     """
    #     table_type = ""
    #     tables_info = self.dbi_connection.tables(schema_name=schema_name)
    #     ###print(tables_info)
    #     tabs = []
    #     for table in tables_info:
    #         tabs.append(f"{table['TABLE_SCHEM']}.{table['TABLE_NAME']}")
    #     return tabs
