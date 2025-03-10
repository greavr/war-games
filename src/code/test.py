import pygame
import sys
import os
import math

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HEX_SIZE = 50  # Radius of the hexagon
HEX_SPACING = 2  # Spacing between hexagons
BACKGROUND_COLOR = (255, 255, 255)  # White

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hexagon Tile Layout")

# --- Load Tile Images ---
def load_tile_images(tile_folder):
    """Loads tile images from a folder."""
    tile_images = {}
    try:
        for filename in os.listdir(tile_folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(tile_folder, filename)
                tile_images[filename] = pygame.image.load(image_path).convert()
    except FileNotFoundError:
        print(f"Error: Tile folder '{tile_folder}' not found.")
    return tile_images

tile_folder = "tiles"  # Replace with your tile folder
tile_images = load_tile_images(tile_folder)

# --- Hexagon Drawing Function ---
def draw_hexagon(surface, color, center, size):
    """Draws a hexagon on the surface."""
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        x = center[0] + size * math.cos(angle_rad)
        y = center[1] + size * math.sin(angle_rad)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)

def draw_hexagon_tile(surface, center, size, tile_image):
    """Draws a hexagon tile with a loaded image."""
    mask = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    draw_hexagon(mask, (255, 255, 255, 255), (size, size), size)
    mask_rect = mask.get_rect(center=center)

    scaled_tile = pygame.transform.scale(tile_image, (size * 2, size * 2))
    surface.blit(scaled_tile, mask_rect, special_flags=pygame.BLEND_RGBA_MULT)
    surface.blit(mask, mask_rect, special_flags=pygame.BLEND_RGBA_MULT)

# --- Hexagon Grid Layout ---
def create_hexagon_grid(screen, tile_images):
    """Creates and draws a hexagon grid."""
    x_offset = HEX_SIZE * math.sqrt(3) + HEX_SPACING
    y_offset = HEX_SIZE * 1.5 + HEX_SPACING

    for row in range(10):  # Adjust rows as needed
        for col in range(10):  # Adjust columns as needed
            x = col * x_offset + (x_offset / 2 if row % 2 != 0 else 0) + HEX_SIZE
            y = row * y_offset + HEX_SIZE

            center = (x, y)
            if tile_images:
                tile_filename = list(tile_images.keys())[ (row + col) % len(tile_images)]
                draw_hexagon_tile(screen, center, HEX_SIZE, tile_images[tile_filename])
            else:
                draw_hexagon(screen, (0, 0, 0), center, HEX_SIZE)

# --- Main Game Loop ---
def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)
        create_hexagon_grid(screen, tile_images)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()