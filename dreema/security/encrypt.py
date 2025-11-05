import random, string
import secrets
import bcrypt

class Encrypt:

    '''
        this generates a random string of x length
        type :
                1 - numbers only
                2 - text only
                3 - text and nunbers
                4 - text and numbers and symbols
    '''
    @staticmethod
    def generateRandom( length:int=10, type:int=4):
        if type == 1:
            chars = string.digits
        elif type == 2:
            chars = string.ascii_letters
        elif type == 3:
            chars = string.ascii_letters + string.digits
        elif type == 4:
            chars = string.ascii_letters + string.digits + string.punctuation
        else:
            chars = string.ascii_letters + string.digits + string.punctuation

        return ''.join(random.choices(chars, k=length))
    
    @staticmethod
    def getSecret(bytelength:int=12):
        secret = secrets.token_hex(bytelength)
        return secret
    
    @staticmethod
    def hash(password:str, rounds:int = 10):
        hashedPwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=rounds))
        return hashedPwd.decode()

    @staticmethod
    def verifyHash(password:str, hash:str):
        try:
            if not bcrypt.checkpw(password.encode(), hash.encode()):
                return False
            
            return True
        except Exception as e:
            return False