from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(
    settings.DATABASE_url_asyncpg
)

async_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass
