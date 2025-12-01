from controllers.app.logosController import LogosController
from dreema.routing import route
from controllers.app import systemController as System
class SystemViews:
    route = [
        route(path="/auth/login", methods=['POST'], handler=System.SystemController.login),
        route(path="/get-logos", methods=['GET'], handler=LogosController.getLogos),
    ]
        