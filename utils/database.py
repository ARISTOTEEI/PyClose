from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import Session,sessionmaker,DeclarativeBase
from sqlalchemy import URL,create_engine,text
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_url_asyncpg
)

async_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

