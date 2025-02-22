# tests/test_core.py - Test script for core.py and shapes.py

from scigimage.core import Image
from scigimage.shapes import draw_circle, draw_line

# Create a blank image
img = Image(512, 512, background_color=(255, 255, 255))  # White background

# Draw a red circle
draw_circle(img, 100, 100, 50, (255, 0, 0))  # Red circle at (100, 100) with radius 50

# Draw a blue line
draw_line(img, 200, 50, 400, 200, (0, 0, 255))  # Blue line from (200, 50) to (400, 200)

# Save the image
img.save("test_shapes.png")

# Display the image
img.show()