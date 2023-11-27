from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = async_sessionmaker(
    expire_on_commit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()
