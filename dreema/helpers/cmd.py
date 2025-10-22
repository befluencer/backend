"""

Use:
        This class aims to provide a way to create sample of the basic
        files from the terminal.
        These files include the Models, Views and Controllers
"""


class Model:
    def template(self, classname):
        return f"""from dreema.orm import database

class {classname}(database.Database):
    #specify table or document name here
    tablename = '{classname.lower()}' 

    def __init__(self):
        super().__init__()
        self.setTable(self.tablename)
        """

    def create(self, classname, filename):
        # sanitize the classname
        if not isinstance(classname, str):
            print(
                "Error: In future updates, we will consider adding multiple file creations"
            )
            return

        with open(f"models/{filename}.py", "w") as f:
            f.write(self.template(classname))
            f.close()

        print(f"Done: model with name {classname} created")


class Controller:
    def template(self, classname):
        return f"""from dreema.requests import Request
from dreema.responses import response
from dreema.responses import SysCodes, SysMessages

class {classname}:
    async def sample(request: Request):
        # sample how to get and validate request body 
        body = await request.applyRules({{'name':'required,name'}})
        
        # sample response
        return response(data=body, status=SysCodes.OP_COMPLETED, message=SysMessages.OP_COMPLETED)
        """

    def create(self, classname, filename):
        # sanitize the classname
        if not isinstance(classname, str):
            print(
                "Error: In future updates, we will consider adding multiple file creations"
            )
            return

        with open(f"controllers/{filename}.py", "w") as f:
            f.write(self.template(classname))
            f.close()

        print(f"Done: Controller with name {classname} created")


class View:
    def template(self, classname):
        return f"""from dreema.routing import route,routegroup
from controllers import sampleController

class {classname}:
    route = [
        route(path="/sample", methods=['POST','GET'], handler=sampleController.UsersAuth.welcome),
    ]
        """

    def create(self, classname, filename):
        # sanitize the classname
        if not isinstance(classname, str):
            print(
                "Error: In future updates, we will consider adding multiple file creations"
            )
            return

        with open(f"views/{filename}.py", "w") as f:
            f.write(self.template(classname))
            f.close()

        print(f"Done: View with name {classname} created")
