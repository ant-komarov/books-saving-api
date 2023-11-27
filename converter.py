from pdf2image.pdf2image import convert_from_path


def pdf_to_jpg(
    pdf_path, output_path, new_file_name, first_page=1, last_page=None, resolution=300
):
    """
    Convert PDF file to JPEG format.

    :param pdf_path: Path to PDF-file.
    :param output_path: Path for saving new JPEG-file.
    :param new_file_name: New filename.
    :param first_page: Number of first page to convert.
    :param last_page: Number of last page to convert.
    :param resolution: Resolution in DPI (dots per inch).
    """
    # poppler_path = r"/app/poppler/Library/bin"

    images_list = convert_from_path(
        pdf_path,
        # poppler_path=poppler_path,
        first_page=first_page,
        last_page=last_page,  # type: ignore
        dpi=resolution,
    )

    for i, image in enumerate(images_list):
        image.save(f"{output_path}/{new_file_name}{i + first_page}.jpg", "JPEG")
