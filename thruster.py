# thruster.py

import pygame
import math
from settings import THRUSTER_ACTIVE_COLOR, THRUSTER_INACTIVE_COLOR, BLACK

class Thruster:
    def __init__(self, name, relative_pos, max_force, direction):
        self.name = name
        self.relative_pos = pygame.math.Vector2(relative_pos)
        self.max_force = max_force
        self.direction = direction  # Angle en degrés
        self.active = False
        self.current_force = 0

    def get_force(self, throttle, ship_angle):
        thrust_direction = ship_angle + self.direction
        force_magnitude = self.max_force * max(0.0, min(throttle, 1.0))
        self.current_force = force_magnitude
        force = pygame.math.Vector2(
            math.sin(math.radians(thrust_direction)),
            -math.cos(math.radians(thrust_direction))
        ) * force_magnitude
        return force

    def draw(self, surface, ship_position, ship_angle):
        color = THRUSTER_ACTIVE_COLOR if self.active else THRUSTER_INACTIVE_COLOR
        size = (10, 5)
        thruster_surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(thruster_surf, color, thruster_surf.get_rect())

        # Calculer la position du propulseur après rotation
        rotated_pos = self.relative_pos.rotate(ship_angle)
        thruster_position = ship_position + rotated_pos

        # Calculer l'angle total du thruster
        total_angle = ship_angle + self.direction

        # Faire pivoter le thruster
        rotated_thruster_surf = pygame.transform.rotate(thruster_surf, -total_angle)
        rotated_thruster_rect = rotated_thruster_surf.get_rect()
        rotated_thruster_rect.center = thruster_position

        surface.blit(rotated_thruster_surf, rotated_thruster_rect)
