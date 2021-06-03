from dbinterface.database_client import DataBaseClientFactory
import datetime
from dbinterface.utils import is_unsafe_sql, iter_count


class TestCase:

    client = DataBaseClientFactory.create(
        dbtype="mysql",
        host="localhost",
        port=3306,
        user="aaron",
        pwd="aaron",
        database="kjt",
    )

    def test_read(self):
        x = self.client.read("select current_date()")
        result = list(x)
        today = datetime.datetime.today()
        assert result[0][0].year == today.date().year

        x = self.client.read("show databases;")
        result = list(x)
        assert "kjt" in [x[0] for x in result]

    def test_write(self):
        count = self.client.write(
            "create table if not exists tmp_test_table(id varchar(10), name varchar(20))",
            params=(),
        )
        count2 = self.client.write(
            "insert into tmp_test_table values(%s, %s)", ("1", "aaron")
        )
        assert count2 == 1

        count3 = self.client.write_many(
            "insert into tmp_test_table values(%s, %s)",
            (("1", "aaron"), ("1", "aaron")),
        )
        assert count3 == 2

    def test_export(self):

        y = self.client.export(
            "select * from information_schema.TABLES",
            params=(),
            file_path="/Users/aaron/tmp/mysql_tables.txt",
            delimeter="0x02",
            quote="0x03",
            all_col_as_str=False,
        )
        assert y > 0

        y = self.client.export(
            "select * from information_schema.TABLES",
            params=(),
            file_path="/Users/aaron/tmp/mysql_tables2.txt",
            delimeter="0x02",
            quote="0x03",
            all_col_as_str=True,
        )
        assert y > 0

    def test_get_tables(self):
        tables_all = self.client.get_tables()
        tables = self.client.get_tables('information_schema')
        assert len(tables_all) > len(tables) > 0

    def test_isactivate(self):
        assert self.client.is_active()
        self.client.close()
        assert self.client.is_active() == False
