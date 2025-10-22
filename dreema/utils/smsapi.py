import http.client as httpClient
from dreema.helpers import Json  
from dreema.responses import SysCodes,SysMessages
from dreema.helpers import getenv
from dreema.security import Encrypt
from .templates import MessageTemplates
import json

class SMSAPI:
    
    async def sendSMS(self, message, destinations:list, scheduleTime:str="", sendername:str='DreemUni'):
        try: 
            host = 'api.smsonlinegh.com'
            requestURI = 'http://api.smsonlinegh.com/v5/message/sms/send'
            apiKey = getenv('SMSKEY')

            headers = {}
            headers['Host'] = host
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = 'application/json'
            headers['Authorization'] = f'key {apiKey}'

            # message data
            msgData = {}
            msgData['text'] = message
            msgData['type'] = 0
            msgData['sender'] = sendername
            msgData['destinations'] = destinations

            if(scheduleTime):
                if scheduleTime:
                    msgData['schedule'] = {
                        'dateTime': scheduleTime
                    }



            httpConn = httpClient.HTTPConnection(host)
            httpConn.request('POST', requestURI, json.dumps(msgData), headers)

            # get the reponse
            response = httpConn.getresponse()

            if response.status == 200:
                # check the status
                return Json({'data':None, 'message':SysMessages.OP_COMPLETED, 'status':SysCodes.OP_COMPLETED})
            return Json({'data':None, 'message':f'{SysMessages.OP_FAILED} {response.reason}', 'status':SysCodes.OP_FAILED})
        except Exception as e:
             return Json({'data':None, 'message':f'{SysMessages.OP_FAILED} - {e}' , 'status':SysCodes.OP_FAILED})
             
    async def sendSignupOTP(self, username, code, destination):
        message = MessageTemplates.smsOTP(username, code)
        res = await self.sendSMS(message, destinations=destination)
        return res


    