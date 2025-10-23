from dreema.helpers import Json, getenv
from codes import SysCodes, SysMessages

"""
    
    Use:   
        This class is the primary function to send responses to the client
        
    Parameters:
        it takes message, status, data, trace, custom and statuscode
        and returns a json serialized result
"""


def response(
    message=None,
    status= None,
    data=None,
    trace=None,
    custom=False,
    statuscode: int = 200,
    headers = {}
) -> dict:

    envCustom = (
        True
        if getenv("CUSTOM_RESPONSE") and "true" in getenv("CUSTOM_RESPONSE").lower()
        else False
    )

    if envCustom or custom or not status :
        return Json(
            {
                "data": message,
                "custom": True,
                "headers": headers
            }
        )

    return Json(
        {
            "data": data,
            "message": message,
            "status": status,
            "trace": trace,
            "statuscode": statuscode,
            "headers": headers
        }
    )
