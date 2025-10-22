import os, shutil
from dreema.responses import SysCodes, SysMessages, response
from dreema.helpers import Json

"""
    
    Use:
        Managing files to include saving files to disk OR an online bucket
        Management includes saving, and deleting from the volume
"""


class FileManagement:
    """
    Requires for a file to be already uploading through multipart
    This only moves the file from the temporary location to the new location
    """

    async def save(self, fullPath: str, destination: str, newfilename: str = None):
        # checking file existence
        if not os.path.exists(fullPath):
            return Json(
                {
                    "data": None,
                    "status": SysCodes.FILE_NOT_EXISTS,
                    "message": SysMessages.FILE_NOT_EXISTS,
                }
            )
         
        #create directory if it does not exist   
        os.makedirs(destination,exist_ok=True)
        filename = newfilename if newfilename else os.path.basename(fullPath)
        path = os.path.join(destination,filename)
        
        #move the file
        shutil.move(fullPath,path)
        
        if not os.path.exists(path):
            return Json(
                {
                    "data": None,
                    "status": SysCodes.FILE_UPLOAD_FAILED,
                    "message": SysMessages.FILE_UPLOAD_FAILED,
                }
            )
        
        return Json(
                {
                    "data": {
                        'size':os.path.getsize(path),
                        'fullpath':path
                    },
                    "status": SysCodes.FILE_UPLOAD_SUCCESS,
                    "message": SysMessages.FILE_UPLOAD_SUCCESS,
                }
            )    

       
    async def delete(self, fullpath:str):
        if not os.path.exists(fullpath):
            return Json(
                {
                    "data": None,
                    "status": SysCodes.FILE_NOT_EXISTS,
                    "message": SysMessages.FILE_NOT_EXISTS,
                }
            )
        try:
            os.remove(fullpath)
            return Json(
                {
                    "data": None,
                    "status": SysCodes.OP_SUCCESS,
                    "message": SysMessages.OP_SUCCESS,
                }
            )
        except Exception as e:
             return Json(
                {
                    "data": None,
                    "status": SysCodes.OP_FAILED,
                    "message": f'{SysMessages.OP_FAILED} - {e}',
                    
                }
            )
            
        