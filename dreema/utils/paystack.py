import http.client
import json

from codes import SysCodes
from dreema.helpers.configurations import getenv
from dreema.helpers.serialization import Json

class PayStack:

    def verifyPay(self,reference:str=None):
        try:
            conn = http.client.HTTPSConnection("api.paystack.co")

            headers = {
                'Authorization': f'Bearer {getenv("PAYSTACK_KEY")}',  # Your secret key in environment
                'Content-Type': 'application/json'
            }

            # Send GET request to verify endpoint
            conn.request("GET", f"/transaction/verify/{reference}", headers=headers)
            res = conn.getresponse()
            data = res.read()

            # Construct a consistent response similar to your initialization return
            resverf = Json(json.loads(data))
            status = resverf.data.get('status', "abandoned")
            message = resverf.get('message', '')
            transaction_data = resverf.get('data', None)

            return Json({
                'status': SysCodes.PAYMENT_VERIFIED_SUCCESS if status=="success" else SysCodes.PAYMENT_VERIFIED_FAILED,
                'message': message,
                'data': transaction_data
            })
        except Exception as e:
            return Json({
                'status': SysCodes.PAYMENT_VERIFIED_FAILED,
                'message': f'{e}',
                'data': None
            })

    def momoPay(self, email:str, phone:str, amount:float, provider:str, callback:str):
        conn = http.client.HTTPSConnection("api.paystack.co")

        payload = json.dumps({
            "email": email,
            "fullname": 'dreemUni user',
            "phone":"0240240241",
            "amount": int(amount * 100),  # Convert GHS to pesewas
            "channels": ["mobile_money"],
            "currency": "GHS",
            "callback_url": callback,
            "mobile_money": {
                "phone": phone,
                "provider": provider.lower()
            }
        })

        headers = {
            'Authorization': f'Bearer {getenv("PAYSTACK_KEY")}',  # Replace with your secret key
            'Content-Type': 'application/json'
        }

        conn.request("POST", "/transaction/initialize", payload, headers)
        res = conn.getresponse()
        data = res.read()

        # Parse and return JSON response
        res = Json(json.loads(data))
        return Json({'status':SysCodes.PAYMENT_INITIALIZED if res.status else SysCodes.PAYMENT_INIT_FAILED, 'message':res.message, 'data':res.data})
