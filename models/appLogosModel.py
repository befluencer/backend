from dreema.orm import database

class AppLogosModel(database.Database):
    #specify table or document name here
    tablename = 'app_logos' 

    def __init__(self):
        super().__init__() 
        self.setTable(self.tablename)
        