# effects.py - Functions for dynamic effects and anti-tampering mechanisms

import time
from PIL import Image as PILImage  # Temporary dependency
from .core import Image  # Relative import for the Image class

def twinkle_stars(image, star_positions, duration=5, interval=0.1):
    """
    Simulate twinkling stars by dynamically changing brightness.

    :param image: Image object.
    :param star_positions: List of tuples [(x1, y1), (x2, y2), ...] representing star positions.
    :param duration: Total duration of the twinkling effect in seconds.
    :param interval: Time interval between frames in seconds.
    """
    frames = []
    steps = int(duration / interval)
    base_pixels = image.pixels.copy()  # Preserve the original image

    for step in range(steps):
        temp_image = Image(image.width, image.height, background_color=(0, 0, 0))
        temp_image.pixels = base_pixels.copy()  # Start with the original image

        for x, y in star_positions:
            brightness = int(255 * (0.5 + 0.5 * (step % 2)))  # Alternate brightness
            temp_image.set_pixel(x, y, (brightness, brightness, brightness))

        frames.append(PILImage.fromarray(temp_image.pixels, 'RGB'))

    # Save as GIF
    frames[0].save(
        "twinkling_stars.gif",
        save_all=True,
        append_images=frames[1:],
        duration=int(interval * 1000),
        loop=0
    )

def add_micro_pattern(image, pattern_data):
    """
    Embed a micro-pattern into the image for anti-tampering.

    :param image: Image object.
    :param pattern_data: Binary data to embed as a micro-pattern.
    """
    width, height = image.width, image.height
    binary_data = ''.join(format(byte, '08b') for byte in pattern_data)
    data_length = len(binary_data)

    index = 0
    for x in range(width):
        for y in range(height):
            if index < data_length:
                r, g, b = image.get_pixel(x, y)
                bit = int(binary_data[index])
                r = (r & ~1) | bit  # Modify the least significant bit
                image.set_pixel(x, y, (r, g, b))
                index += 1