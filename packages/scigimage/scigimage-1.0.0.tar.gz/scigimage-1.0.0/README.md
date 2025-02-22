# scigimage

`scigimage` is a lightweight Python library for generating visually dynamic star maps with twinkling effects and animations. It provides tools for basic image manipulation, gradient generation, and anti-tampering mechanisms.

## Features

- Generate star maps with twinkling stars.
- Add gradients and noise for visual complexity.
- Export animations as GIFs.
- Embed micro-patterns for anti-tampering.
- Modular design for extensibility.

## Installation

Install the library using `pip`:

```bash
pip install scigimage

```

USAGE:
from scigimage.core import Image
from scigimage.shapes import draw_circle, draw_line
from scigimage.effects import twinkle_stars

# Create a blank image

img = Image(512, 512, background_color=(0, 0, 0))

# Draw a white circle

draw_circle(img, 256, 256, 100, (255, 255, 255))

# Add twinkling stars

twinkle_stars(img, [(256, 256)], duration=5, interval=0.1)

# Save the output

img.save("output.png")
