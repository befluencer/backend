from dreema.requests import Request
from dreema.responses import response
from dreema.responses import SysCodes, SysMessages
from models.appInfoModel import AppInfoModel
from dreema.redis import Redis
from dreema.helpers import getconfig

class SampleController:

    async def welcome(request: Request):
        return response(message=SysMessages.SETUP_COMPLETED, status=SysCodes.SETUP_COMPLETED)