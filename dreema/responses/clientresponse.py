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
    message=SysMessages.OP_COMPLETED,
    status: int = SysCodes.OP_COMPLETED,
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

    if envCustom or custom:
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
