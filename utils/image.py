from io import BytesIO
from PIL import Image
import os


def save_image(image, output_filename, output_directory, alpha_to_white=True):
    filename = os.path.join(output_directory, f"{output_filename}-{image.name}")

    with open(filename, "wb") as image_file:
        if alpha_to_white:
            image_file.write(make_png_white(image.data))
        else:
            image_file.write(image.data)

    relative_file_location = os.path.join(get_last_subdirectory(output_directory), get_last_subdirectory(filename))

    return f"![]({relative_file_location})"


def make_png_white(image_data):
    # Open the image from bytes
    with Image.open(BytesIO(image_data)) as input_img:
        # Check if the image has an alpha (transparency) channel
        if input_img.mode in ('RGBA', 'LA') or (input_img.mode == 'P' and 'transparency' in input_img.info):
            # Create a new image with a white background
            new_img = Image.new('RGB', input_img.size, (255, 255, 255))
            new_img.paste(input_img, mask=input_img.split()[3] if input_img.mode == 'LA' else input_img.split()[3])

            # Return the modified image as bytes
            with BytesIO() as output_buffer:
                new_img.save(output_buffer, format="PNG")
                return output_buffer.getvalue()
        else:
            print("The image does not have a transparent background.")
            return image_data


def get_last_subdirectory(path):
    if path == "/":
        return ""

    # Use os.path.normpath to handle variations in path separators
    normalized_path = os.path.normpath(path)

    # Use os.path.split to split the path into the head and tail
    head, tail = os.path.split(normalized_path)

    # If there is a tail (i.e., the path is not just a root directory)
    if tail:
        return tail
    else:
        # If the path ends with a slash, get the last non-empty part
        parts = normalized_path.split(os.path.sep)
        non_empty_parts = [part for part in parts if part]
        return non_empty_parts[-1]
