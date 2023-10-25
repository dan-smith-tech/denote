def save_image(image, output_directory):
    filename = f"{output_directory}/{image.name}"

    with open(filename, "wb") as image_file:
        image_file.write(image.data)

    return f"![]({filename})"
