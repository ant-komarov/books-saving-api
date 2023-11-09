from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
import schemas
import models


async def create_genre(db: AsyncSession, genre: schemas.GenreCreate):
    query = insert(models.Genre).values(**genre.model_dump())
    return await db.execute(query)


async def get_genres(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = select(models.Genre).offset(skip).limit(limit)
    genres_list = await db.execute(query)
    return [genre[0] for genre in genres_list.fetchall()]


async def get_genre_by_name(db: AsyncSession, name: str):
    query = select(models.Genre).filter(models.Genre.name == name)
    result = await db.execute(query)
    return result.scalar_one_or_none()
