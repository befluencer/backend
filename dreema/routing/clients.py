from dreema.helpers import Json

"""
    
    Use:
        Routes and routegroups used in views to define routes 
"""


# helpers
def route(path: str, methods, handler):
    return Json({"path": path, "method": methods, "handler": handler})


def routegroup(cls: list, prefix: str = "", postfix: str = ""):
    # get the routes in the other folder
    grouped = []
    for r in cls:
        try:
            grouped.append(
                Json(
                    {
                        "path": f"/{prefix}{r.path}/{postfix}",
                        "method": r.method,
                        "handler": r.handler,
                    }
                )
            )
        except Exception:
            continue

    return grouped
