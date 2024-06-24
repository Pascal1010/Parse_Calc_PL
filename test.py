import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Unlimited Map Camera Movement")

# Tile settings
tile_size = 50

# Camera settings
camera_x = 0
camera_y = 0
camera_speed = 5

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current state of all keyboard buttons
    keys = pygame.key.get_pressed()

    # Update camera position based on arrow key presses
    if keys[pygame.K_LEFT]:
        camera_x -= camera_speed
    if keys[pygame.K_RIGHT]:
        camera_x += camera_speed
    if keys[pygame.K_UP]:
        camera_y -= camera_speed
    if keys[pygame.K_DOWN]:
        camera_y += camera_speed

    # Clear the screen
    screen.fill(black)

    # Draw the visible part of the map
    start_x = camera_x // tile_size * tile_size
    start_y = camera_y // tile_size * tile_size
    end_x = (camera_x + screen_width) // tile_size * tile_size + tile_size
    end_y = (camera_y + screen_height) // tile_size * tile_size + tile_size

    for y in range(start_y, end_y, tile_size):
        for x in range(start_x, end_x, tile_size):
            color = ((x // tile_size) % 255, (y // tile_size) % 255, ((x // tile_size) + (y // tile_size)) % 255)
            draw_x = x - camera_x
            draw_y = y - camera_y
            pygame.draw.rect(screen, color, (draw_x, draw_y, tile_size, tile_size))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
