# game/ship.py

import pygame
from settings import *
from .thruster import Thruster
from .laser import Laser
from .ship_part import ShipPart

class Ship:
    def __init__(self, x, y):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.mass = SHIP_MASS
        self.linear_damping = LINEAR_DAMPING
        self.thrusters = []
        self.parts = []  # Liste des parties du vaisseau
        self.active_thrusters = set()
        self.angle = 0  # Angle du vaisseau en degrés
        self.angular_velocity = 0  # Vitesse angulaire en degrés par seconde
        self.angular_damping = 0.05  # Facteur d'amortissement angulaire
        self.moment_of_inertia = 5000  # Moment d'inertie du vaisseau

        # Variables pour la gestion du tir
        self.laser_cooldown = 0.2  # Temps entre les tirs en secondes
        self.laser_timer = 0  # Timer pour le tir du laser

        self.initialize_parts()
        self.initialize_thrusters()

    def add_thruster(self, thruster):
        self.thrusters.append(thruster)

    def add_part(self, part):
        self.parts.append(part)

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

        # Mettre à jour le timer du laser
        if self.laser_timer > 0:
            self.laser_timer -= dt

    def draw(self, surface, camera_offset):
        # Dessiner les parties du vaisseau
        for part in self.parts:
            part.draw(surface, self.position - camera_offset, self.angle)

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
        # Activer les propulseurs de rotation
        if keys[pygame.K_LEFT]:
            throttle_inputs.append((self.rotation_left_thruster1, 1.0))
            throttle_inputs.append((self.rotation_left_thruster2, 1.0))
        if keys[pygame.K_RIGHT]:
            throttle_inputs.append((self.rotation_right_thruster1, 1.0))
            throttle_inputs.append((self.rotation_right_thruster2, 1.0))
        return throttle_inputs

    def fire_laser(self):
        if self.laser_timer <= 0:
            self.laser_timer = self.laser_cooldown
            # Créer un nouveau laser à la position et à l'angle du vaisseau
            return Laser(self.position, self.angle)
        else:
            return None

    def initialize_parts(self):
        # Coque du vaisseau
        hull_shape = [
            pygame.math.Vector2(0, -40),   # Pointe avant
            pygame.math.Vector2(-20, 40),  # Coin arrière gauche
            pygame.math.Vector2(20, 40)    # Coin arrière droit
        ]
        hull = ShipPart("Coque", (0, 0), shape=hull_shape, color=WHITE)
        self.add_part(hull)

        # Cockpit du vaisseau
        cockpit_shape = [
            pygame.math.Vector2(-10, -20),
            pygame.math.Vector2(-10, -10),
            pygame.math.Vector2(10, -10),
            pygame.math.Vector2(10, -20)
        ]
        cockpit = ShipPart("Cockpit", (0, 0), shape=cockpit_shape, color=(0, 255, 255))
        self.add_part(cockpit)

        # Réacteurs du vaisseau (déjà inclus via les thrusters)

    def initialize_thrusters(self):
        # Création des ShipParts pour les thrusters
        thruster_size = (10, 20)
        thruster_color = (255, 165, 0)  # Orange

        # Propulseur principal (arrière)
        main_thruster_part = ShipPart(
            "Thruster Principal",
            (0, 40),
            shape=[
                pygame.math.Vector2(-5, 0),
                pygame.math.Vector2(5, 0),
                pygame.math.Vector2(5, -20),
                pygame.math.Vector2(-5, -20)
            ],
            color=thruster_color
        )
        self.add_part(main_thruster_part)

        # Propulseur arrière (avant)
        reverse_thruster_part = ShipPart(
            "Thruster Arrière",
            (0, -40),
            shape=[
                pygame.math.Vector2(-5, 0),
                pygame.math.Vector2(5, 0),
                pygame.math.Vector2(5, 20),
                pygame.math.Vector2(-5, 20)
            ],
            color=thruster_color
        )
        self.add_part(reverse_thruster_part)

        # Propulseur gauche (latéral)
        left_thruster_part = ShipPart(
            "Thruster Gauche",
            (-20, 0),
            shape=[
                pygame.math.Vector2(0, -5),
                pygame.math.Vector2(0, 5),
                pygame.math.Vector2(20, 5),
                pygame.math.Vector2(20, -5)
            ],
            color=thruster_color
        )
        self.add_part(left_thruster_part)

        # Propulseur droit (latéral)
        right_thruster_part = ShipPart(
            "Thruster Droit",
            (20, 0),
            shape=[
                pygame.math.Vector2(0, -5),
                pygame.math.Vector2(0, 5),
                pygame.math.Vector2(-20, 5),
                pygame.math.Vector2(-20, -5)
            ],
            color=thruster_color
        )
        self.add_part(right_thruster_part)

        # Propulseurs de rotation
        rotation_thruster_shape = [
            pygame.math.Vector2(-5, -5),
            pygame.math.Vector2(5, -5),
            pygame.math.Vector2(5, 5),
            pygame.math.Vector2(-5, 5)
        ]

        rotation_left_thruster_part1 = ShipPart(
            "Rotation Gauche Thruster 1",
            (20, -40),
            shape=rotation_thruster_shape,
            color=thruster_color
        )
        rotation_left_thruster_part2 = ShipPart(
            "Rotation Gauche Thruster 2",
            (-20, 40),
            shape=rotation_thruster_shape,
            color=thruster_color
        )
        self.add_part(rotation_left_thruster_part1)
        self.add_part(rotation_left_thruster_part2)

        rotation_right_thruster_part1 = ShipPart(
            "Rotation Droite Thruster 1",
            (-20, -40),
            shape=rotation_thruster_shape,
            color=thruster_color
        )
        rotation_right_thruster_part2 = ShipPart(
            "Rotation Droite Thruster 2",
            (20, 40),
            shape=rotation_thruster_shape,
            color=thruster_color
        )
        self.add_part(rotation_right_thruster_part1)
        self.add_part(rotation_right_thruster_part2)

        # Création des Thrusters en les associant avec leurs ShipParts
        self.main_thruster = Thruster("Principal", (0, 40), THRUSTER_FORCE_MAIN, 0, ship_part=main_thruster_part)
        self.reverse_thruster = Thruster("Arrière", (0, -40), THRUSTER_FORCE_REVERSE, 180, ship_part=reverse_thruster_part)
        self.left_thruster = Thruster("Gauche", (-20, 0), THRUSTER_FORCE_LATERAL, 90, ship_part=left_thruster_part)
        self.right_thruster = Thruster("Droite", (20, 0), THRUSTER_FORCE_LATERAL, -90, ship_part=right_thruster_part)

        self.rotation_left_thruster1 = Thruster(
            "Rotation Gauche 1", (20, -40), THRUSTER_FORCE_ROTATION, -90, ship_part=rotation_left_thruster_part1)
        self.rotation_left_thruster2 = Thruster(
            "Rotation Gauche 2", (-20, 40), THRUSTER_FORCE_ROTATION, 90, ship_part=rotation_left_thruster_part2)

        self.rotation_right_thruster1 = Thruster(
            "Rotation Droite 1", (-20, -40), THRUSTER_FORCE_ROTATION, 90, ship_part=rotation_right_thruster_part1)
        self.rotation_right_thruster2 = Thruster(
            "Rotation Droite 2", (20, 40), THRUSTER_FORCE_ROTATION, -90, ship_part=rotation_right_thruster_part2)

        # Ajouter tous les thrusters à la liste
        self.add_thruster(self.main_thruster)
        self.add_thruster(self.reverse_thruster)
        self.add_thruster(self.left_thruster)
        self.add_thruster(self.right_thruster)
        self.add_thruster(self.rotation_left_thruster1)
        self.add_thruster(self.rotation_left_thruster2)
        self.add_thruster(self.rotation_right_thruster1)
        self.add_thruster(self.rotation_right_thruster2)
