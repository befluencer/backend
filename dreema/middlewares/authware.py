from datetime import datetime
from typing import Union
from backend.codes import SysCodes, SysMessages
from backend.dreema.helpers.serialization import Json
from backend.dreema.security.encrypt import Encrypt
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
    async def user( request , types ):
        
        # browser cookie
        headers = request.headers()
        tokens = Json(headers).get("cookie","").replace(" ","")
        tokens = tokens.split(";")
        
        tokensdict = {}
        for token in tokens:
            if token:
                key, value = token.split('=')
                tokensdict[key] =  value

        # using bearer tokens
        
        # compare request tokens or headers
        # if Encrypt.verifyHash(token, user.auth.token):
            # do something

        return Json({'data':None, 'status':SysCodes.INVALID_CREDS, 'message':'Auth setup not done'})
  