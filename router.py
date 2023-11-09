from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.dependencies import get_db
import schemas
import crud


router = APIRouter()

@router.get("/genres/", response_model=list[schemas.Genre])
async def get_genres_list(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    return await crud.get_genres(db, skip, limit)


@router.post("/genres/", response_model=schemas.Genre)
async def create_genre(genre: schemas.GenreCreate, db: AsyncSession = Depends(get_db)):
    db_genre = crud.get_genre_by_name(db, genre.name)
    if db_genre:
        raise HTTPException(status_code=400, detail="Genre with such name already exists")
    return await crud.create_genre(db, genre)
