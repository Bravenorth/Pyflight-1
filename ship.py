# ship.py

import pygame
from settings import *
from thruster import Thruster

class Ship:
    def __init__(self, x, y):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.mass = SHIP_MASS
        self.linear_damping = LINEAR_DAMPING
        self.thrusters = []
        self.ship_width, self.ship_height = 40, 80
        self.active_thrusters = set()
        self.angle = 0  # Angle du vaisseau en degrés
        self.angular_velocity = 0  # Vitesse angulaire en degrés par seconde
        self.angular_damping = 0.05  # Facteur d'amortissement angulaire
        self.moment_of_inertia = 5000  # Moment d'inertie du vaisseau

        self.initialize_thrusters()

    def add_thruster(self, thruster):
        self.thrusters.append(thruster)

    def apply_thrusters(self, throttle_inputs, dt):
        total_force = pygame.math.Vector2(0, 0)
        total_torque = 0  # Initialiser le couple total à zéro

        # Réinitialiser les propulseurs inactifs
        current_active_thrusters = set(thruster for thruster, _ in throttle_inputs)
        thrusters_to_reset = self.active_thrusters - current_active_thrusters
        for thruster in thrusters_to_reset:
            thruster.active = False
            thruster.current_force = 0
        self.active_thrusters = current_active_thrusters

        for thruster, throttle in throttle_inputs:
            thruster.active = True
            thrust_force = thruster.get_force(throttle, self.angle)
            total_force += thrust_force

            # Calcul du bras de levier (distance du thruster au centre du vaisseau après rotation)
            lever_arm = thruster.relative_pos.rotate(self.angle)
            # Calcul du couple (torque) : τ = r × F
            torque = lever_arm.cross(thrust_force)
            total_torque += torque

        # Mise à jour de la vitesse linéaire
        self.velocity += (total_force / self.mass) * dt

        # Mise à jour de la vitesse angulaire
        angular_acceleration = total_torque / self.moment_of_inertia
        self.angular_velocity += angular_acceleration * dt

        # Appliquer l'amortissement angulaire
        self.angular_velocity *= (1 - self.angular_damping)

        # Mise à jour de l'angle du vaisseau
        self.angle += self.angular_velocity * dt
        self.angle %= 360  # S'assurer que l'angle reste entre 0 et 360 degrés

        # Amortissement linéaire
        damping_factor = max(0, 1 - self.linear_damping * (self.velocity.length() ** 0.5) * dt)
        self.velocity *= damping_factor

    def update(self, dt):
        self.position += self.velocity * dt

        # Limiter la position du vaisseau aux limites de la carte
        self.position.x = max(0, min(self.position.x, MAP_WIDTH))
        self.position.y = max(0, min(self.position.y, MAP_HEIGHT))

    def draw(self, surface, camera_offset):
        # Créer une surface pour le vaisseau
        ship_surf = pygame.Surface((self.ship_width, self.ship_height), pygame.SRCALPHA)
        pygame.draw.polygon(ship_surf, WHITE, [
            (self.ship_width / 2, 0),
            (0, self.ship_height),
            (self.ship_width, self.ship_height)
        ])

        # Faire pivoter la surface du vaisseau
        rotated_ship_surf = pygame.transform.rotate(ship_surf, -self.angle)
        rotated_ship_rect = rotated_ship_surf.get_rect(center=self.position - camera_offset)

        # Dessiner le vaisseau
        surface.blit(rotated_ship_surf, rotated_ship_rect)

        # Dessiner les thrusters
        for thruster in self.thrusters:
            thruster.draw(surface, self.position - camera_offset, self.angle)

    def draw_info(self, surface):
        y_offset = 10
        for thruster in self.thrusters:
            status = "Actif" if thruster.active else "Inactif"
            text = f"{thruster.name}: {status}, Force: {thruster.current_force:.1f} N"
            text_surface = FONT.render(text, True, WHITE)
            surface.blit(text_surface, (10, y_offset))
            y_offset += 20

        # Calcul de la vitesse en km/h
        speed_mps = self.velocity.length()
        speed_kph = speed_mps * 3.6

        speed_text = f"Vitesse: {speed_mps:.1f} m/s ({speed_kph:.1f} km/h)"
        speed_surface = FONT.render(speed_text, True, WHITE)
        surface.blit(speed_surface, (10, y_offset))
        y_offset += 20

        position_text = f"Position: ({self.position.x:.1f}, {self.position.y:.1f})"
        position_surface = FONT.render(position_text, True, WHITE)
        surface.blit(position_surface, (10, y_offset))
        y_offset += 20

        angle_text = f"Angle: {self.angle:.1f}°, Vitesse angulaire: {self.angular_velocity:.1f}°/s"
        angle_surface = FONT.render(angle_text, True, WHITE)
        surface.blit(angle_surface, (10, y_offset))

    def get_thruster_inputs(self, keys):
        throttle_inputs = []
        if keys[pygame.K_z]:
            throttle_inputs.append((self.main_thruster, 1.0))
        if keys[pygame.K_s]:
            throttle_inputs.append((self.reverse_thruster, 1.0))
        if keys[pygame.K_q]:
            throttle_inputs.append((self.left_thruster, 1.0))
        if keys[pygame.K_d]:
            throttle_inputs.append((self.right_thruster, 1.0))
        # Contrôles de rotation manuelle
        if keys[pygame.K_LEFT]:
            self.angular_velocity -= ROTATION_SPEED  # Utilisation de la variable depuis settings.py
        if keys[pygame.K_RIGHT]:
            self.angular_velocity += ROTATION_SPEED
        return throttle_inputs

    def initialize_thrusters(self):
        self.main_thruster = Thruster("Principal", (0, 40), THRUSTER_FORCE_MAIN, 0)  # Propulseur arrière
        self.reverse_thruster = Thruster("Arrière", (0, -40), THRUSTER_FORCE_REVERSE, 180)  # Propulseur avant
        self.left_thruster = Thruster("Gauche", (-20, 0), THRUSTER_FORCE_LATERAL, 90)  # Propulseur gauche
        self.right_thruster = Thruster("Droite", (20, 0), THRUSTER_FORCE_LATERAL, -90)  # Propulseur droit
        self.add_thruster(self.main_thruster)
        self.add_thruster(self.reverse_thruster)
        self.add_thruster(self.left_thruster)
        self.add_thruster(self.right_thruster)
