from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.dependencies import get_db
import schemas
import crud
from tasks.tasks import process_excel_file
from utils import (
    save_file_to_uploads,
    get_path_to_file,
    create_html_page,
)


router = APIRouter()


@router.get("/genres/", response_model=list[schemas.Genre])
async def get_genres_list(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10
):
    return await crud.get_genres(db, skip, limit)


@router.post("/genres/")
async def create_genre(genre: schemas.GenreCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        db_genre = await crud.get_genre_by_name(db, genre.name)
        if db_genre:
            raise HTTPException(
                status_code=400, detail="Genre with such name already exists"
            )
        await crud.create_genre(db, genre)
    return {"message": "New genre successfully added"}


@router.get("/authors/", response_model=list[schemas.Author])
async def get_authors_list(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10
):
    return await crud.get_authors(db, skip, limit)


@router.post("/authors/")
async def create_author(
    author: schemas.AuthorCreate, db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        db_author = await crud.get_author_by_name(db, author.name)
        if db_author:
            raise HTTPException(
                status_code=400, detail="Author with such name already exists"
            )
        await crud.create_author(db, author)
    return {"message": "New author successfully added"}


@router.get("/books/", response_model=list[schemas.Book])
async def get_books_list(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10
):
    return await crud.get_books(db, skip, limit)


@router.post("/books/")
async def create_book(
    book: schemas.BookCreate = Depends(schemas.BookCreate.as_form),
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        new_book = await crud.create_book(db, book)
        await save_file_to_uploads(
            file=book.file, filename=new_book.slug_title, file_id=new_book.id
        )
    return {"message": "New book successfully added"}


@router.get("/books/{book_id}/")
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book_by_id(db=db, book_id=book_id)

    if db_book.read_only:  # type: ignore
        html_content = create_html_page(db_book)

        return HTMLResponse(content=html_content, status_code=200)

    file_path = get_path_to_file(db_book.slug_title, book_id)  # type: ignore

    return FileResponse(path=file_path, headers={"Content-Disposition": "inline"})


@router.post("/upload/excel/")
def upload_excel_file(file: UploadFile = File(...)):
    with file.file as f:
        content = f.read()

    with open(file.filename, "wb") as tmp_file:  # type: ignore
        tmp_file.write(content)

    task = process_excel_file.delay(tmp_file.name)

    return {"task_id": str(task.id)}
