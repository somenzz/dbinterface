from dbinterface.database_client import DataBaseClientFactory
import datetime
from dbinterface.utils import is_unsafe_sql, iter_count


class TestCase:
    client = DataBaseClientFactory.create(
            dbtype="postgres",
            host="localhost",
            port=5432,
            user="postgres",
            pwd="121113",
            database="postgres",
        )

    def test_read(self):
        x = self.client.read("select current_date")
        result = list(x)
        today = datetime.datetime.today()
        assert result[0][0].year == today.date().year

    def test_write(self):
        count = self.client.write("insert into lsflls(zlsbz,sbh,sblx,jgm,zjlsh) values(%s,%s,%s,%s,%s)",params=( '0', '1104' , '0' ,'070667801' , 10730))
        assert count == 1

    def test_write_many(self):
        count = self.client.write_many("insert into lsflls values(%s,%s,%s,%s,%s)", params=(
                ( '0'     , '1104' , '0' ,'070667801' , 10730),
                ( '0'     , '1104' , '0' ,'070667801' , 10730),
                ( '0'     , '1104' , '0' ,'070667801' , 10730),
            )
        )
        assert count == 3

    def test_export(self):
        y = self.client.export(
            "select * from lsflls", params=(), file_path="/Users/aaron/tmp/lsflls1.txt"
        )
        assert y >= 100

        y = self.client.export(
            "select * from lsflls",
            params=(),
            file_path="/Users/aaron/tmp/lsflls2.txt",
            all_col_as_str=False,
        )
        assert y >= 100




    def test_is_unsafe_sql(self):
        sql = "delete from emp"
        assert is_unsafe_sql(sql)
        assert is_unsafe_sql(" ") == False
        assert is_unsafe_sql("select * from emp") == False

        assert is_unsafe_sql("select current time from emp") == False

    def test_iter_count(self):
        count = iter_count("./setup.py")
        assert count == 90


    def test_get_tables(self):
        tables_all = self.client.get_tables()
        tables = self.client.get_tables('information_schema')

        assert len(tables_all) > len(tables) > 0

    def test_isactivate(self):
        self.client.close()
        assert self.client.is_active() == False


    def test_copy_to_file(self):
        self.client.connect()
        count = self.client.copy_to_file("select * from lsflls","/tmp/lsflls_test.txt")
        assert count >= 100


    def test_copy_from_file(self):
        self.client.connect()
        count = self.client.copy_from_file("/Users/aaron/tmp/lsflls_test.txt",'lsflls',delimiter='0x02')
        assert count == 100
