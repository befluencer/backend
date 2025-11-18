from dreema.requests import Request
from dreema.responses import response
from dreema.responses import SysCodes, SysMessages
from dreema.scheduler.jobs import ScheduleOTP
from dreema.utils.emailapi import EmailAPI
from dreema.redis import Redis
from dreema.security import Encrypt, Tokenizer
from dreema.helpers import Json
from datetime import datetime, timedelta
from dreema.utils import SMSAPI
from dreema.helpers import getconfig
import re
from dreema.middlewares import DBware


class MediaKitController:

    async def deleteKit(request:Request):
        user = await request.user('creator')
        if user.status < 0:
            return response(user,custom=True)
            
        mid = DBware()
        res = await mid.delete( model='mediakits', filters={'_creatorId':user.data._id})
        return response(res, custom=True)

    async def createKit(request:Request):
        body = await request.trimApplyRules({
            'data': 'required',
        })
        if body.status < 0:
            return response(body,custom=True)
        
        user = await request.user('creator')
        if user.status < 0:
            return response(user,custom=True)

        mid = DBware()
        ext = await mid.read( model='mediakits', filters={'_creatorId':user.data._id})

        body.data['_creatorId'] = user.data._id
        if ext.status < 0:
            res = await mid.create( model='mediakits', data=body.data)
            return response(res, custom=True)
        
        else:
            res = await mid.update( model='mediakits', filters={'_id':ext.data._id}, data=body.data)
            return response(res, custom=True)

    async def getKit(request:Request):
        user = await request.user('creator')
        if user.status < 0:
            return response(user,custom=True)

        mid = DBware()
        res = await mid.read( model='mediakits', filters={'_creatorId':user.data._id})
        return response(res, custom=True)