from dreema.orm.events import EventsInterface
from dreema.helpers.configurations import Json
from dreema.responses import SysCodes, SysMessages
from .querybuilder import QueryBuilder


class Queries(
    EventsInterface,
):

    def __init__(self, connector: dict, table: str) -> None:
        self.conn = connector.data.connection
        self.table = table

    async def create(self, data, params: dict = None):

        if not isinstance(data, dict) and not isinstance(data, list):
            return Json(
                {
                    "data": None,
                    "status": SysCodes.DB_CONNECTION_FAILED,
                    "message": "data must be a dictionary or a list for bulk create",
                }
            )

        try:
            builder = QueryBuilder(self.table)
            resultBuild = builder.createQueryBuilder(data=data, params=params)

            if resultBuild.status < 0:
                return resultBuild

            cursor = await self.conn.cursor()
            await cursor.execute(resultBuild.data.query, resultBuild.data.queryParams)
            await self.conn.commit()
            insertedId = (
                cursor.lastrowid
                if isinstance(data, dict)
                else cursor.lastrowid + len(data) - 1
            )

            return Json(
                {
                    "data": {"lastInsertedId": insertedId},
                    "status": SysCodes.CREATE_SUCCESS,
                    "message": SysMessages.CREATE_SUCCESS,
                }
            )

        except Exception as e:
            self.errorMessage = f"{type(e).__name__}: {e}"
            return Json(
                {
                    "data": None,
                    "status": SysCodes.CREATE_FAILED,
                    "message": self.errorMessage,
                }
            )

    async def read(self, filters: dict = None, params: dict = None):
        try:

            builder = QueryBuilder(self.table)
            resultBuild = builder.readQueryBuilder(filters=filters, params=params)

            if resultBuild.status < 0:
                resultBuild.message = SysMessages.DELETE_FAILED
                return resultBuild

            cursor = await self.conn.cursor()
            await cursor.execute(resultBuild.data.query, resultBuild.data.queryParams)
            description = cursor.description
            result = await cursor.fetchall()
            if result is None:
                return Json(
                    {
                        "data": None,
                        "status": SysCodes.NO_RECORD,
                        "message": SysMessages.NO_RECORD,
                    }
                )

            columns = [dt[0] for dt in description]
            data = [dict(zip(columns, row)) for row in result]

            if len(data) == 0:
                return Json(
                    {
                        "data": None,
                        "status": SysCodes.NO_RECORD,
                        "message": SysMessages.NO_RECORD,
                    }
                )

            return Json(
                {
                    "data": (
                        data[0] if params is None or params.get("limit") == 1 else data
                    ),
                    "status": SysCodes.READ_SUCCESS,
                    "message": SysMessages.READ_SUCCESS,
                }
            )
        except Exception as e:
            self.errorMessage = f"{type(e).__name__}: {e}"
            return Json(
                {
                    "data": None,
                    "status": SysCodes.READ_FAILED,
                    "message": self.errorMessage,
                }
            )

    async def delete(self, filters, params: dict = None):
        if not isinstance(filters, dict) and (not params or params.get("limit") != 0):
            return Json(
                {
                    "data": None,
                    "status": SysCodes.DB_CONNECTION_FAILED,
                    "message": "delete required filter(s). For bulk delete, set limit to 0",
                }
            )

        try:
            builder = QueryBuilder(self.table)
            resultBuild = builder.deleteQueryBuilder(filters=filters, params=params)

            if resultBuild.status < 0:
                return resultBuild

            cursor = await self.conn.cursor()
            await cursor.execute(resultBuild.data.query, resultBuild.data.queryParams)
            await self.conn.commit()
            return Json(
                {
                    "data": None,
                    "status": SysCodes.DELETE_SUCCESS,
                    "message": SysMessages.DELETE_SUCCESS,
                }
            )

        except Exception as e:
            return Json(
                {
                    "data": None,
                    "status": SysCodes.DELETE_FAILED,
                    "message": SysMessages.DELETE_FAILED,
                    "trace": f"{type(e).__name__}: {e}",
                }
            )

    async def update(self, filters=None, data=None, params: dict = None):

        if not isinstance(data, dict):
            return Json(
                {
                    "data": None,
                    "status": SysCodes.DB_CONNECTION_FAILED,
                    "message": "data and filter must be a dictionary",
                }
            )

        try:
            builder = QueryBuilder(self.table)
            resultBuild = builder.updateQueryBuilder(
                filters=filters, data=data, params=params
            )

            if resultBuild.status < 0:
                return resultBuild

            cursor = await self.conn.cursor()
            await cursor.execute(resultBuild.data.query, resultBuild.data.queryParams)
            await self.conn.commit()

            return Json(
                {
                    "data": None,
                    "status": SysCodes.UPDATE_SUCCESS,
                    "message": SysMessages.UPDATE_SUCCESS,
                }
            )

        except Exception as e:
            self.errorMessage = f"{type(e).__name__}: {e}"
            return Json(
                {
                    "data": None,
                    "status": SysCodes.UPDATE_FAILED,
                    "message": self.errorMessage,
                }
            )
