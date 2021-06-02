from .db2_client import Db2Client
from .mysql_client import MysqlClient
from .postgres_client import PostgresClient


class DataBaseClientFactory:
    """
    dbtype: mysql,db2,postgres
    """

    @classmethod
    def create(cls, dbtype, host, port, user, pwd, database, **kwargs):
        _client = None
        if dbtype == "mysql":
            _client = MysqlClient()

        elif dbtype == "db2":
            _client = Db2Client()

        elif dbtype == "postgres":
            _client = PostgresClient()

        else:
            pass

        _client.init(host, port, user, pwd, database, **kwargs)
        _client.connect()
        return _client
