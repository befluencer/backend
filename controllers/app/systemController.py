from datetime import datetime
from dreema.middlewares import DBware
from dreema.requests import Request
from dreema.responses import response
from dreema.responses import SysCodes, SysMessages
from dreema.security import Encrypt, Tokenizer
from models.appInfoModel import AppInfoModel
from dreema.redis import Redis
from dreema.helpers import Json, getconfig

class SystemController:

    async def login(request:Request):
        body = await request.trimApplyRules({
            'email': 'required',
            'password': 'required',
        })
         
        if body.status < 0:
            return response(body, custom=True)
        
        
        # check if user is a brand
        body = body.data
        mod = DBware()

        # check if user is a brand or creator
        types = ['brands', 'creators']
        found = False
        for type in types:
            usr = await mod.read(model=type,filters={'email':(body.email).lower().strip()})
            if usr.status < 0:
                continue

            userinfo = usr.data
            if not Encrypt.verifyHash( body.password, userinfo.auth.password):
                return response(status=SysCodes.INVALID_CREDS, message=SysMessages.INVALID_CREDS)

            
            _id =  userinfo._id
            auth = Json(userinfo.get('auth', {}))
            rawtoken = Tokenizer.generateAccessToken(prefix=f"bf|{type}|")
            auth.token = rawtoken.token #Encrypt.hash(rawtoken.token)
            auth.tokenExpiry = rawtoken.expiry
            lastLogin = int(datetime.now().timestamp())

            print(usr)
            
            # update access token
            res = await mod.update( model=type, filters={'_id':_id}, data={'auth': auth, 'lastLogin':lastLogin})
            if res.status < 0:
                return response(status=SysCodes.OP_FAILED, message=SysMessages.OP_FAILED)
            
            # create and update cookie
            return response(data={
                '_id': _id,
                'name': userinfo.firstname,
                'email': userinfo.get('email', None),   
                'metadata': userinfo.metadata,
                'accessToken': rawtoken.token
            }, status=SysCodes.OP_COMPLETED)

        return response(status=SysCodes.INVALID_CREDS, message=SysMessages.INVALID_CREDS)