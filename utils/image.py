import os


def save_image(image, output_filename, output_directory):
    filename = os.path.join(output_directory, f"{output_filename}-{image.name}")

    with open(filename, "wb") as image_file:
        image_file.write(image.data)

    relative_file_location = os.path.join(get_last_subdirectory(output_directory), get_last_subdirectory(filename))

    return f"![]({relative_file_location})"


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
