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


class AuthController:

    async def getme(request:Request):
        user = await request.user('brand')

        if user.status < 0:
            return response(user,custom=True)

        del user.data.auth
        return response(user, custom=True)

    async def checkUserExists(request:Request):
        body = await request.body()
        mid = DBware()
      
        if body.get('email', None):
            res = await mid.read('brands', filters={'email':body.email,})
            if res.status > 0:
                return response(message='Email already used',status=SysCodes.OP_FAILED)

        return response(message="Does not exist", status=SysCodes.OP_SUCCESS)

    async def updateUser(request:Request):
        body = await request.body()
        user = await request.user('brand')

        if user.status < 0:
            return response(user, custom=True)
        
        mid = DBware()    
        if body.get('name',None):
            await mid.update('brands', filters={'_id':user.data._id}, data={'name': body.name})

        if body.get('phone',None):
            await mid.update('brands', filters={'_id':user.data._id}, data={'phone': body.phone})

        if body.get('email',None):
            await mid.update('brands', filters={'_id':user.data._id}, data={'email': body.email})


        if body.get('onboardingStep',"None") != "None":
            await mid.update('brands', filters={'_id':user.data._id}, data={'metadata.onboardingSteps': body.tourStep})

        return response(message=SysMessages.UPDATE_SUCCESS)

    async def resetPassword(request:Request):
        body = await request.trimApplyRules({
            'email': 'required',
            'password': 'required',
        })
         
        if body.status < 0:
            return response(body, custom=True)
        
        body = body.data
        pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$')
        match = bool(pattern.match(body.password))

        if not match:
            return response(message="Password must be 8+ characters with at least one uppercase, lowercase, number and symbol", status=SysCodes.OP_FAILED)

        mid = DBware()
        res = await mid.read('brands',filters={'email':(body.email).lower().strip()})

        if res.status < 0:
            return response(status=SysCodes.INVALID_CREDS, message=SysMessages.INVALID_CREDS)
        
        # check if the user is verified
        userinfo = res.data
        if not userinfo.auth.otpStatus:
            return response(message="Unverified identity", status=SysCodes.OP_FAILED)

        # verify password
        _id = userinfo._id
        userinfo.auth.password = Encrypt.hash(body.password)
        del userinfo._id

        res = await mid.update('brands',filters={'_id':_id}, data=userinfo)
        return response(res, custom=True)
       
    async def requestOTP(request:Request=None):
        body = await request.trimApplyRules({
                'email': 'required',
        })

        if body.status < 0:
            return response(body, custom=True)
        
        body = body.data

        # check if the school name or cod exists
        mid = DBware()
        usr = await mid.read(model='brands',filters={'email':(body.email).lower(),})
        
        if usr.status < 0:
            return response(status=SysCodes.NO_RECORD, message="User not found")

        # check last request and send
        userinfo = Json(usr.data)
        if( userinfo.auth.get('otpLast',None) and userinfo.auth.otpLast > int(datetime.now().timestamp())):
            return response(message="Wait 60seconds after last request", status=SysCodes.OP_FAILED)

        code = Encrypt.generateRandom(6,1)
        email_api = EmailAPI()
        email = await email_api.sendEmailOTP(code, [body.email])
        print(email)
    
        # update info
        auth = Json(userinfo.get('auth', {}))
        auth.otp = Encrypt.hash(code)
        auth.otpExpiry = int((datetime.now() + timedelta(hours=1)).timestamp())
        auth.otpLast  = int((datetime.now() + timedelta(seconds=10)).timestamp())
        auth.otpStatus = False
        
        res = await mid.update( 'brands', filters={'_id':userinfo._id}, data={'auth':auth})
        return response(res, custom=True)
    
    async def verifyOTP(request:Request):
        body = await request.trimApplyRules({
            'email': 'required',
            'otp': 'required',
        })
         
        if body.status < 0:
            return response(body, custom=True)
        
        body = body.data
        
        mid = DBware()
        usr = await mid.read(model='brands',filters={'email':(body.email).lower().strip(),})
        
        if usr.status < 0:
            return response(status=SysCodes.NO_RECORD, message="User not found")

        # check token correctness and expiry
        userinfo = usr.data
        currtime = int(datetime.now().timestamp())
        if userinfo.auth.otpStatus:
            return response(status=SysCodes.OP_SUCCESS, message='User already verified')

        if not Encrypt.verifyHash( body.otp, userinfo.auth.otp):
            return response(status=SysCodes.AUTH_INVALID, message='Invalid OTP')
        
        if currtime > userinfo.auth.otpExpiry:
            return response(status=SysCodes.AUTH_EXPIRED, message='OTP has expired')
        
        # update necessary info on user
        await mid.update( 'brands', filters={'_id':userinfo._id}, data={'auth.otpStatus':True, 'metadata.verified':True})
        return response(status=SysCodes.OP_SUCCESS, message='User verified')

    async def addBrand(request:Request):
        body = await request.trimApplyRules({
            'email' : 'required',
            'password': 'required',
            'firstname': 'required',
            'lastname': 'required'
        })

        if body.status < 0:
            return response(body, custom=True)
        
        #verify password
        body = body.data
        pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$')
        match = bool(pattern.match(body.password))

        if not match:
            return response(message="Password must be 8+ characters with at least one uppercase, lowercase, number and symbol", status=SysCodes.OP_FAILED)

        # check if the school name or cod exists
        mid = DBware()

        # check email and phone
        if body.get('email',None):
            body.email = body.email.lower().strip()
            res = await mid.read('brands',filters={'email':body.email})
            creator = res = await mid.read('creators',filters={'email':body.email})

            if res.status > 0 or creator.status > 0:
                return response(data=None, status=SysCodes.ALREADY_EXISTS, message='Email already used')

        # create an account -> remember to check password strength
        auth = Json({})
        token = Tokenizer.generateAccessToken(prefix="bf|brand|")
        rawtoken = token.token
        token.token = rawtoken 
        passwordhash = Encrypt.hash(body.password)
        auth.password = passwordhash
        auth.token = token.token
        auth.tokenExpiry = token.expiry
        del body.password

        # add some metadata
        metadata = Json({})
        metadata.verified = False
        metadata.datecreated = int(datetime.now().timestamp())

        body.auth = auth
        body.metadata = metadata

        res = await mid.create('brands', data=body)
        if res.status < 0:
            return response(res, custom=True)
        
        # cookie = Tokenizer.ResponseCookie("student",rawtoken)
        request.setNewBody({'email':body.email})
        await AuthController.requestOTP(request)

        return response(data={
            '_id':res.data._id,
            'name': body.firstname,
            'email': body.get('email', None),
            'accessToken': rawtoken
        })

