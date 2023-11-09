from sqlalchemy.ext.asyncio import AsyncSession
from db.database import SessionLocal



async def get_db() -> AsyncSession: # type: ignore
    db = SessionLocal()
    try:
        yield db # type: ignore
    finally:
        db.close()
