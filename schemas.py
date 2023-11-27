from datetime import date
from fastapi import File, Form, UploadFile
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
    date_published: date


class BookCreate(BookBase):
    author_id: int
    genre_id: int
    file: UploadFile

    @classmethod
    def as_form(cls,
                title: str = Form(...),
                date_published: date = Form(...),
                author_id: int = Form(...),
                genre_id: int = Form(...),
                file: UploadFile = File(...)):
        return cls(title=title,
                   date_published=date_published,
                   author_id=author_id,
                   genre_id=genre_id,
                   file=file)


class Book(BookBase):
    id: int
    author: Author
    genre: Genre

    class Config:
        from_attributes = True
