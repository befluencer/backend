from .appInfoModel import AppInfoModel
from .creators import creatorsModel 

MODELS = {
    'app-info': AppInfoModel(),
    'creators': creatorsModel.CreatorsModel(),
}

def getModel(key):
    return MODELS.get(key, None)
    