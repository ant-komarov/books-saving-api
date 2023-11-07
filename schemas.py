from datetime import date
from pydantic import BaseModel


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    publish_date: date


class BookCreate(BookBase):
    author_id: int
    genre_id: int


class Book(BookBase):
    id: int
    author: Author
    genre: Genre

    class Config:
        from_attributes = True
