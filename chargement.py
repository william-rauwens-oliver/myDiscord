import pygame
import os
import pygame_gui


pygame.init()

# Fenêtre
largeur_fenetre, hauteur_fenetre = 800, 800
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))

gestionnaire = pygame_gui.UIManager((largeur_fenetre, hauteur_fenetre))

# pygame_gui
gestionnaire = pygame_gui.UIManager((largeur_fenetre, hauteur_fenetre))

pygame.quit()

