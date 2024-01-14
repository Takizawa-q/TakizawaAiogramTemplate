import asyncpg
import asyncio
import aiomysql
from app.config import config


class PostgreSQLConnection():
    print(1)
    
    cursor: asyncpg.pool.Pool
    
    @staticmethod
    async def create_connection():
        PostgreSQLConnection.cursor = await asyncpg.create_pool(
            user=config.db.user,
            password=config.db.password,
            database=config.db.database,
            host=config.db.host,
            port=config.db.port)