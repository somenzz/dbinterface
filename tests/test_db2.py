from dbinterface.database_client import DataBaseClientFactory
import datetime
from dbinterface.utils import is_unsafe_sql, iter_count


class TestCase:

    client = DataBaseClientFactory.create(
        dbtype="db2",
        host="localhost",
        port=50000,
        user="db2inst1",
        pwd="121113",
        database="testdb",
    )


    def test_get_tables(self):
        tables_all = self.client.get_tables()
        tables = self.client.get_tables("SYSCAT")
        assert len(tables_all) > len(tables)

    def test_read(self):
        x = self.client.read("select 'db2' from emp")
        result = list(x)
        assert result[0][0] == "db2"

    def test_write_create(self):
        self.client.write(
            "create table if not exists SOMENZZ(id varchar(10),name varchar(20))",
            params=(),
        )
        tables = self.client.get_tables("db2inst1")
        assert "SOMENZZ" in [x['name'] for x in tables]

    def test_export(self):
        y = self.client.export(
            "select * from syscat.tables",
            params=(),
            file_path="/Users/aaron/tmp/tables.txt",
            all_col_as_str=False,
        )
        assert y > 0

        y = self.client.export(
            "select * from syscat.tables",
            params=(),
            file_path="/Users/aaron/tmp/tables.txt",
            all_col_as_str=True,
        )
        assert y > 0

    def test_write(self):
        count = self.client.write(
            sql="insert into SOMENZZ values(?,?)", params=(1, "aaron")
        )
        assert count == 1
        count = self.client.write_many(
            sql="insert into SOMENZZ values(?,?)",
            params=(("1", "aaron"), ("2", "brant")),
        )
        assert count == 2

    def test_isactivate(self):
        assert self.client.is_active()
        self.client.close()
        assert not self.client.is_active()

    def test_init(self):
        self.client.init(
            host="localhost",
            port=50000,
            user="db2inst1",
            pwd="121113",
            database="testdb",
        )
        assert True