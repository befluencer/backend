from .appInfoModel import AppInfoModel
from .creators import creatorsModel 
from .brands import brandModel
from .mediakits import mediakitModel

MODELS = {
    'app-info': AppInfoModel(),
    'creators': creatorsModel.CreatorsModel(),
    'brands': brandModel.BrandModel(),
    'mediakits': mediakitModel.MediaKitModel(),
}

def getModel(key):
    return MODELS.get(key, None)
    