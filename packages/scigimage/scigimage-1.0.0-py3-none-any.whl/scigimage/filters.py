# filters.py - Functions for applying image processing filters

import numpy as np
from scipy.ndimage import gaussian_filter

def gaussian_blur(image, kernel_size=3, sigma=1):
    """
    Apply Gaussian blur to the image.

    :param image: Image object.
    :param kernel_size: Size of the Gaussian kernel.
    :param sigma: Standard deviation of the Gaussian distribution.
    """
    blurred_pixels = gaussian_filter(image.pixels, sigma=sigma)
    image.pixels = blurred_pixels.astype(np.uint8)

def threshold(image, threshold_value=128):
    """
    Convert the image to binary (black-and-white) based on a threshold.

    :param image: Image object.
    :param threshold_value: Threshold value for binarization.
    """
    gray = np.dot(image.pixels[..., :3], [0.2989, 0.5870, 0.1140])  # Convert to grayscale
    binary = (gray > threshold_value) * 255
    image.pixels = np.stack([binary] * 3, axis=-1).astype(np.uint8)