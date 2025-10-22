from . import Json
import config

"""
    
"""
def loadenv():
    envdict = {}
    
    with open(".env", "r") as data:
        for line in data:
            # Ignore lines that are comments or empty
            if line.strip() and not line.startswith("#"):
                key, value = line.split("=", 1)  # Only split on the first '='
                envdict[key.strip()] = value.strip().strip("'").strip('"')  # Clean up the value
                
    # save it to redis
    return Json(envdict)


def getenv(key: str) -> str:
    """
    Use:
            Read from .env file to be used by other
            parts of the library

    Parameters:
            key (str): the key is needed to reference to the keyname of the variable

    Returns:
            str: a string of the value of the specified key
            Default: Empty string ""

    """
    try:
        return loadenv().get(key, "")
    except Exception: 
        return ""


def getconfig(key: str):
    """
    Use:
            Read from config.py file to be used by
            any other part of the system

    Parameters:
        key (str): the key is needed to reference to the config in config.py

    Returns:
            The value of whatever was set in the file
            Default: Empty string ""
    """
    try:
        return Json(config.CONFIG[key])
    except Exception:
        return ""
