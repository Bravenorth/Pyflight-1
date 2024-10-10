# game/laser.py

import pygame
import math
from settings import WHITE, LASER_SPEED, LASER_LIFETIME

class Laser:
    def __init__(self, position, angle):
        self.position = pygame.math.Vector2(position)
        self.angle = angle  # Angle en degrés
        self.speed = LASER_SPEED
        self.velocity = pygame.math.Vector2(
            math.sin(math.radians(self.angle)),
            -math.cos(math.radians(self.angle))
        ) * self.speed
        self.lifetime = LASER_LIFETIME
        self.age = 0  # Temps écoulé depuis le tir du laser

    def update(self, dt):
        self.position += self.velocity * dt
        self.age += dt

    def draw(self, surface, camera_offset):
        # Dessiner le laser comme un petit cercle
        laser_pos = self.position - camera_offset
        pygame.draw.circle(surface, WHITE, (int(laser_pos.x), int(laser_pos.y)), 2)
