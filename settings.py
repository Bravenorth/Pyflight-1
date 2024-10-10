# settings.py

import pygame

# Configuration de la fenêtre
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
WINDOW_TITLE = "Simulation de Vaisseau"

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
THRUSTER_ACTIVE_COLOR = (255, 0, 0)    # Rouge
THRUSTER_INACTIVE_COLOR = (0, 255, 0)  # Vert

# Police pour l'affichage du texte
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 18)

# Paramètres du vaisseau et des propulseurs
SHIP_MASS = 800
LINEAR_DAMPING = 0.02
THRUSTER_FORCE_MAIN = 15000
THRUSTER_FORCE_REVERSE = 7500
THRUSTER_FORCE_LATERAL = 5000
THRUSTER_FORCE_ROTATION = 3000  # Force des propulseurs de rotation

# Paramètres du laser
LASER_SPEED = 500  # Vitesse du laser en unités par seconde
LASER_LIFETIME = 2  # Durée de vie du laser en secondes

# Paramètres de la carte
MAP_WIDTH, MAP_HEIGHT = 5000, 5000

# Autres paramètres
FRAME_RATE = 60
