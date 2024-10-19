import os
from typing import Generator

from sqlalchemy import MetaData
from sqlalchemy.engine import url
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from logger import logger

Base = declarative_base(metadata=MetaData())

ASYNC_DATABASE_URL = url.URL.create(
    drivername="postgresql+asyncpg",
    database=os.getenv("POSTGRES_DB", ""),
    port=int(os.getenv("POSTGRES_PORT", "")),
    host=os.getenv("POSTGRES_HOST", ""),
    username=os.getenv("POSTGRES_USER", ""),
    password=os.getenv("POSTGRES_PASSWORD", ""),
)

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    future=True,
    echo=int(os.getenv("SHOW_QUERIES", 1)),
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        async with session.begin():
            yield session
    except Exception as e:
        logger.error(f"try get db session {e}", exc_info=True)
