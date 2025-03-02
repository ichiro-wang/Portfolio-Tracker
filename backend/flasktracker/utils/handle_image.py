from PIL import Image
from werkzeug.utils import secure_filename
import os
import secrets
import io


def handle_image(file):
    # ensure filename is safe
    safe_file_name = secure_filename(file.filename)

    # take filename and make a random name for storage
    file_name, file_ext = os.path.splitext(safe_file_name)
    file_ext = file_ext.lower()

    if file_ext in [".jpg", ".jpeg"]:
        file_ext = ".jpeg"
        image_format = "JPEG"
        content_type = "image/jpeg"
    elif file_ext == ".png":
        image_format = "PNG"
        content_type = "image/png"
    else:
        raise Exception("Invalid file format")

    random_hex = secrets.token_hex(8)
    storage_file_name = random_hex + "_" + file_name + file_ext

    # resize using PIL for storage purposes
    output_size = (150, 150)
    i = Image.open(file)
    i.thumbnail(output_size)

    # convert pil image to in-memory bytesio
    image_io = io.BytesIO()
    i.save(image_io, format=image_format)
    image_io.seek(0)

    return image_io, storage_file_name, content_type
