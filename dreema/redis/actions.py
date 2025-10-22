from datetime import datetime
import json
import operator
from dreema.helpers.configurations import getenv
from dreema.responses import SysCodes, SysMessages
from dreema.helpers import Json
import redis.asyncio as redis

class Redis:
    _instance = None
    
    def __init__(self, client=None):
        if not Redis._instance:
                Redis._instance = redis.Redis(
                    host=getenv("REDIS_HOST"),
                    port=int(getenv("REDIS_PORT")),
                    password=getenv("REDIS_PASSWORD"),
                    decode_responses=True
                )

        self.client = Json({
            'data': Redis._instance,
            'message': SysMessages.REDIS_SETUP_SUCCESS,
            'status': SysCodes.REDIS_SETUP_SUCCESS
        })
        
    async def internalUpdate(self, key, model):
        res = await model.read(params={'limit':0})
        value = res.data
        res = await self.set(key,value)
        return res

    async def delete(self, key):
        if self.client.status < 0:
            return Json({'data':None, 'message':f'{SysMessages.REDIS_READ_FAILED} - Could not get client', 'status':SysCodes.REDIS_READ_FAILED})
        
        try:
            res = await self.client.data.delete(key)
            if res == None:
                return Json({'data':None, 'message':f'{SysMessages.REDIS_KEY_NOT_FOUND}', 'status':SysCodes.REDIS_KEY_NOT_FOUND})
            
            # res = json.load(res)
            return Json({'data':res, 'message':f'{SysMessages.OP_COMPLETED}', 'status':SysCodes.OP_COMPLETED})
        except Exception as e:
            return Json({'data':None, 'message':f'{SysMessages.OP_FAILED} - {e}', 'status':SysCodes.OP_FAILED})

    async def read(self, key):
        if self.client.status < 0:
            return Json({'data':None, 'message':f'{SysMessages.REDIS_READ_FAILED} - Could not get client', 'status':SysCodes.REDIS_READ_FAILED})
        
        try:
            res = await self.client.data.get(key)
            if res == None:
                return Json({'data':None, 'message':f'{SysMessages.REDIS_KEY_NOT_FOUND}', 'status':SysCodes.REDIS_KEY_NOT_FOUND})
            
            dt = json.loads(res)
            return Json({'data':dt, 'message':f'{SysMessages.REDIS_READ_SUCCESS}', 'status':SysCodes.REDIS_READ_SUCCESS})
        except Exception as e:
            return Json({'data':None, 'message':f'{SysMessages.REDIS_READ_FAILED} - {e}', 'status':SysCodes.REDIS_READ_FAILED})
     
    async def create(self, key, value,expiry=0):
        if not isinstance(value, str):
            value = json.dumps(value)
        
        if self.client.status < 0:
            return Json({'data':None, 'message':f'{SysMessages.REDIS_CREATE_FAILED} - Could not get client', 'status':SysCodes.REDIS_CREATE_FAILED})
        
        try:
            if expiry > 0:
                await self.client.data.set(key, value, ex=expiry)
            else:
                await self.client.data.set(key, value)
            return Json({'data':None, 'message':f'{SysMessages.REDIS_CREATE_SUCCESS}', 'status':SysCodes.REDIS_CREATE_SUCCESS})
        except Exception as e:
            return Json({'data':None, 'message':f'{SysMessages.REDIS_CREATE_FAILED} - {e}', 'status':SysCodes.REDIS_CREATE_FAILED})
 
    async def update(self, key, value):
        return await self.set(key,value)