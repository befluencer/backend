from datetime import datetime
import requests
from dreema.middlewares import DBware
from dreema.requests import Request
from dreema.responses import response
from dreema.responses import SysCodes, SysMessages
from dreema.security import Encrypt, Tokenizer
from models.appInfoModel import AppInfoModel
from dreema.redis import Redis
from dreema.helpers import Json, getconfig

class LogosController:

    async def getLogos(request:Request):
        body = await request.applyRules({
            'query': 'required,str',
        }, request.params())

        if body.status < 0:
            return response(body, custom=True)
        

        body = body.data
        print(body.query)
        mod = DBware()
        res = await mod.read(model='app-logos', params={'limit':0})
        if res.status  > 0:
            _log = []
            for logo in res.data:
                if body.query.lower() in logo['domain'].lower():
                    _log.append(logo)
            
            if len(_log) > 0:
                return response(data=_log, status=SysCodes.OP_COMPLETED, message=SysMessages.OP_COMPLETED)

        if res.status < 0 or len(_log) == 0:
            # here we make a request to the backend and get their logos
            url = f'https://api.logo.dev/search?q={body.query}'
            
            # Get authorization header from incoming request
            headers = {}
            # auth_header = request.headers().get('authorization') or request.headers().get('')
            # if auth_header:
            headers['Authorization'] = 'sk_NySxTEHLRku8WVvrKrvEiQ'
            
            http_response = requests.get(url, headers=headers)
            if http_response.status_code != 200:
                return response(status=SysCodes.OP_FAILED, message=SysMessages.OP_FAILED, trace=http_response.text)

            data = http_response.json()
            actualLogos = []
            

            print("searching from database", data)

            if res.status > 0:
                for logo in data:
                    for appLg in res.data:
                        if logo['name'] != appLg['name']:
                            actualLogos.append(logo)
                            break
            
            res = await mod.create(model='app-logos', data=data)
            print("created in database", res)
            return response(data=data, custom=True)

        return response(message="Could not find brand", status=SysCodes.NO_RECORD)