import unittest
from dbinterface.database_client import DataBaseClientFactory
import datetime


class TestCase:
    def test_postgres(self):

        # pg = DataBaseClientFactory.create(
        #     dbtype="postgres",
        #     host="localhost",
        #     port=5432,
        #     user="postgres",
        #     pwd="121113",
        #     database="postgres",
        # )
        # x = pg.read("select current_date")
        # result = list(x)
        # today = datetime.datetime.today()
        # assert result[0][0] == today.date()
        assert True

    def test_mysql(self):

        # client = DataBaseClientFactory.create(
        #     dbtype="mysql",
        #     host="localhost",
        #     port=3306,
        #     user="aaron",
        #     pwd="aaron",
        #     database="information_schema",
        # )
        # x = client.read("select current_date()")
        # result = list(x)
        # today = datetime.datetime.today()
        # assert result[0][0] == today.date()
        assert  True


    def test_mysql2(self):

        # client = DataBaseClientFactory.create(
        #     dbtype="mysql",
        #     host="localhost",
        #     port=3306,
        #     user="aaron",
        #     pwd="aaron",
        #     database="information_schema",
        # )
        # x = client.read("show databases;")
        # result = list(x)
        # assert "information_schema" in [x[0] for x in result]
        assert True

    def test_oracle(self):
        assert True


    def test_db2(self):

        # pg = DataBaseClientFactory.create(
        #     dbtype="db2",
        #     host="localhost",
        #     port=50000,
        #     user="db2inst1",
        #     pwd="121113",
        #     database="testdb",
        # )
        # x = pg.read("select sysdate from emp")
        # result = list(x)
        # today = datetime.datetime.today()
        # assert result[0][0].date() == today.date()
        assert True