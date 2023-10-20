import fitz  # PyMuPDF
import re
import os

SUBSTITUTIONS = [
    ("\n", "\n\n"),
    (re.compile("•"), "-"),
    (re.compile("▶"), "-")
]


def extract_images_from_pdf(pdf_path, output_file, media_folder):
    with fitz.open(pdf_path) as doc, open(output_file, "w", encoding="utf-8") as out:
        for page_index, page in enumerate(doc):
            page_text = page.get_text()

            if page_index == 0:
                page_text = "# " + page_text
            else:
                page_text = "## " + page_text

            lines = page_text.split("\n")
            processed_lines = []
            for line in lines:
                match = re.compile(r'^([a-z].*)$').match(line)
                if match:
                    processed_lines[-1] += ' ' + match.group(1)
                else:
                    processed_lines.append(line)

            page_text = '\n'.join(processed_lines)

            for pattern, replacement in SUBSTITUTIONS:
                page_text = re.sub(pattern, replacement, page_text)



            for image in page.get_images(full=True):
                base_image = doc.extract_image(image[0])
                image_bytes = base_image["image"]

                with open(f"{media_folder}/{image[7]}.png", "wb") as image_file:
                    image_file.write(image_bytes)

            out.write(page_text)


if __name__ == "__main__":
    os.makedirs("media", exist_ok=True)
    extract_images_from_pdf("test.pdf", "output.md", "media")
