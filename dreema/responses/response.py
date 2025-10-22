import json
from dreema.helpers import getenv, getconfig
from dreema.logging import Logger
from datetime import datetime

"""
    Use: 
        Handle all outgoing responses from the library
"""

class Response:
    def __init__(self, request, send) -> None:
        self.request = request
        self.send = send

    async def response(self, content):
        """
        Parameters:
            dict (content): This is a JSON type sent from response in clientresponse.py

        Returns:
            dict: returns a response containing the various headers alongside
                  the necessary response passed.
        """

        statuscode = 200
        customHeaders = []

        if not getattr(content, "custom", None):
            statuscode = 200 if not getattr(content, "statuscode", None) else content.statuscode
            content.pop("statuscode", None)

            environment = getenv("ENVIRONMENT")
            if environment not in ["debug", "local"]:
                content.pop("trace", None)
        else:
            content = content.data

        # remove the header in the response
        headers = getattr(content, "headers", {}) or {}
        content.pop("headers", None)


        # Build default headers
        body = json.dumps(content).encode("utf-8")
        # origin = self.request.headers().origin if hasattr(self.request.headers(),"origin") else "https://dev.dreemuni.com"

        defaultHeaders = [
            (b"content-type", b"application/json"),
            (b"access-control-allow-origin", self.request.headers().origin.encode()),
            (b"access-control-allow-methods", b"GET, POST, PUT, DELETE, OPTIONS"),
            (b"access-control-allow-headers", b"Content-Type, Authorization"),
            (b"access-control-allow-credentials", b"true"),
            (b"content-length", str(len(body)).encode("utf-8")),
        ]

        # Add custom headers (e.g., Set-Cookie)
        for key, value in headers.items():
            print('running backwards')
            customHeaders.append((key.encode("latin-1"), value.encode("latin-1")))

        # logging
        # timedelta = (datetime.now() - self.request.entryTime()).total_seconds() * 1000
        # req = f' path-{self.request.path()} ip-{self.request.client().host} method-{self.request.method()} time{timedelta:.3f}ms'
        # Logger.info(message=req, filename='register')

        await self.send({
            "type": "http.response.start",
            "status": statuscode,
            "headers": defaultHeaders + customHeaders
        })
        await self.send({"type": "http.response.body", "body": body})
