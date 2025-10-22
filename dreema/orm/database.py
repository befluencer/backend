from dreema.helpers import getenv, Json
from dreema.orm.mongo import connection as MongoConnector
from dreema.orm.mysql import connection as MySQLConnector
from dreema.orm.mongo import queries as MongoQueries
from dreema.orm.mysql import queries as MySQLQueries
from dreema.responses import SysCodes
from dreema.orm.events import EventsInterface


# WE MIGHT CONSIDER A SINGLETON TYPE
class Database(EventsInterface):
    _connection = None

    def __init__(self):
        # based on the credentials make the connection
        self.type = getenv("DB_TYPE")
        self.host = getenv("DB_HOST")
        self.port = getenv("DB_PORT")
        self.user = getenv("DB_USER")
        self.pwd = getenv("DB_PASSWORD")
        self.db = getenv("DB_NAME")
        self.tls = True if getenv("DB_USE_TLS") == "True" else False

    """
        TABLE or document from which operations 
        will be done injected into by the model
    """

    def setTable(self, tablename):
        self.tablename = tablename

    """
        Connecting to the database based on the 
        DBMS selected in mongo
    """

    async def connect(self):
        self.connFlag = False
        if self.type is None:
            return Json(
                {
                    "data": None,
                    "message": "Database type not found",
                    "status": SysCodes.ENV_READ_FAILED,
                }
            )

        if self.type not in ["mysql", "mongo"]:
            return Json(
                {
                    "data": None,
                    "message": "Dreema ORM only support mysql and mongodb for now",
                    "status": SysCodes.ENV_READ_FAILED,
                }
            )

        if (
            self.host is None
            or self.port is None
            or self.user is None
            or self.pwd is None
            or self.db is None
        ):
            return Json(
                {
                    "data": None,
                    "message": "Could not find database credentials in mysql",
                    "status": SysCodes.ENV_READ_FAILED,
                }
            )

        if self.type.lower() == "mysql":
            if not Database._connection or Database._connection.status < 0: 
                conn = MySQLConnector.Connector()
                Database._connection = await conn.connect(
                    host=self.host,
                    port=int(self.port),
                    user=self.user,
                    pwd=self.pwd,
                    db=self.db,
                    tls=self.tls,
                )

            if Database._connection.status < 0:
                return Database._connection

            self.dbms = MySQLQueries.Queries(self.connection, self.tablename)

        if self.type.lower() == "mongo":
            if not Database._connection or Database._connection.status < 0:
                conn = MongoConnector.Connector()
                Database._connection = await conn.connect(
                    host=self.host,
                    port=int(self.port),
                    user=self.user,
                    pwd=self.pwd,
                    db=self.db,
                    tls=self.tls,
                )
            
            if Database._connection.status < 0:
                return Database._connection

            self.dbms = MongoQueries.Queries(Database._connection, self.tablename)

    """
        all models implement this abstract READ method
        from which all READ operations are done regardless
        of the DBMS selected
    """

    async def read(self, filters=None, params=None):
        await self.connect()
        if Database._connection.status < 0:
            return Database._connection
        
        return await self.dbms.read(filters, params)

    """
        all models implement this abstract UPDATE method
        from which all UPDATE operations are done regardless 
        of the selected DBMS
    """

    async def update(self, filters=None, data=None, params=None):
        await self.connect()
        if Database._connection.status < 0:
            return Database._connection

        return await self.dbms.update(filters=filters, data=data, params=params)

    """
        all models implement this abstract DELETE method
        from which all DELETE operations are done regardless
        of the selected DBMS
    """

    async def delete(self, filters=None, params=None):
        await self.connect()
        if Database._connection.status < 0:
            return Database._connection

        return await self.dbms.delete(filters, params)

    """
        all models implement this abstract CREATE method
        from which all CREATE operations are done regardless
        of the selected DBMS
    """

    async def create(self, data, params=None):
        await self.connect()
        if Database._connection.status < 0:
            return Database._connection

        return await self.dbms.create(data, params)
