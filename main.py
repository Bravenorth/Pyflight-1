# main.py

import pygame
from settings import *
from game.ship import Ship
from game.background import generate_stars, draw_background

def main():
    pygame.init()
    WIN = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # Générer les étoiles
    stars = generate_stars()

    run = True
    ship = Ship(MAP_WIDTH // 2, MAP_HEIGHT // 2)
    lasers = []  # Liste pour stocker les lasers actifs

    while run:
        dt = clock.tick(FRAME_RATE) / 1000  # Durée d'une frame en secondes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        throttle_inputs = ship.get_thruster_inputs(keys)
        ship.apply_thrusters(throttle_inputs, dt)
        ship.update(dt)

        # Gérer le tir du laser
        if keys[pygame.K_SPACE]:
            new_laser = ship.fire_laser()
            if new_laser is not None:
                lasers.append(new_laser)

        # Mettre à jour les lasers
        for laser in lasers[:]:
            laser.update(dt)
            # Supprimer les lasers qui ont dépassé leur durée de vie ou sont hors de la carte
            if laser.age > laser.lifetime:
                lasers.remove(laser)
            elif (laser.position.x < 0 or laser.position.x > MAP_WIDTH or
                  laser.position.y < 0 or laser.position.y > MAP_HEIGHT):
                lasers.remove(laser)

        camera_offset = ship.position - pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)
        camera_offset.x = max(0, min(camera_offset.x, MAP_WIDTH - WIDTH))
        camera_offset.y = max(0, min(camera_offset.y, MAP_HEIGHT - HEIGHT))

        WIN.fill(BLACK)
        draw_background(WIN, camera_offset, stars)
        ship.draw(WIN, camera_offset)
        ship.draw_info(WIN)

        # Dessiner les lasers
        for laser in lasers:
            laser.draw(WIN, camera_offset)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
