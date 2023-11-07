import os
from models import Book
from settings import settings


# Save file to uploads folder
async def save_file_to_uploads(file, filename):
    with open(f'{settings.UPLOADED_FILES_PATH}{filename}', "wb") as uploaded_file:
        file_content = await file.read()
        uploaded_file.write(file_content)
        uploaded_file.close()


# Delete file from uploads folder
def delete_file_from_uploads(file_name):
    try:
        os.remove(settings.UPLOADED_FILES_PATH + file_name)
    except FileNotFoundError as e:
        print(e)

# Format filename
def format_filename(file: Book):
    return f"{file.slug_title}.pdf"
