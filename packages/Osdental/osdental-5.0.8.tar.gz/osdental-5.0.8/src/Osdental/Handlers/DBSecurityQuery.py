import os
from uuid import UUID
from typing import Dict, Any
from dotenv import load_dotenv
from Osdental.Database.Connection import Connection
from Osdental.RedisCache.Redis import RedisCacheAsync
from Osdental.Exception.ControlledException import UnauthorizedException
from Osdental.Utils.Message import UNAUTHORIZATED
from Osdental.Utils.Code import DB_UNAUTHORIZATED
from Osdental.Utils.Constant import CHARSET

load_dotenv() 

class DBSecurityQuery:

    def __init__(self):
        self.db = Connection(os.getenv('DATABASE_SECURITY'))
        self.redis = RedisCacheAsync(os.getenv('REDIS_HOST_SECURITY'), os.getenv('REDIS_PORT_SECURITY'), os.getenv('REDIS_PASSWORD_SECURITY'))

    async def get_data_legacy(self) -> Dict[str,Any]:
        return await self.db.execute_query_return_data('EXEC SECURITY.sps_SelectDataLegacy', fetchone=True)
    
    async def validate_auth_token(self, token_id:UUID, user_id:UUID) -> bool:
        query = """ 
        EXEC SECURITY.sps_ValidateUserToken  
        @i_idToken = :token_id,
        @i_idUser = :user_id
        """
        await self.redis.connect()
        redis_response = await self.redis.exists(token_id)
        if redis_response:
            data_byte = await self.redis.get_str(token_id)
            return data_byte.decode(CHARSET)
        
        is_auth = await self.db.execute_query_return_first_value(query, {'token_id': token_id, 'user_id': user_id})
        if not is_auth:
            raise UnauthorizedException(error=UNAUTHORIZATED, status_code=DB_UNAUTHORIZATED)
            
        await self.redis.set_str(token_id, is_auth, ttl=1800)
        await self.redis.close()
        return is_auth