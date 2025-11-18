from dreema.orm import database

class BrandModel(database.Database):
    #specify table or document name here
    tablename = 'brands' 

    def __init__(self):
        super().__init__() 
        self.setTable(self.tablename)

