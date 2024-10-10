# game/thruster.py

import pygame
import math
from settings import THRUSTER_ACTIVE_COLOR, THRUSTER_INACTIVE_COLOR

class Thruster:
    def __init__(self, name, relative_pos, max_force, direction, ship_part=None):
        self.name = name
        self.relative_pos = pygame.math.Vector2(relative_pos)
        self.max_force = max_force
        self.direction = direction  # Angle en degrés
        self.active = False
        self.current_force = 0
        self.ship_part = ship_part  # ShipPart associée au thruster

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
        # Dessiner la ShipPart associée si elle existe
        if self.ship_part:
            self.ship_part.draw(surface, ship_position, ship_angle)

        # Dessiner l'indicateur d'activation du thruster (optionnel)
        if self.active:
            color = THRUSTER_ACTIVE_COLOR
            size = (10, 5)
            thruster_surf = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.rect(thruster_surf, color, thruster_surf.get_rect())
            rotated_pos = self.relative_pos.rotate(ship_angle)
            thruster_position = ship_position + rotated_pos
            total_angle = ship_angle + self.direction
            rotated_thruster_surf = pygame.transform.rotate(thruster_surf, -total_angle)
            rotated_thruster_rect = rotated_thruster_surf.get_rect()
            rotated_thruster_rect.center = thruster_position
            surface.blit(rotated_thruster_surf, rotated_thruster_rect)
