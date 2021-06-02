
from dbinterface.database_client import DataBaseClientFactory
import datetime
from dbinterface.utils import is_unsafe_sql, iter_count

class TestCase:
    def test_postgres(self):

        pg = DataBaseClientFactory.create(
            dbtype="postgres",
            host="localhost",
            port=5432,
            user="postgres",
            pwd="121113",
            database="postgres",
        )
        x = pg.read("select current_date")
        y = pg.copy_to_file("select * from lsflls", "/tmp/lsflls.txt")

        assert y == 100
        result = list(x)
        today = datetime.datetime.today()
        assert result[0][0].year == today.date().year

    def test_mysql(self):

        client = DataBaseClientFactory.create(
            dbtype="mysql",
            host="localhost",
            port=3306,
            user="aaron",
            pwd="aaron",
            database="information_schema",
        )
        x = client.read("select current_date()")
        result = list(x)
        today = datetime.datetime.today()
        assert result[0][0].year == today.date().year

    def test_mysql2(self):

        client = DataBaseClientFactory.create(
            dbtype="mysql",
            host="localhost",
            port=3306,
            user="aaron",
            pwd="aaron",
            database="information_schema",
        )
        x = client.read("show databases;")
        result = list(x)
        assert "information_schema" in [x[0] for x in result]

    def test_oracle(self):
        assert True

    def test_db2(self):

        client = DataBaseClientFactory.create(
            dbtype="db2",
            host="localhost",
            port=50000,
            user="db2inst1",
            pwd="121113",
            database="testdb",
        )
        x = client.read("select 'db2' from emp")
        result = list(x)
        assert result[0][0] == 'db2'
        client.write("create table if not exists SOMENZZ(id varchar(10),name varchar(20))",params=())
        tables = client.get_tables("db2inst1")
        assert "SOMENZZ" in [x[1] for x in tables]


    def test_is_unsafe_sql(self):
        sql = "delete from emp"
        assert is_unsafe_sql(sql)
        assert is_unsafe_sql(" ") == False
        assert is_unsafe_sql("select * from emp") == False

    def test_iter_count(self):
        count = iter_count("./setup.py")
        assert count == 90

