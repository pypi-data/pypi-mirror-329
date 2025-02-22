# core.py - Core functionality for image creation and pixel manipulation

import numpy as np

class Image:
    """
    A class to represent an image with customizable dimensions and background color.
    Pixel data is stored as a scignumpy array (using standard numpy for now).
    """

    def __init__(self, width, height, background_color=(0, 0, 0)):
        """
        Initialize a blank image with the given dimensions and background color.

        :param width: Width of the image in pixels.
        :param height: Height of the image in pixels.
        :param background_color: Tuple representing the RGB background color (default is black).
        """
        self.width = width
        self.height = height
        self.background_color = background_color
        # Create a blank canvas using numpy
        self.pixels = np.full((height, width, 3), background_color, dtype=np.uint8)

    def get_pixel(self, x, y):
        """
        Get the RGB value of a pixel at the specified coordinates.

        :param x: X-coordinate of the pixel.
        :param y: Y-coordinate of the pixel.
        :return: Tuple representing the RGB value of the pixel.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return tuple(self.pixels[y, x])
        else:
            raise IndexError("Pixel coordinates out of bounds.")

    def set_pixel(self, x, y, color):
        """
        Set the RGB value of a pixel at the specified coordinates.

        :param x: X-coordinate of the pixel.
        :param y: Y-coordinate of the pixel.
        :param color: Tuple representing the RGB value to set.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y, x] = color
        else:
            raise IndexError("Pixel coordinates out of bounds.")

    def save(self, file_path, format="PNG"):
        """
        Save the image to a file.

        :param file_path: Path to save the image file.
        :param format: Format of the image file (default is PNG).
        """
        from PIL import Image as PILImage  # Use Pillow for saving (temporary dependency)
        img = PILImage.fromarray(self.pixels, 'RGB')
        img.save(file_path, format=format)

    def show(self):
        """
        Display the image using Pillow's built-in viewer.
        """
        from PIL import Image as PILImage  # Use Pillow for displaying (temporary dependency)
        img = PILImage.fromarray(self.pixels, 'RGB')
        img.show()