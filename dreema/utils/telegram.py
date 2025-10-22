import requests

from dreema.helpers.configurations import getenv
from dreema.helpers.serialization import Json


class Telegram:

    def sendTGDocument(self, caption, files):
        # Create a POST request to send the document
        url = f"https://api.telegram.org/bot{getenv('BOT_ID')}/sendDocument"
        data = {'chat_id': getenv('CHAT_ID'), 'caption':caption}
        file = {'document': (f'{files.name}.{files.ext}', open(files.fullPath, 'rb'))}
        try:
                response = requests.post(url, data=data, files=file)
                response_json = response.json()

                return Json({'status': 12, 'message':'Document sent to telegram', 'data':response_json})

        except Exception as e:
                return Json({'status':-12 , 'message':f'An error-occured [{e}]', 'data':None})