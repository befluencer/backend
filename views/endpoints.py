from dreema.routing import route, routegroup
import controllers.sampleController as Sample

"""
        author:  Raphael Djangmah
        Use:
                This file is the main view entry.
"""
routes = [
        # creating single routes
        route(path="/", methods=["GET", "POST"], handler=Sample.SampleController.welcome),
        
]
