from dreema.security import Encrypt
from datetime import datetime, timedelta
from dreema.helpers import Json, getconfig
from dreema.redis import Redis
from dreema.responses import SysCodes,SysMessages

class Tokenizer:

    @staticmethod
    def ResponseCookie(name, value, max_age=60*60*24*30): #token valid for 30 days
        expires = int((datetime.now() + timedelta(seconds=max_age)).timestamp())
        return f"{name}={value}; Path=/; Max-Age={max_age}; Expires={expires}; HttpOnly; Secure; SameSite=None;Partitioned;"

    @staticmethod
    def generateAccessToken( prefix="du|", postfix="",expiryHours:int = 12 ):
        return Json({
            'token':f'{prefix}{Encrypt.getSecret()}{postfix}',
            'expiry': int((datetime.now() + timedelta(hours=expiryHours)).timestamp())
        })
    
