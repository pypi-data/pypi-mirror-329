# test_scigimage.py - Comprehensive test script for scigimage

from scigimage.core import Image
from scigimage.shapes import draw_circle, draw_line, draw_random_gradient, draw_star_influenced_gradient, add_noise
from scigimage.effects import twinkle_stars, add_micro_pattern
from scigimage.filters import gaussian_blur
from scigimage.utils import save_as_custom_format

def test_core_functionality():
    print("Testing core functionality...")
    img = Image(512, 512, background_color=(0, 0, 0))  # Black background

    # Draw a white circle
    draw_circle(img, 256, 256, 100, (255, 255, 255))

    # Draw a red line
    draw_line(img, 100, 100, 400, 400, (255, 0, 0))

    # Add random gradient
    draw_random_gradient(img)

    # Add noise
    add_noise(img, intensity=30)

    # Save the image
    img.save("test_output.png")
    print("Core functionality test complete. Output saved as 'test_output.png'.")

def test_twinkling_stars():
    print("Testing twinkling stars animation...")
    img = Image(512, 512, background_color=(0, 0, 0))  # Black background

    # Add stars
    star_positions = [(256, 256), (300, 300), (200, 200)]
    for x, y in star_positions:
        img.set_pixel(x, y, (255, 255, 255))  # White stars

    # Generate twinkling stars animation
    twinkle_stars(img, star_positions, duration=5, interval=0.1)
    print("Twinkling stars test complete. Animation saved as 'twinkling_stars.gif'.")

def test_anti_tampering():
    print("Testing anti-tampering mechanisms...")
    img = Image(512, 512, background_color=(0, 0, 0))  # Black background

    # Embed micro-pattern
    add_micro_pattern(img, b"SECURE_DATA")

    # Save the image with embedded pattern
    img.save("test_micro_pattern.png")
    print("Anti-tampering test complete. Output saved as 'test_micro_pattern.png'.")

def test_filters():
    print("Testing filters...")
    img = Image(512, 512, background_color=(0, 0, 0))  # Black background

    # Draw a white circle
    draw_circle(img, 256, 256, 100, (255, 255, 255))

    # Apply Gaussian blur
    gaussian_blur(img, sigma=2)

    # Save the image
    img.save("test_blur.png")
    print("Filters test complete. Output saved as 'test_blur.png'.")

def test_error_handling():
    print("Testing error handling...")
    try:
        img = Image(-512, 512, background_color=(0, 0, 0))  # Invalid width
    except ValueError as e:
        print(f"Error handling test passed: {e}")

    try:
        draw_circle(None, 256, 256, 100, (255, 255, 255))  # Invalid image object
    except Exception as e:
        print(f"Error handling test passed: {e}")

    print("Error handling tests complete.")

if __name__ == "__main__":
    test_core_functionality()
    test_twinkling_stars()
    test_anti_tampering()
    test_filters()
    test_error_handling()
    print("All tests completed.")