from pypdf import PdfReader
import os

from utils.patterns import SUBSTITUTIONS, TRIMS
from utils.string import apply_substitutions, escape_lines, title_page
from utils.image import save_image


def parse_pdf_page(page, media_folder):
    page_text = apply_substitutions(
        escape_lines(
            page.extract_text()
        ),
        SUBSTITUTIONS
    )

    for image in page.images:
        page_text += "\n" + save_image(image, media_folder) + "\n"

    return page_text


def write_pdf(input_file, output_file, media_folder):
    with (open(output_file, "w", encoding="utf-8") as out):
        reader = PdfReader(input_file)

        for page_index, page in enumerate(reader.pages):
            page_text = title_page(
                parse_pdf_page(page, media_folder),
                page_index
            )

            page_text = apply_substitutions(page_text, TRIMS)

            out.write(page_text)


if __name__ == "__main__":
    os.makedirs("media", exist_ok=True)
    write_pdf("doc.pdf", "output.md", "media")
