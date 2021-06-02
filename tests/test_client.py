import unittest
from dbinterface.database_client import DataBaseClientFactory
import datetime


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
        result = list(x)
        today = datetime.datetime.today()
        assert result[0][0] == today.date()

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
        assert result[0][0] == today.date()

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
