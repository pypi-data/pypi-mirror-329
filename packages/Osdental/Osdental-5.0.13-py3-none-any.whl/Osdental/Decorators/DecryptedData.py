import os
from functools import wraps
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from Osdental.Encryptor.Aes import AES
from Osdental.Encryptor.Jwt import JWT
from Osdental.Exception.ControlledException import UnauthorizedException
from Osdental.Handlers.DBSecurityQuery import DBSecurityQuery
from Osdental.Utils.Constant import (JWT_USER_KEY, USER_ID, TOKEN_ID, LEGACY_ID, ENTERPRISE_ID, AUTHORIZATION_ID, PROFILE_ID, ITEM_REPORT_ID, 
USER_AES_KEY, EXTERNAL_ENTERPRISE_ID, ABBREVIATION, USER_FULL_NAME)
from Osdental.Utils.Message import UNAUTHORIZATED

load_dotenv()

aes = AES()
jwt_user_key = os.getenv(JWT_USER_KEY)
db_security_query = DBSecurityQuery()

def process_encrypted_data(model:BaseModel = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs): 
            legacy = await db_security_query.get_data_legacy()
            if 'user_token' in kwargs:
                user_token_encrypted = kwargs.get('user_token')
                user_token = aes.decrypt(legacy.get('AES_KEY_USER'), user_token_encrypted)
                payload = JWT.extract_payload(user_token, jwt_user_key)
                token = await db_security_query.validate_auth_token(payload.get(TOKEN_ID), payload.get(USER_ID))
                if not token:
                    raise UnauthorizedException(error=UNAUTHORIZATED)
                
                kwargs['user_token_id'] = payload.get(TOKEN_ID)
                kwargs['user_id'] = payload.get(USER_ID)
                kwargs['external_enterprise_id'] = payload.get(EXTERNAL_ENTERPRISE_ID)
                kwargs['profile_id'] = payload.get(PROFILE_ID)
                kwargs['legacy_id'] = payload.get(LEGACY_ID)
                kwargs['item_report_id'] = payload.get(ITEM_REPORT_ID)
                kwargs['enterprise_id'] = payload.get(ENTERPRISE_ID)
                kwargs['authorization_id'] = payload.get(AUTHORIZATION_ID)
                kwargs['user_full_name'] = payload.get(USER_FULL_NAME)
                kwargs['abbreviation'] = payload.get(ABBREVIATION)
                kwargs['user_aes_key'] = payload.get(USER_AES_KEY)
                kwargs.pop('user_token', None)

            if 'aes_data' in kwargs:
                aes_data = kwargs.get('aes_data')
                decrypted_data = aes.decrypt(legacy.get('AES_KEY_USER'), aes_data)
                if model:
                    try:
                        kwargs['data'] = model(**decrypted_data)
                    except ValidationError as e:
                        raise ValueError(f'Invalid data format: {e}')
                else:
                    kwargs['data'] = decrypted_data
                
                kwargs.pop('aes_data', None)

            kwargs['legacy'] = legacy
            kwargs['jwt_user_key'] = jwt_user_key
            return await func(self, **kwargs)  
        
        return wrapper
    return decorator