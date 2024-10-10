# game/ship_part.py

import pygame

class ShipPart:
    def __init__(self, name, relative_pos, image=None, shape=None, color=(255, 255, 255)):
        self.name = name
        self.relative_pos = pygame.math.Vector2(relative_pos)
        self.image = image  # Image Pygame.Surface
        self.shape = shape  # Liste de points pour dessiner une forme
        self.color = color  # Couleur de la forme si aucune image n'est fournie

    def draw(self, surface, ship_position, ship_angle):
        if self.image:
            # Si une image est fournie, la dessiner avec la rotation appropriée
            rotated_image = pygame.transform.rotate(self.image, -ship_angle)
            rotated_rect = rotated_image.get_rect()
            rotated_pos = self.relative_pos.rotate(ship_angle)
            rotated_rect.center = ship_position + rotated_pos
            surface.blit(rotated_image, rotated_rect)
        elif self.shape:
            # Dessiner la forme définie
            rotated_shape = [point.rotate(ship_angle) + ship_position + self.relative_pos.rotate(ship_angle) for point in self.shape]
            pygame.draw.polygon(surface, self.color, rotated_shape)
        else:
            # Dessiner un rectangle par défaut si aucune image ou forme n'est fournie
            size = (20, 20)
            part_surf = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.rect(part_surf, self.color, part_surf.get_rect())
            rotated_part_surf = pygame.transform.rotate(part_surf, -ship_angle)
            rotated_rect = rotated_part_surf.get_rect()
            rotated_pos = self.relative_pos.rotate(ship_angle)
            rotated_rect.center = ship_position + rotated_pos
            surface.blit(rotated_part_surf, rotated_rect)
