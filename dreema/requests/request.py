from datetime import datetime
from dreema.helpers import Json
from dreema.responses import SysCodes, SysMessages
from dreema.files import FileParser
from urllib.parse import parse_qs
import json
from dreema.security import Tokenizer


"""
    
    Use:
            Manages all request information from clients and the server
"""


class Request:
    def __init__(self, scope, receive, send) -> None:
        """
        Receives the scope, receive and send from the uvicorn server
        """
        self.scope = scope
        self.receive = receive
        self.send = send
        self._body = None

    def setNewBody(self, data:dict):
        self._body = Json(data)

    async def user(self, types=""):
        user = await Tokenizer.authUser(self, types=types)
        return user
    
    async def applyRules(self, rules: dict, body: dict = None):
        """
        Use:
            Useful for validating request body checking for
            parameters like required property, and variable types

        Parameters:
            Rules to be checked

        Returns:
            json: A json serialized response containing the body
        """
        body = body if body else await self.body()
        systemrules = ["required", "int", "str", "float", "list", "bool"]

        for key, rule in rules.items():
            indRules = rule.replace(" ", "").split(",")
            for r in indRules:
                if body.get(key, "None") == "None" :
                    return Json(
                        {
                            "data": None,
                            "message": f"{key} is required",
                            "status": SysCodes.ATTR_MISSING,
                        }
                    )

                try:
                    index = systemrules.index(r)
                    match (index):
                        case 1:
                            if not isinstance(body.get(key, None), int):
                                return Json(
                                    {
                                        "status": SysCodes.ATTR_MISSING,
                                        "data": None,
                                        "message": f"{key} must be of type int",
                                    }
                                )
                        case 2:
                            if not isinstance(body.get(key, None), str):
                                return Json(
                                    {
                                        "status": SysCodes.ATTR_MISSING,
                                        "data": None,
                                        "message": f"{key} must be of type str",
                                    }
                                )
                        case 3:
                            if not isinstance(body.get(key, None), float):
                                return Json(
                                    {
                                        "status": SysCodes.ATTR_MISSING,
                                        "data": None,
                                        "message": f"{key} must be of type float",
                                    }
                                )
                        case 4:
                            if not isinstance(body.get(key, None), list):
                                return Json(
                                    {
                                        "status": SysCodes.ATTR_MISSING,
                                        "data": None,
                                        "message": f"{key} must be of type list",
                                    }
                                )
                        case 5:
                            if not isinstance(body.get(key, None), bool):
                                return Json(
                                    {
                                        "status": SysCodes.ATTR_MISSING,
                                        "data": None,
                                        "message": f"{key} must be of type bool",
                                    }
                                )
                except Exception as e:
                    return Json(
                        {
                            "status": SysCodes.ATTR_MISSING,
                            "data": None,
                            "message": f"{r} request rule not applicable",
                            "trace": f'An error occured - {e}',
                        }
                    )

        return Json(
                        {
                            "status": SysCodes.ATTR_FOUND,
                            "data": body,
                            "message": SysMessages.ATTR_FOUND
                        }
                    )

    async def trimApplyRules(self, rules: dict, body: dict = None):
        """
            Use:
                Useful for validating request body checking for 
                parameters like required property, and variable types
                    
            Parameters:
                Rules to be checked
                
            Returns:
                json: A json serialized response containing the body
        """
        body = body if body else await self.body()
        systemrules = ["required",  "int", "str", "float", "list", "bool","nullable",]
        checkedkeys = []

        for key, rule in rules.items():
            checkedkeys.append(key)
            indRules = rule.replace(" ", "").split(",")

            if(not body.get(key, None) and "nullable" in indRules):
                continue

            for r in indRules:
                if body.get(key, "None") == "None" :
                    return Json(
                        {
                            "data": None,
                            "message": f"{key} is required",
                            "status": SysCodes.ATTR_MISSING,
                        }
                    )

                try:
                    index = systemrules.index(r)
                    match (index):
                        case 1:
                            if not isinstance(body.get(key, None), int):
                                return Json(
                                    {
                                        "status": SysCodes.ATTR_MISSING,
                                        "data": None,
                                        "message": f"{key} must be of type int",
                                    }
                                )
                        case 2:
                            if not isinstance(body.get(key, None), str):
                                return Json(
                                    {
                                        "status": SysCodes.ATTR_MISSING,
                                        "data": None,
                                        "message": f"{key} must be of type str",
                                    }
                                )
                        case 3:
                            if not isinstance(body.get(key, None), float):
                                return Json(
                                    {
                                        "status": SysCodes.ATTR_MISSING,
                                        "data": None,
                                        "message": f"{key} must be of type float",
                                    }
                                )
                        case 4:
                            if not isinstance(body.get(key, None), list):
                                return Json(
                                    {
                                        "status": SysCodes.ATTR_MISSING,
                                        "data": None,
                                        "message": f"{key} must be of type list",
                                    }
                                )
                        case 5:
                            if not isinstance(body.get(key, None), bool):
                                return Json(
                                    {
                                        "status": SysCodes.ATTR_MISSING,
                                        "data": None,
                                        "message": f"{key} must be of type bool",
                                    }
                                )
                except Exception as e:
                    return Json(
                        {
                            "status": SysCodes.ATTR_MISSING,
                            "data": None,
                            "message": f"{r} request rule not applicable",
                            "trace": f'An error occured - {e}',
                        }
                    )

        # make sure you return only what is required by the rules
        result = {}
        for key in checkedkeys:
            value = body.get(key, "None")
            if value != "None":
                result[key] = value

        return Json(
                        {
                            "status": SysCodes.ATTR_FOUND,
                            "data": result,
                            "message": SysMessages.ATTR_FOUND
                        }
                    )

    """ return server information including host and port on which application runs"""

    def server(self):
        server = self.scope["server"]
        return Json({"host": server[0], "port": server[1]})

    """ return the http version used by the client"""

    def http(self):
        return self.scope["http_version"]

    """ return the scheme"""

    def scheme(self):
        return self.scope["scheme"]

    """ return the type of connection being handled """

    def type(self):
        return self.scope["type"]

    """ returns the version and spec details about the server in json"""

    def asgi(self):
        return Json(self.scope["asgi"])


    """
        Get the time the request came in
    """
    def entryTime(self):
        return datetime.now()

    """
        returns some properties of the client including their host and port
    """
    def client(self):
        client = self.scope["client"]
        return Json({"host": client[0], "port": client[1]})

    """ returns the HTTP method used by the client"""
    def method(self):
        return self.scope["method"]

    """ returns the path used by the client in the request"""

    def path(self):
        return self.scope["path"]

    """ returns info on the authorization header including the type and value set"""

    def auth(self):
        try:
            headerAuth = self.headers().authorization
            listAuth = headerAuth.split(" ", 1) if headerAuth is not None else ""
            return Json(
                {
                    "type": None if len(listAuth) != 2 else listAuth[0],
                    "value": None if len(listAuth) != 2 else listAuth[1],
                
                })
        except Exception as e:
            return Json({"type": None ,"value": None})


    """ returns all headers set on the request"""

    def headers(self):
        heads = self.scope["headers"]
        result = Json({})

        for key, value in heads:
            result[key.decode("utf-8")] = value.decode("utf-8")
        return result

    """ returns all query parameters set on the request"""

    def params(self):
        """decode the string"""
        string = self.scope["query_string"].decode("utf-8")

        """ split by &"""
        queryParam = {
            key: value[0] if len(value) == 1 else value
            for key, value in parse_qs(string).items()
        }
        return Json(queryParam)

    """ asynchronously fetched and returns the request body"""

    async def body(self):
        if self._body:
            return self._body
        
        body = b""
        more_body = True
        while more_body:
            message = await self.receive()
            body += message.get("body", b"")
            more_body = message.get("more_body", False)

        try:
            content = self.headers()["content-type"]
            if "json" in content:
                body = body.decode("utf-8")
                return Json(json.loads(body))

            if "multipart" in content:
                parser = FileParser()
                multipart = await parser.parseMultipart(body, content)
                result = await parser.getMultipartKeys(multipart)
                return Json(result)

            return Json({})

        except Exception as e:
            return Json({"error": e})
