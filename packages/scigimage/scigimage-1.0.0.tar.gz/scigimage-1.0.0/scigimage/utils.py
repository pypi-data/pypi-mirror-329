# utils.py - Utility functions for saving images in custom and standard formats

import zlib
import struct

def save_as_png(image, file_path):
    """
    Save the image as a PNG file using a custom implementation.

    :param image: Image object.
    :param file_path: Path to save the PNG file.
    """
    width, height = image.width, image.height
    pixels = image.pixels

    # Convert pixels to bytes
    pixel_data = bytearray()
    for row in pixels:
        for r, g, b in row:
            pixel_data.extend([r, g, b])

    # Compress pixel data
    compressed_data = zlib.compress(pixel_data)

    # Create PNG file structure
    def png_chunk(chunk_type, data):
        return struct.pack("!I", len(data)) + chunk_type + data + struct.pack("!I", zlib.crc32(chunk_type + data))

    ihdr = png_chunk(b"IHDR", struct.pack("!2I5B", width, height, 8, 2, 0, 0, 0))
    idat = png_chunk(b"IDAT", compressed_data)
    iend = png_chunk(b"IEND", b"")

    with open(file_path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")  # PNG signature
        f.write(ihdr)
        f.write(idat)
        f.write(iend)

def save_as_custom_format(image, file_path):
    """
    Save the image in a custom format optimized for star maps.

    :param image: Image object.
    :param file_path: Path to save the custom image file.
    """
    with open(file_path, "wb") as f:
        f.write(b"SCIGIMAGE_CUSTOM_FORMAT\n")
        f.write(struct.pack("!2I", image.width, image.height))  # Width and height
        f.write(image.pixels.tobytes())  # Pixel data