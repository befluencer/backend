# code/scheduler/jobs.py

from datetime import datetime
from dreema.helpers.configurations import getconfig
from dreema.middlewares.dbware import DBware
from dreema.redis.actions import Redis
from dreema.utils import paystack
from dreema.utils.smsapi import SMSAPI
from dreema.utils.emailapi import EmailAPI
from dreema.scheduler.setup import scheduler, runAsyncJob
from dreema.utils.templates import MessageTemplates
import asyncio

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@scheduler.task(name="RepeatableJob")
def repeatableJob():
    
    async def checkPayment():
        redis = Redis()
        mid = DBware()
        res = await mid.read('payments', params={'limit':0},)
        
        # 
        if res.status < 0:
            return None
        
        # for all payments that is less than 24 hours, verify the transaction
        stack = paystack.PayStack()
        currtime = int(datetime.now().timestamp())

        for dt in res.data:
            hours = int(abs(currtime -  dt.dateCreated) /3600)

            # get time difference and status
            if hours > 1 or dt.status:
                continue

            if dt.paymentType == 1:
                # verify
                resPay = stack.verifyPay( reference = dt.initPayInfo.reference)
                if resPay.status < 0:
                    continue
            
            # 
            if dt.objType == 1:
                for _id in dt._objId:
                    obj = await redis.read(key=getconfig('redisKeys').NOTFSUBS, filters={'_id':_id,}, model=NotfSubsModel())
                    if obj.status < 0: continue

                    obj = obj.data
                    uni = await redis.read(key=getconfig('redisKeys').UNIS, filters={'_id':obj._institutionId}, model=UnisModel())
                    meds = await redis.read(key=getconfig('redisKeys').MEDIUMS, filters={'_id':obj._mediumId}, model=NotfMediums())

                    
                    # update the subscription details
                    obj.paid = 1
                    _id = obj._id
                    del obj._id
                    await redis.update(key=getconfig('redisKeys').NOTFSUBS, filters={'_id':_id,}, data=obj, model=NotfSubsModel())
                    usr = await redis.read(key=getconfig('redisKeys').STUDENTS, filters={'_id':obj._userId},  model=StudentModel())
                    

                    # send a notification
                    if uni.status < 0 or meds.status < 0:
                        continue
                    
                    if meds.data.name.lower() == "email":
                        ScheduleEmail.delay(message=MessageTemplates.emailNotfSuccess(institution=uni.data.name), destinations=obj.destination, subject="DreemUni Payment ✅🔊")
                    else:
                        ScheduleSMS.delay(MessageTemplates.smsNotfSuccess(institution=uni.data.name),destinations=obj.destination)

                    # send an sms to the user that subscribed
                    if usr.status > 0:
                        ScheduleSMS.delay(MessageTemplates.smsPaid(),destinations=[usr.data.phone])

            # credit buying
            if dt.objType == 2:
                pt = await mid.read('payments', filters={'_id':dt._id})
                if pt.data.status != 0:
                    continue
                
                usr = await redis.read(getconfig('redisKeys').STUDENTS,filters={'_id':dt._userId}, model=StudentModel())

                # update the credits
                if usr.status > 0:
                    credit = usr.data.get('credit', 0) + dt.get('credit', 0)

                    await redis.update(key=getconfig('redisKeys').STUDENTS,filters={'_id':dt._userId}, data={'credit':credit}, model=StudentModel())
                    ScheduleSMS.delay(MessageTemplates.creditTopUpSucess(),destinations=[usr.data.phone])

            if dt.objType == 3:
                pt = await mid.read('payments', filters={'_id':dt._id})
                if pt.data.status != 0:
                    continue
            
                sale = await mid.read('checker-orders',filters={'_id':dt._objId})

                if(sale.status > 0):
                    sale = sale.data
                    _checkerIds = sale._checkerIds

                    checkers = await mid.read('checkers',filters={'flag':1, 'level':sale.get('level', 1), '_id':{'op':'nin', 'value':_checkerIds} }, params={'limit':sale.get('quantity',1), 'bool':'and'},)

                    if checkers.status > 0:
                        # usr = usr.data
                        quantity = int(sale.quantity) 
                        checkers = [checkers.data] if quantity==1 else checkers.data

                        for checker in checkers:
                            _checkerIds.append(checker._id)
                            await mid.update('checkers', filters={'_id':checker._id},data={'_userId':dt._userId, 'flag':2})
                            await mid.update('checker-orders', filters={'_id':sale._id},data={'_checkerIds':_checkerIds, 'paid':True})

                            # send message to contacts
                            ScheduleSMS.delay(MessageTemplates.checkerBuy( checker.serialNumber, checker.pin, "WASSCE" if sale.get('level', 1) == 1 else "BECE"),destinations=sale.contact)
                else:
                    continue

            
            if dt.objType == 4:
                pt = await mid.read('payments', filters={'_id':dt._id})
                if pt.data.status != 0:
                    continue

                sale = await mid.read('form-orders', filters={'_id':dt._objId})

                # 
                if sale.status > 0:
                    sale = sale.data
                    _formIds = sale._formIds
                    uni = await mid.read('unis', filters={'_id':sale._uniId})
                    forms = await mid.read('forms', filters={'flag':1, '_uniId':sale._uniId, '_id':{'op':'nin', 'value':_formIds} }, params={'limit':sale.get('quantity',1), 'bool':'and'})

                    if forms.status > 0:
                        quantity = int(sale.quantity) 
                        forms = [forms.data] if quantity==1 else forms.data

                        for form in forms:
                            _formIds.append(form._id)

                            await mid.update('forms', filters={'_id':form._id},data={'_userId':dt._userId, 'flag':2} )
                            await mid.update('form-orders', filters={'_id':sale._id},data={'_formIds':_formIds, 'paid':True})
                            
                            # send message to contacts
                            ScheduleSMS.delay(MessageTemplates.checkerBuy( form.serialNumber, form.pin, uni.data.name, ),destinations=sale.contact)

                    
            # update the status of the payment itself
            dt.status = 1
            id = dt._id
            del dt._id
            await redis.update(key=getconfig('redisKeys').PAYMENTS, filters={'_id':id,}, data=dt, model=PaymentsModels())

        return "Completed"

    loop.run_until_complete(checkPayment())
    
@scheduler.task(name="UpdateNotf")
def notificationUpdate():
    async def send():
        redis = Redis()
        res = await redis.read(key=getconfig('redisKeys').NOTFSUBS, params={'limit':0}, model=NotfSubsModel())
        resIns = await redis.read(key=getconfig('redisKeys').NOTFINS, params={'limit':0}, model=NotfInsModel())
        resUni = await redis.read(key=getconfig('redisKeys').UNIS, params={'limit':0}, model=UnisModel())
        resMed = await redis.read(key=getconfig('redisKeys').MEDIUMS, params={'limit':0}, model=NotfMediums())
        resIns = resIns.data if resIns.status > 0 else []
        resMed = resMed.data if resMed.status > 0 else []
        resUni = resUni.data if resUni.status > 0 else []

        # find the number of hours of the time
        if res.status > 0:
            for notf in res.data:
                
                if notf.get("paid", 0) and notf.get('status',-1) == 0 and notf.totalSent < 5:
                    notfIns = [ ins for ins in resIns if ins._institutionId == notf._institutionId ]
                    notfMed = [ med for med in resMed if med._id == notf._mediumId ]
                    uni     = [ ins for ins in resUni if ins._id == notf._institutionId ]

                    if len(notfIns) == 0 or len(uni) == 0 or len(notfMed) == 0:
                        continue

                    notfMed = notfMed[0]
                    notfIns = notfIns[0]
                    uni = uni[0]

                    difference = int(datetime.now().timestamp()) - notf.dateadded
                    update = False 
                    match notf.totalSent:
                        case 0:
                            if difference > 1 * 60:  # 5 minutes
                                # send to SMS only
                                if notfMed.name == "SMS":
                                    message = f"""{uni.name} admission forms {'are now OUT!' if notfIns.get('isOpened', False) else 'was CLOSED on ' + str(datetime.fromtimestamp(notfIns.data.deadline).strftime('%Y-%m-%d %H:%M:%S')) + '. Once they are open, you will be able to purchase them.'} {"Available at the following banks: " + notfIns.data.banks if notfIns.data.get('banks') else ""} {'and at any regional post office.' if notfIns.data.get('postOffice', False) else ''}  {'You can also using the shortcode ' + notfIns.data.get('shortcode', '') + ' and follow the prompts.' if notfIns.data.get('shortcode', '') else 'Follow the purchase instructions provided.'} The form costs GHS{notfIns.data.get('amount', 'N/A')}.00."""
                                    ScheduleSMS.delay(message, [notf.destination])

                                    # add message to historys
                                    data = { '_subscriptionId': notf._id, 'message': message, '_userId':notf._userId, 'destination':notf.destination, 'sentAt': int(datetime.now().timestamp()), 'medium':notfMed.name, '_mediumId':notfMed._id, 'status': 0}
                                    await redis.create(getconfig('redisKeys').MESSAGES, model=MessageModel(), data=data)
                                    update = True
                        case 1:
                            if difference > 24 * 60 * 60:  # 24 hours
                                pass
                                # print('send guideline')
                                # update = True
                        case 2:
                            if difference > 2 * 24 * 60 * 60:  # 2 days
                                pass
                                # print('send official deadline')
                                # update = True
                        case 3:
                            if difference > 3 * 24 * 60 * 60:  # 2 days
                                pass
                                # print('3 days to official deadline')
                                # update = True
                        case 4:
                            if difference > 4 * 24 * 60 * 60:  # 2 days
                                pass
                                # print('Official deadline day')
                                # update = True
                        
                    if update:
                        data = {'totalSent': notf.totalSent + 1}
                        # update the status to 1 meaning we are done sending
                        if notf.totalSent == 4:
                            data = {'totalSent': notf.totalSent + 1, 'status': 1}
                        
                        await redis.update(key=getconfig('redisKeys').NOTFSUBS, filters={'_id':notf._id, }, data=data, model=NotfSubsModel() )  
    
    loop.run_until_complete(send())


@scheduler.task(name="CallbackScheduler")
def CallbackScheduler(job, *args, **kwargs):
    async def run():
        await job(*args, **kwargs)

    loop.run_until_complete(run())

@scheduler.task(name="ScheduleOTP")
def ScheduleOTP(code: str, phone: str = None, email: str = None):
    async def send():
        if phone:
            sms = SMSAPI()
            await sms.sendSignupOTP("", code, [phone])

        if email:
            email_api = EmailAPI()
            await email_api.sendEmailOTP(code, [email])

    loop.run_until_complete(send())


@scheduler.task(name="ScheduleSMS")
def ScheduleSMS(message:str, destinations:list, scheduler:str=""):
    async def send():
        sms = SMSAPI()
        sms = await sms.sendSMS(message=message, destinations=destinations, scheduleTime=scheduler)
    loop.run_until_complete(send())

@scheduler.task(name="ScheduleEmail")
def ScheduleEmail(message:str, destinations:list, subject=list):
    async def send():
        email = EmailAPI()
        await email.sendEmail( message=message, destinations=destinations, subject=subject)

    loop.run_until_complete(send())

