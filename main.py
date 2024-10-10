# main.py

import pygame
from settings import *
from ship import Ship
from background import generate_stars, draw_background

def main():
    pygame.init()
    WIN = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # Générer les étoiles
    stars = generate_stars()

    run = True
    ship = Ship(MAP_WIDTH // 2, MAP_HEIGHT // 2)

    while run:
        dt = clock.tick(FRAME_RATE) / 1000  # Durée d'une frame en secondes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        throttle_inputs = ship.get_thruster_inputs(keys)
        ship.apply_thrusters(throttle_inputs, dt)
        ship.update(dt)

        camera_offset = ship.position - pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)
        camera_offset.x = max(0, min(camera_offset.x, MAP_WIDTH - WIDTH))
        camera_offset.y = max(0, min(camera_offset.y, MAP_HEIGHT - HEIGHT))

        WIN.fill(BLACK)
        draw_background(WIN, camera_offset, stars)
        ship.draw(WIN, camera_offset)
        ship.draw_info(WIN)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
