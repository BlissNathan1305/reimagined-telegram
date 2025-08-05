import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random

# -------------------------------
# Configuration
# -------------------------------
WIDTH, HEIGHT = 1440, 3200  # Common high-end mobile resolution
OUTPUT_DIR = "wallpapers"
OUTPUT_FORMAT = "JPEG"
QUALITY = 95

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Trendy color palettes (2024 styles: soft pastels, duotones, cyber gradients)
PALETTES = {
    "soft_sunset": ["#F9C4B4", "#F8A5C2", "#E07AAE", "#C05A9C"],
    "ocean_dream": ["#7ED6DF", "#26C6DA", "#00ACC1", "#008C9E"],
    "cyber_purple": ["#9D50BB", "#B16CE5", "#C780FA", "#D5A6F4"],
    "morning_light": ["#FFEAA7", "#F6E58D", "#F9CA24", "#F0932B"],
    "neon_twilight": ["#667eea", "#764ba2", "#8b5cf6", "#d946ef"],
    "mint_frost": ["#a8e6cf", "#dcedc1", "#ffd5c2", "#ffaaa5"]
}

def random_color(palette_name=None):
    palette = PALETTES.get(palette_name) if palette_name else random.choice(list(PALETTES.values()))
    return random.choice(palette)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def draw_gradient(img, draw, color1, color2, vertical=True):
    """Draws a smooth gradient between two colors."""
    start = hex_to_rgb(color1)
    end = hex_to_rgb(color2)
    for i in range(WIDTH if not vertical else HEIGHT):
        ratio = i / (WIDTH if not vertical else HEIGHT)
        r = int(start[0] * (1 - ratio) + end[0] * ratio)
        g = int(start[1] * (1 - ratio) + end[1] * ratio)
        b = int(start[2] * (1 - ratio) + end[2] * ratio)
        color = (r, g, b)
        if vertical:
            draw.line([(0, i), (WIDTH, i)], fill=color, width=1)
        else:
            draw.line([(i, 0), (i, HEIGHT)], fill=color, width=1)

def draw_circle_pattern(img, color, alpha=64, count=15):
    """Draws semi-transparent floating circles on the given image."""
    r, g, b = hex_to_rgb(color)
    rgba_color = (r, g, b, alpha)
    
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    
    for _ in range(count):
        x = random.randint(-WIDTH//2, WIDTH)
        y = random.randint(-HEIGHT//2, HEIGHT)
        size = random.randint(WIDTH//10, WIDTH//3)
        draw_overlay.ellipse([x, y, x + size, y + size], fill=rgba_color)
    
    img.paste(overlay, (0, 0), overlay)  # Use overlay as mask for transparency

def add_noise(img, intensity=10):
    """Adds subtle noise for texture."""
    noise = Image.new("RGB", img.size, (0, 0, 0))
    for x in range(img.width):
        for y in range(img.height):
            value = random.randint(0, intensity)
            noise.putpixel((x, y), (value, value, value))
    img = Image.blend(img, noise, 0.05)
    return img

def generate_wallpaper(index):
    # Choose a random palette
    palette_name = random.choice(list(PALETTES.keys()))
    bg_color1 = random_color(palette_name)
    bg_color2 = random_color(palette_name)
    accent_color = random_color(palette_name)

    # Create base image in RGB
    img = Image.new("RGB", (WIDTH, HEIGHT), bg_color1)
    draw = ImageDraw.Draw(img)

    # Draw vertical gradient
    draw_gradient(img, draw, bg_color1, bg_color2, vertical=True)

    # Convert to RGBA to support transparency
    img = img.convert("RGBA")

    # Add semi-transparent circle patterns
    draw_circle_pattern(img, accent_color, alpha=40, count=10)
    draw_circle_pattern(img, random_color(palette_name), alpha=30, count=8)

    # Convert back to RGB to apply blur and save as JPEG
    rgb_img = img.convert("RGB")

    # Apply soft blur for depth (glassmorphism-inspired)
    blurred = rgb_img.filter(ImageFilter.GaussianBlur(radius=50))
    blended = Image.blend(blurred, rgb_img, 0.7)  # 70% sharp, 30% blur

    # Add subtle noise texture
    blended = add_noise(blended, intensity=15)

    # Enhance contrast and color slightly
    enhancer = ImageEnhance.Contrast(blended)
    blended = enhancer.enhance(1.1)
    enhancer = ImageEnhance.Color(blended)
    blended = enhancer.enhance(1.15)

    # Save as high-quality JPEG
    filename = os.path.join(OUTPUT_DIR, f"wallpaper_{index:03d}.jpg")
    blended.save(filename, format=OUTPUT_FORMAT, quality=QUALITY, optimize=True)
    print(f"Generated: {filename}")

# -------------------------------
# Generate multiple wallpapers
# -------------------------------
if __name__ == "__main__":
    num_wallpapers = 5  # Change as needed
    print(f"Generating {num_wallpapers} 4K mobile wallpapers...")
    for i in range(num_wallpapers):
        generate_wallpaper(i + 1)
    print("✅ All wallpapers generated!")
