# settings.py

import pygame

# Configuration de la fenêtre
WIDTH, HEIGHT = 1024, 768
WINDOW_SIZE = (WIDTH, HEIGHT)
WINDOW_TITLE = "Simulation de Vaisseau"

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
THRUSTER_ACTIVE_COLOR = (255, 0, 0)   # Rouge
THRUSTER_INACTIVE_COLOR = (0, 255, 0) # Vert

# Police pour l'affichage du texte
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 18)

# Paramètres du vaisseau et des propulseurs
SHIP_MASS = 800
LINEAR_DAMPING = 0.02
THRUSTER_FORCE_MAIN = 10000
THRUSTER_FORCE_REVERSE = 2500
THRUSTER_FORCE_LATERAL = 2500

# Vitesse de rotation (nouvelle variable)
ROTATION_SPEED = 2  # Vitesse de rotation manuelle en degrés par seconde

# Paramètres de la carte
MAP_WIDTH, MAP_HEIGHT = 5000, 5000

# Autres paramètres
FRAME_RATE = 60
