import os
import logging
from celery import Celery
from converter import pdf_to_jpg
from db.database import SessionLocal
from utils import get_authors_list_from_xls, get_titles_list_from_xls
from crud import get_books_by_authors_or_titles
from settings import settings
from models import Book


app = Celery("tasks", broker="redis://redis-1:6379/0", backend="redis://redis-1:6379/0")

app.conf.broker_connection_retry_on_startup = True

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# @app.task
async def process_excel_file(file_path):
    print("Start proceed file...")
    authors = get_authors_list_from_xls(file_path)
    logging.info(authors)
    titles = get_titles_list_from_xls(file_path)
    logging.info(titles)
    async with SessionLocal() as db:
        book_list = await get_books_by_authors_or_titles(db, authors, titles)
        logging.info(book_list)
        for book in book_list:
            book.read_only = True  # type: ignore
            convert_file_to_images(book)
        await db.commit()
        logging.info("Done")


def convert_file_to_images(book: Book):
    file_path = os.path.join(
        settings.UPLOADED_FILES_PATH, str(book.id), f"{book.slug_title}.pdf"
    )
    new_path = os.path.join(settings.UPLOADED_FILES_PATH, str(book.id), "img", "")
    os.makedirs(os.path.dirname(new_path), exist_ok=True)
    logging.info("Start converting pdf to images")
    pdf_to_jpg(pdf_path=file_path, output_path=new_path, new_file_name=book.slug_title)
    logging.info("Converted")
