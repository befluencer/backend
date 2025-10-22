from .appInfoModel import AppInfoModel

MODELS = {
    'app-info': AppInfoModel(),
}

def getModel(key):
    return MODELS.get(key, None)
    