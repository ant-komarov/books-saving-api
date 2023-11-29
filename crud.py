from slugify.slugify import slugify
from sqlalchemy import insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, Session
import schemas
import models


#  Genre functions
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


#  Author functions
async def create_author(db: AsyncSession, author: schemas.AuthorCreate):
    query = insert(models.Author).values(**author.model_dump())
    return await db.execute(query)


async def get_authors(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = select(models.Author).offset(skip).limit(limit)
    authors_list = await db.execute(query)
    return [author[0] for author in authors_list.fetchall()]


async def get_author_by_name(db: AsyncSession, name: str):
    query = select(models.Author).filter(models.Author.name == name)
    result = await db.execute(query)
    return result.scalar_one_or_none()


#  Book functions
async def create_book(db: AsyncSession, book: schemas.BookCreate):
    book_db = book.model_dump()
    del book_db["file"]
    book_title = book_db.get("title")
    book_db["slug_title"] = slugify(book_title)  # type: ignore
    query = insert(models.Book).values(**book_db).returning(models.Book)
    result = await db.execute(query)
    return result.scalar_one()


async def get_books(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = (
        select(models.Book)
        .options(selectinload(models.Book.author), selectinload(models.Book.genre))
        .offset(skip)
        .limit(limit)
    )
    books_list = await db.execute(query)
    return [book[0] for book in books_list.fetchall()]


async def get_book_by_title(db: AsyncSession, title: str):
    query = select(models.Book).filter(models.Book.title == title)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_book_by_id(db: AsyncSession, book_id: int):
    query = select(models.Book).filter(models.Book.id == book_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


def get_books_by_authors_or_titles(db: Session, authors: list, titles: list):
    result = (
        db.query(models.Book)
        .filter(or_(models.Book.title.in_(titles), models.Author.name.in_(authors)))
        .options(selectinload(models.Book.author))
        .all()
    )
    return result
