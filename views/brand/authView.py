from dreema.routing import route,routegroup
from controllers.brand import authController as Auth

class AuthView:
    route = [
        route(path="/signup", methods=['POST'], handler=Auth.AuthController.addBrand),
        route(path="/login", methods=['POST'], handler=Auth.AuthController.login),
        route(path="/request-otp", methods=['POST'], handler=Auth.AuthController.requestOTP),
        route(path="/verify-otp", methods=['POST'], handler=Auth.AuthController.verifyOTP),
        route(path="/reset-password", methods=['POST'], handler=Auth.AuthController.resetPassword),
        route(path="/check-existence", methods=['GET'], handler=Auth.AuthController.checkUserExists),
        route(path="/user", methods=['GET'], handler=Auth.AuthController.getme),
        

    ]

