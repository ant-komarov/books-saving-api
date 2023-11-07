from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from slugify.slugify import slugify
from db.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    slug_name = Column(String(511))

    books = relationship("Book", back_populates="author")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug_name = slugify(self.name) # type: ignore



class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63))

    books = relationship("Book", back_populates="genre")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(511))
    author_id = Column(Integer, ForeignKey("authors.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))
    date_published = Column(Date)
    slug_title = Column(String(511))

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug_title = slugify(self.title) # type: ignore
