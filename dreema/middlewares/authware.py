from datetime import datetime
from typing import Union
from dreema.middlewares.dbware import DBware
from dreema.responses import SysCodes, SysMessages
from dreema.helpers.serialization import Json
from dreema.security.encrypt import Encrypt
from models._modelsList import getModel

class AuthWare:
    @staticmethod
    def adminAuth(data, token):
        for user in data:
            user = Json(user)
            if Encrypt.verifyHash(token, user.auth.token): 
               del user.auth
               del user.metadata
               return Json({'data':user, 'status':SysCodes.AUTH_SUCCESS, 'message':SysMessages.AUTH_SUCCESS})
            
        return Json({'data':None, 'status':SysCodes.INVALID_CREDS, 'message':'Unauthorized'})
            
    @staticmethod
    def studentsAuth(data, token):
        for user in data:
            user = Json(user)
            if Encrypt.verifyHash(token, user.auth.token):
               # check if user is verified
               if not user.metadata.verified:
                   return Json({ 'data':None, 'status':SysCodes.USER_NOT_VERIFIED, 'message':'User did not pass OTP'})
               
               del user.auth
               del user.metadata
               return Json({'data':user, 'status':SysCodes.AUTH_SUCCESS, 'message':SysMessages.AUTH_SUCCESS})
            
        return Json({'data':None, 'status':SysCodes.INVALID_CREDS, 'message':'Unauthorized'})
            

    @staticmethod 
    async def user( token , usertype = 1 ):
        
        # using bearer tokens
        token = token.get('value')
        if not token:
            return Json({'data':None, 'status':SysCodes.AUTH_FAILED, 'message':'Could not find access token'})
        
        # 
        if usertype == 1:
            mod = DBware()
            usr = await mod.read(model='creators', filters={'auth.token':token})
            if usr.status < 0:
                return Json({'data':None, 'status':SysCodes.INVALID_CREDS, 'message':SysMessages.INVALID_CREDS})
            
            del usr.data.auth
            return Json({'data':usr.data, 'status':SysCodes.INVALID_CREDS, 'message':"Authentication successful"})
        
        return Json({'data':None, 'status':SysCodes.INVALID_CREDS, 'message':'Auth setup not done'})
  