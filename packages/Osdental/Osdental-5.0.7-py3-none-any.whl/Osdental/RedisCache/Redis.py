import json
from typing import Dict, List, Optional
import redis.asyncio as redis

class RedisCacheAsync:
    def __init__(self, host:str, port:int, password:str, db:int = 1):
        """Connect to the Redis server."""
        self.pool = redis.ConnectionPool.from_url(
            f"rediss://{host}:{port}",
            password=password,
            db=db
        )
        self.client = redis.Redis(connection_pool=self.pool)


    async def set_dict(self, key:str, value:Dict[str,str], ttl:Optional[int] = None):
        """Set a JSON value in the cache."""
        json_value = json.dumps(value)
        await self.client.set(key, json_value)
        if ttl:
            await self.client.expire(key, ttl)

    async def set_str(self, key:str, value:str, ttl:Optional[int] = None):
        """Set a string value in the cache."""
        await self.client.set(key, value)
        if ttl:
            await self.client.expire(key, ttl)

    async def get_dict(self, key:str) -> Optional[str]:
        """Get a JSON value from the cache and convert it back to a Python object."""
        json_value = await self.client.get(key)
        if json_value:
            return json.loads(json_value)
        return None

    async def get_str(self, key:str) -> Optional[str]:
        """Get a string value from the cache."""
        value = await self.client.get(key)
        return value.decode('utf-8') if value else None

    async def delete(self, key:str) -> bool:
        """Delete a value from the cache."""
        return await self.client.delete(key)

    async def exists(self, key:str) -> bool:
        """Check if a key exists in the cache."""
        return await self.client.exists(key)

    async def flush(self):
        """Flush all keys in the cache."""
        await self.client.flushdb()

    async def close(self):
        """Close the connection pool."""
        if self.pool:
            await self.pool.disconnect()

    # NUEVO MÉTODO: Obtener múltiples claves en una sola operación
    async def mget(self, keys:List[str]) -> List[Optional[str]]:
        """Get multiple values from the cache."""
        values = await self.client.mget(keys)
        return [json.loads(value) if value else None for value in values]
