from views.endpoints import routes
from dreema.requests import Request
from dreema.responses import response
from dreema.responses import SysCodes, StatusCodes, SysMessages
import traceback
from .cors import Cors

"""
    
    Use:
        Core routing for dispatching routes from the views
"""


class Dispatcher:
    ROUTES = []
    ROUTEMAPS = {}

    def __init__(self, request: Request) -> None:
        self.routes = routes
        self.request = request

    async def dispatchRoute(self):

        try:
            path = self.request.path().rstrip("/")
            method = self.request.method()

            # checking for CORS
            cors = Cors(self.request)
            cors = cors.process()
            if cors.status < 0:
                return response(cors, custom=True)

            # check for path, methods and functions
            allroutes = []
            if not Dispatcher.ROUTES:
                for route in routes:
                    # if its is a route group
                    if isinstance(route, list):
                        for r in route:
                            r.path = r.path.rstrip("/")
                            r.path = r.path.replace("//", "/")

                            allroutes.append(r)
                        continue
                    else:
                        route.path = route.path.rstrip("/")
                        route.path = route.path.replace("//", "/")
                        allroutes.append(route)

                Dispatcher.ROUTES = allroutes

            # search for the route
            router = Dispatcher.ROUTEMAPS[path] if path in Dispatcher.ROUTEMAPS else None
            if not router:
                for route in Dispatcher.ROUTES:
                    if route is None or path != route.path:
                        continue

                    if method not in route.method:
                        return response(
                            statuscode=StatusCodes.METHOD_NOT_ALLOWED,
                            message=SysMessages.UNALLOWED_METHOD,
                            status=SysCodes.UNALLOWED_METHOD,
                        )

                    router = route
                    Dispatcher.ROUTEMAPS[path] = route

            # use the maper to
            if router:
                if not callable(router.handler):
                    return response(
                        status=SysCodes.ENDPOINT_FUNC_FAIL,
                        statuscode=StatusCodes.BAD_REQUEST,
                    )

                res = await router.handler(self.request)
                return res

            # Send a 404 response if no matching route is found
            return response(
                message=SysMessages.ENDPOINT_NOT_FOUND,
                status=SysCodes.ENDPOINT_NOT_FOUND,
                statuscode=StatusCodes.NOT_FOUND,
            )

        except Exception as e:
            return response(
                message=SysMessages.UNKNOWN_ERROR,
                status=SysCodes.UNKNOWN_ERROR,
                trace=f"{e} {traceback.format_exc()}",
            )
