from dreema.orm import database

class MediaKitModel(database.Database):
    #specify table or document name here
    tablename = 'mediakits' 

    def __init__(self):
        super().__init__() 
        self.setTable(self.tablename)

