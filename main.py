# Space Invader 1.0
# Main File

# Importing all module needed...
import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 850, 850
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader 2.0")

# Load images for our game...
RED_SPACE_SHIP = pygame.image.load(os.path.join("images", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("images", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("images", "pixel_ship_blue_small.png"))

# Main player's ship...
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("images", "pixel_ship_yellow.png"))

# Laser...
RED_LASER = pygame.image.load(os.path.join("images", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("images", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("images", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("images", "pixel_laser_yellow.png"))

# Background...
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images", "background-black.png")), (HEIGHT, WIDTH))

# Other essential properties...
def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("arialblack", 50)

    clock = pygame.time.Clock()

# Drawing the background...
    def redraw_window():
        WIN.blit(BACKGROUND, (0,0))
        # Draw Text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

# Quit the game by pressing the "x"...
        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                run = False

main()