from pypdf import PdfReader
import requests
import os
from io import BytesIO

from utils.patterns import SUBSTITUTIONS, TRIMS
from utils.string import apply_substitutions, escape_lines, title_page, is_remote_path
from utils.image import save_image


def parse_pdf_page(page, output_filename, media_folder):
    # TODO: change to tesseract OCR for text extraction
    page_text = apply_substitutions(
        escape_lines(
            page.extract_text()
        ),
        SUBSTITUTIONS
    )

    # TODO: add object detection for LATEX equation identification
    # TODO: use rapid_latex_ocr to extract equations from the sections of the images identified above

    for image in page.images:
        page_text += "\n" + save_image(image, output_filename, media_folder) + "\n"

    return page_text


def write_pdf(input_file, output_file, output_filename, media_folder):
    if is_remote_path(input_file):
        res = requests.get(input_file)
        input_file = BytesIO(res.content)

    reader = PdfReader(input_file)

    with open(output_file, "w", encoding="utf-8") as out:
        for page_index, page in enumerate(reader.pages):
            page_text = title_page(
                parse_pdf_page(page, output_filename, media_folder),
                page_index
            )

            page_text = apply_substitutions(page_text, TRIMS)

            out.write(page_text)


def init():
    input_file = input("Input file location (local or remote): ")
    output_location = input("Output location (local): ")
    output_filename = input("Output filename: ")
    output_file = os.path.join(output_location, output_filename + ".md")

    media_folder = os.path.join(output_location, "media")
    os.makedirs(media_folder, exist_ok=True)

    write_pdf(input_file, output_file, output_filename, media_folder)


if __name__ == "__main__":
    init()
