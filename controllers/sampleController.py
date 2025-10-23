from dreema.requests import Request
from dreema.responses import response
from dreema.responses import SysCodes, SysMessages
from models.appInfoModel import AppInfoModel
from dreema.redis import Redis
from dreema.helpers import getconfig

class SampleController:

    async def welcome(request: Request):
        mod = AppInfoModel()
        res = await mod.read()

        if res.status < 0:
            return await mod.create({'name':'Befluencer', 'colors':{'accent':'#4BC', 'secondary':'#CFA'}})
        
        return response(res)

        return response(message='Setup completed. Let us build!', status=SysCodes.SETUP_COMPLETED)