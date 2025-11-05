from email.utils import formataddr
from dreema.helpers import Json  
from dreema.responses import SysCodes,SysMessages
from dreema.helpers import getenv
from dreema.security import Encrypt
from .templates import MessageTemplates
import smtplib
from email.message import EmailMessage
from dreema.helpers.configurations import getconfig, getenv

class EmailAPI: 
    async def sendEmail(self, message, destinations:list, subject:str="DreemUni"):
        try:
            desties = [destinations] if isinstance(destinations, str) else destinations
            with smtplib.SMTP(getenv("MAIL_HOST"), int(getenv("MAIL_PORT"))) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(getenv("MAIL_SOURCE"), getenv("MAIL_PASSWORD"))

                for des in desties:
                    msg = EmailMessage()
                    msg['Subject'] = subject
                    msg['From'] = formataddr(("Befluencer", getenv("MAIL_SOURCE")))
                    msg['To'] = des
                    msg.set_content("This email contains HTML content.")
                    msg.add_alternative(message, subtype='html')

                    smtp.send_message(msg)

            return Json({'data':None, 'status':SysCodes.OP_SUCCESS, 'message':SysMessages.OP_SUCCESS})
        except Exception as e:
            return Json({'data':None, 'status':SysCodes.OP_FAILED, 'message':SysMessages.OP_FAILED, 'trace':f'{e}'})
        

    async def sendEmailOTP(self, code:str, destination:list, subject="Befluencer Account Verification✅"):
        message = MessageTemplates.emailOTP(code)
        res = await self.sendEmail(message=message, destinations=destination, subject=subject)
        return res