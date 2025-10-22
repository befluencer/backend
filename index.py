from dreema.routing import Dispatcher
from dreema.requests import Request
from dreema.responses import Response, response
from dreema.responses import StatusCodes, SysCodes, SysMessages
from dreema.redis import Redis
import traceback
from context import AppContext


"""
    
    Use:
        Handles request and response information 
        to and fro the client
"""

# dispatch the routes
async def app(scope, receive, send):
    try:
        request = Request(scope, receive, send)

        #start the redis server
        request.redisClient = None
        dispatch = Dispatcher(request)
        exec = await dispatch.dispatchRoute()

        response = Response(request,send)
        await response.response(exec)

    except Exception as e:
        response = Response(send)
        await response.response(
            content={
                "data": None,
                "message": SysMessages.UNKNOWN_ERROR,
                "status": SysCodes.UNKNOWN_ERROR,
                "trace": f"{e} {traceback.format_exc()}",
                "statuscode": StatusCodes.FORBIDDEN,
            }
        )
