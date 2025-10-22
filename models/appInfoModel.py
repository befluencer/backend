from dreema.orm import database

class AppInfoModel(database.Database):
    #specify table or document name here
    tablename = 'app_info' 

    def __init__(self):
        super().__init__() 
        self.setTable(self.tablename)
        