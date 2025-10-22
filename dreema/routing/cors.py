from dreema.helpers import getconfig
from dreema.requests import Request
from dreema.responses import SysCodes, SysMessages
from dreema.helpers import Json


class Cors:

    def __init__(self, request: Request):
        self.request = request
        self.extractConfig()

    def extractConfig(self):
        self.cors = getconfig("cors")

        # creating config if not created
        if self.cors == "" or not isinstance(self.cors, object):
            self.cors = Json({})
            self.cors.allowedOrigins = ["localhost", "127.0.0.1"]
            self.cors.allowedMethods = ["get", "post"]
            self.cors.allowCredentials = False
            self.cors.notAllowedHeaders = []
        else:

            # setting default values
            if not getattr(self.cors, "allowedOrigins", None):
                self.cors.allowedOrigins = ["localhost", "127.0.0.1"]
            else:
                self.cors.allowedOriginis = self.cors.allowedOrigins

            #
            if not getattr(self.cors, "allowedMethods", None):
                self.cors.allowedMethods = ["GET", "POST"]
            else:
                self.cors.allowedMethods = [
                    method.lower() for method in self.cors.allowedMethods
                ]

            #
            if not getattr(self.cors, "allowCredentials", None):
                self.cors.allowCredentials = False

            #
            if not getattr(self.cors, "notAllowedHeaders", None):
                self.cors.notAllowedHeaders = []
            else:
                self.cors.notAllowedHeaders = [
                    header.lower() for header in self.cors.notAllowedHeaders
                ]


    def process(self):
        # check for the origin
        method = self.request.method()
        headers = self.request.headers()

        try:
            if (
                "*" not in self.cors.allowedOrigins
                and headers.origin not in self.cors.allowedOrigins
            ):
                return Json(
                    {
                        "data": None,
                        "message": SysMessages.CORS_ORIGIN_NOT_ALLOWED,
                        "status": SysCodes.CORS_ORIGIN_NOT_ALLOWED,
                    }
                )

            if (
                "*" not in self.cors.allowedMethods
                and method.lower() not in self.cors.allowedMethods
            ):
                return Json(
                    {
                        "data": None,
                        "message": SysMessages.CORS_METHOD_NOT_ALLOWED,
                        "status": SysCodes.CORS_METHOD_NOT_ALLOWED,
                    }
                )

            if set(headers) & set(self.cors.notAllowedHeaders):
                return Json(
                    {
                        "data": None,
                        "message": SysMessages.CORS_HEADER_NOT_ALLOWED,
                        "status": SysCodes.CORS_HEADER_NOT_ALLOWED,
                    }
                )

            return Json(
                {
                    "data": None,
                    "message": SysMessages.CORS_NO_ISSUES,
                    "status": SysCodes.CORS_NO_ISSUES,
                }
            )
        except Exception as e:
            return Json(
                {
                    "data": None,
                    "message": f"{SysMessages.CORS_ERRORS} {e}",
                    "status": SysCodes.CORS_ERRORS,
                }
            )
