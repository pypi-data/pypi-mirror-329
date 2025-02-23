import random
import string
from Osdental.Utils.Code import DB_SUCCESS
from Osdental.Utils.Message import SUCCESS

class Util:
    
    @staticmethod
    def response(status:str = DB_SUCCESS, message:str=SUCCESS, data:str=None):
        return {
            'status': status,
            'message': message,
            'data': data
        }

    @staticmethod
    def generate_password(length: int = 12) -> str:
        # Define a set of valid characters (excluding problematic characters)
        valid_characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|:,.?"
        password = ''.join(random.choice(valid_characters) for _ in range(length))
        return password
    
    @staticmethod
    def concat_str(*args):
        return ' '.join(str(arg) for arg in args).strip()