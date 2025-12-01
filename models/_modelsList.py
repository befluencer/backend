from models.appLogosModel import AppLogosModel
from .appInfoModel import AppInfoModel
from .creators import creatorsModel 
from .brands import brandModel
from .mediakits import mediakitModel

MODELS = {
    'app-info': AppInfoModel(),
    'creators': creatorsModel.CreatorsModel(),
    'brands': brandModel.BrandModel(),
    'mediakits': mediakitModel.MediaKitModel(),
    'app-logos': AppLogosModel(),
}

def getModel(key):
    return MODELS.get(key, None)
    