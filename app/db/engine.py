from typing import Union

from sqlalchemy import URL, MetaData
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


async def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
    return _create_async_engine(url, future=True, pool_pre_ping=True)


async def create_db(engine: AsyncEngine, metadata: MetaData) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


async def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)