# connect to a database asynchronously
import aiomysql
from dreema.helpers import Json
from dreema.responses import SysCodes, SysMessages
import traceback


class Connector:
    def __init__(self) -> None:
        pass

    async def connect(
        self, host: str, port: int, user: str, pwd: str, db: str, tls: bool
    ):
        try:
            # SQL
            conn = await aiomysql.connect(
                host=host, port=port, user=user, password=pwd, db=db
            )
            return Json(
                {"data": {"connection": conn}, "status": SysCodes.DB_CONNECTION_SUCCESS}
            )
        except Exception as e:
            return Json(
                {
                    "data": None,
                    "message": SysMessages.DB_CONNECTION_FAILED,
                    "status": SysCodes.DB_CONNECTION_FAILED,
                    "trace": f" {e} {traceback.format_exc()}",
                }
            )

    async def disconnect(self):
        pass
