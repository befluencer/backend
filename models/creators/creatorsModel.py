from dreema.orm import database

class CreatorsModel(database.Database):
    #specify table or document name here
    tablename = 'creators' 

    def __init__(self):
        super().__init__() 
        self.setTable(self.tablename)
        