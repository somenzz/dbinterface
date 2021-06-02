import unittest
from dbinterface.database_client import DataBaseClientFactory
import datetime

class Test(unittest.TestCase):

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
        self.assertEqual(result[0][0], today.date())


    def test_mysql(self):

        pg = DataBaseClientFactory.create(
            dbtype="mysql",
            host="localhost",
            port=3306,
            user="aaron",
            pwd="aaron",
            database="information_schema",
        )
        x = pg.read("select current_date()")
        result = list(x)
        today = datetime.datetime.today()
        self.assertEqual(result[0][0], today.date())
