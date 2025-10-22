import http.client
import json

from codes import SysCodes,SysMessages
from dreema.helpers.configurations import getenv
from dreema.helpers.serialization import Json
import random,string
from models.thirdPModel import ThirdPModel

class MoniCliq:

    
    async def requestCode(self,quantity:int=1, level:int=1):
        model = ThirdPModel()
        url = 'evds2.misornu-backend.com'
        path=f'/api/requests?api_token={getenv("MONICLIQ")}'
        fullurl = f'{url}{path}'

        conn = http.client.HTTPSConnection(url)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Send GET request to verify endpoint
        global data
        count = 0

        try:

            while count < 10:
                part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                code = f"DU-{part1}-{part2}"
            
                body = {
                    "request_id": code,
                    'denomination_id': "WASSCE" if level == 1 else "BECE",
                    'quantity': quantity
                }

                
                conn.request("POST", f"{path}",body=json.dumps(body), headers=headers)
                res = conn.getresponse()
                status = res.status
                result =  res.read().decode('utf-8')
                data =Json(json.loads(result))
                count += 1
                _res = {
                    'party': 'monicliq',
                    'url': fullurl,
                    'request': body,
                    'response': data
                }
                
                await model.create(data=_res)
                if (status == 201 or status == 200) and data.status=="processed":
                    break

            return Json({
                'status': SysCodes.PAYMENT_VERIFIED_SUCCESS, #if status=="processed" else SysCodes.PAYMENT_VERIFIED_FAILED,
                'message': SysMessages.OP_COMPLETED,
                'data': data
            })
        except Exception as e:
            _res = {
                    'party': 'monicliq',
                    'url': fullurl,
                    'request': {},
                    'response': f'{e}'
            }

            await model.create(_res)
            return Json({
                'status': SysCodes.PAYMENT_VERIFIED_FAILED,
                'message': f'{e}',
                'data': None
            })
        
    def balance(self):
        model = ThirdPModel()
        url = 'evds2.misornu-backend.com'
        path=f'/api/applications/me?api_token={getenv("MONICLIQ")}'
        fullurl = f'{url}{path}'

        conn = http.client.HTTPSConnection(url)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Send GET request to verify endpoint
        global data
        count = 0

        try:
            conn.request("GET", f"{path}", headers=headers)
            res = conn.getresponse()
            status = res.status
            result =  res.read().decode('utf-8')
            data =Json(json.loads(result))
            balance = data.available_balance

            return Json({
                'status': SysCodes.READ_SUCCESS, #if status=="processed" else SysCodes.PAYMENT_VERIFIED_FAILED,
                'message': SysMessages.READ_SUCCESS,
                'data': {
                    'balance': balance
                }
            })
        except Exception as e:

            return Json({
                'status': SysCodes.PAYMENT_VERIFIED_FAILED,
                'message': f'{e}',
                'data': {
                    'balance': -1
                }
            })