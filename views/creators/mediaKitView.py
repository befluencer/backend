from dreema.routing import route,routegroup
from controllers.creators import mediakit as MediaKit

class MediaKitView:
    route = [
        route(path="/get", methods=['GET'], handler=MediaKit.MediaKitController.getKit),
        route(path="/create-edit", methods=['POST'], handler=MediaKit.MediaKitController.createKit),
        route(path="/delete", methods=['POST'], handler=MediaKit.MediaKitController.deleteKit),
    ]

