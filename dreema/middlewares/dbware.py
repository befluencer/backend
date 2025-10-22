from datetime import datetime
from typing import Union
from models._modelsList import getModel

class DBware:
    async def create(self, model:str=None, data:Union[list,dict]=None):
        model = getModel(model)

        if(isinstance(data, list)):
            for index,_ in enumerate(data):
                if data[index].get('flag', "-_") == "-_":
                    data[index]['flag'] =  1
                data[index]['dateCreated'] = int(datetime.now().timestamp())
        
        if(isinstance(data, dict)):
            if data.get('flag', "-_") == "-_":
                data['flag'] =  1
            data['dateCreated'] =  int(datetime.now().timestamp())
        
        # use model to create and quickly update
        return await model.create(data=data)
    
    async def delete(self, model:str=None, filters:dict=None, params:dict=None):
         # use model to create and quickly update
        model = getModel(model)
        return await model.delete(filters, params=params)
    
    async def update(self, model:str, data:Union[list,dict], filters:dict=None, params:dict=None):
        if(isinstance(data, object)):
            data['lastUpdated'] =  int(datetime.now().timestamp())
        
        if isinstance(data, list):
            for dt in data:
                for index,dt in enumerate(data):
                    if isinstance(dt, dict):  # extra safety check
                        data[index]['lastUpdated'] = int(datetime.now().timestamp())


         # use model to create and quickly update
        model = getModel(model)
        return await model.update(filters, data, params=params)
    
    async def read(self, model:str=None, filters:dict=None, params:dict=None):
        model = getModel(model)
        return await model.read(filters=filters, params=params)