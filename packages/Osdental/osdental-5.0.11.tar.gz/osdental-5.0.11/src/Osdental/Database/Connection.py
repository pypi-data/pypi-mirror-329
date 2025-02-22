from typing import Dict, List
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from Osdental.Exception.ControlledException import DatabaseException
from Osdental.Utils.Code import DB_SUCCESS

class Connection:

    _instances: Dict[str, 'Connection'] = {}

    def __new__(cls, db_url: str):
        if db_url not in cls._instances:
            cls._instances[db_url] = super(Connection, cls).__new__(cls)
        return cls._instances[db_url]

    def __init__(self, db_url: str):
        if not hasattr(self, 'initialized'):
            self.engine = create_async_engine(
                db_url,
                pool_size=20,          
                max_overflow=40,       
                pool_timeout=30,       
                pool_recycle=3600     
            )
            self.session_factory = sessionmaker(
                bind=self.engine, 
                class_=AsyncSession, 
                expire_on_commit=False
            )
            self.initialized = True

    async def get_session(self) -> AsyncSession:
        return self.session_factory()

    async def execute_query_return_first_value(self, query:str, params:Dict[str,str] = None) -> str:
        async with (await self.get_session()) as session:
            async with session.begin():
                result = await session.execute(text(query), params)
                return result.scalar()

    async def execute_query_return_data(self, query:str, params:Dict[str,str] = None, fetchone=False) -> List[Dict[str,str]] | Dict[str,str]:
        async with (await self.get_session()) as session:
            async with session.begin():
                result = await session.execute(text(query), params)
                keys = result.keys()
                if fetchone:
                    return dict(zip(keys, result.fetchone()))
                
                return [dict(zip(keys, row)) for row in result.fetchall()] 

    async def execute_query_return_message(self, query:str, params:Dict[str,str] = None, code:str = DB_SUCCESS) -> str:
        async with (await self.get_session()) as session:
            async with session.begin():
                result = await session.execute(text(query), params)
                row = result.fetchone() 
                if row.STATUS_CODE != code:
                    raise DatabaseException(error=row.STATUS_MESSAGE, status_code=row.STATUS_CODE)

                return row.STATUS_MESSAGE
                
    async def execute_query(self, query:str, params:Dict[str,str] = None) -> None:
        async with (await self.get_session()) as session:
            async with session.begin():
                await session.execute(text(query), params)


    async def execute_transaction(self, queries: List[str], params: List[Dict[str, str]] = None) -> None:
        async with (await self.get_session()) as session:
            async with session.begin():
                for i, query in enumerate(queries):
                    await session.execute(text(query), params[i] if params else None)
    
    async def close_engine(self) -> None:
        """Dispose of the engine and remove instance."""
        if self.engine:
            await self.engine.dispose() 
        
        if self.db_url in self._instances:
            del self._instances[self.db_url]