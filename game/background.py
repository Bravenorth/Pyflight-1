# game/background.py

import pygame
import random
from settings import MAP_WIDTH, MAP_HEIGHT

def generate_stars(num_stars=1500):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, MAP_WIDTH)
        y = random.randint(0, MAP_HEIGHT)
        radius = random.randint(1, 3)
        color = random.choice([
            (255, 255, 255),
            (200, 200, 255),
            (255, 200, 200),
            (255, 255, 200)
        ])
        stars.append((x, y, radius, color))
    return stars

def draw_background(surface, camera_offset, stars):
    for star in stars:
        star_pos = (star[0] - camera_offset.x, star[1] - camera_offset.y)
        pygame.draw.circle(surface, star[3], star_pos, star[2])
