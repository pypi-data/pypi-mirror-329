# shapes.py - Functions for drawing shapes, gradients, and noise

import numpy as np
import random

def draw_circle(image, x, y, radius, color):
    """
    Draw a circle on the image.

    :param image: Image object.
    :param x: X-coordinate of the circle's center.
    :param y: Y-coordinate of the circle's center.
    :param radius: Radius of the circle.
    :param color: Tuple representing the RGB color of the circle.
    """
    if radius <= 0:
        raise ValueError("Radius must be greater than 0.")
    
    for i in range(x - radius, x + radius + 1):
        for j in range(y - radius, y + radius + 1):
            if (i - x) ** 2 + (j - y) ** 2 <= radius ** 2:
                try:
                    image.set_pixel(i, j, color)
                except IndexError:
                    pass

def draw_line(image, x1, y1, x2, y2, color):
    """
    Draw a line on the image using Bresenham's algorithm.

    :param image: Image object.
    :param x1: X-coordinate of the start point.
    :param y1: Y-coordinate of the start point.
    :param x2: X-coordinate of the end point.
    :param y2: Y-coordinate of the end point.
    :param color: Tuple representing the RGB color of the line.
    """
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        try:
            image.set_pixel(x1, y1, color)
        except IndexError:
            pass
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def draw_random_gradient(image):
    """
    Draw a random gradient across the image.

    :param image: Image object.
    """
    width, height = image.width, image.height
    for x in range(width):
        # Generate random colors for each column
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        for y in range(height):
            image.set_pixel(x, y, (r, g, b))

def draw_star_influenced_gradient(image, star_positions, base_color=(255, 0, 0), influence_radius=50):
    """
    Draw a gradient influenced by star positions.

    :param image: Image object.
    :param star_positions: List of tuples [(x1, y1), (x2, y2), ...] representing star positions.
    :param base_color: Tuple representing the base RGB color of the gradient.
    :param influence_radius: Radius around each star where the gradient is influenced.
    """
    width, height = image.width, image.height
    for x in range(width):
        for y in range(height):
            # Start with the base color
            r, g, b = base_color

            # Modify color based on proximity to stars
            for sx, sy in star_positions:
                distance = ((x - sx) ** 2 + (y - sy) ** 2) ** 0.5
                if distance < influence_radius:
                    # Add variation near stars
                    r += int((255 - r) * (1 - distance / influence_radius))
                    g += int((255 - g) * (1 - distance / influence_radius))
                    b += int((255 - b) * (1 - distance / influence_radius))

            # Clamp values to valid range
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            image.set_pixel(x, y, (r, g, b))

def add_noise(image, intensity=50):
    """
    Add random noise to the image.

    :param image: Image object.
    :param intensity: Intensity of the noise (default is 50).
    """
    width, height = image.width, image.height
    for x in range(width):
        for y in range(height):
            r, g, b = image.get_pixel(x, y)
            r += np.random.randint(-intensity, intensity)
            g += np.random.randint(-intensity, intensity)
            b += np.random.randint(-intensity, intensity)
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            image.set_pixel(x, y, (r, g, b))