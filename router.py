from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.dependencies import get_db
import schemas
import crud


router = APIRouter()

@router.get("/genres/", response_model=list[schemas.Genre])
async def get_genres_list(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    return await crud.get_genres(db, skip, limit)


@router.post("/genres/")
async def create_genre(genre: schemas.GenreCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        db_genre = await crud.get_genre_by_name(db, genre.name)
        if db_genre:
            raise HTTPException(status_code=400, detail="Genre with such name already exists")
        await crud.create_genre(db, genre)
    return {"message": "New genre successfully added"}


@router.get("/authors/", response_model=list[schemas.Author])
async def get_authors_list(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    return await crud.get_authors(db, skip, limit)


@router.post("/authors/")
async def create_author(author: schemas.AuthorCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        db_author = await crud.get_author_by_name(db, author.name)
        if db_author:
            raise HTTPException(status_code=400, detail="Author with such name already exists")
        await crud.create_author(db, author)
    return {"message": "New author successfully added"}


@router.get("/books/", response_model=list[schemas.Book])
async def get_books_list(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    return await crud.get_books(db, skip, limit)


@router.post("/books/")
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        await crud.create_book(db, book)
    return {"message": "New book successfully added"}
