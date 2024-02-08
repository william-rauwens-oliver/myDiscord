import pygame
import mysql.connector
import os

# Connexion à la base de données
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="willy",
    database="discord"
)
cursor = db.cursor()

# Initialisation de Pygame
pygame.init()

# Définition des couleurs Discord
BACKGROUND_COLOR = (54, 57, 63)
TEXT_COLOR = (255, 255, 255)
INPUT_BOX_COLOR = (44, 47, 51)  # Couleur de fond des champs de texte
INPUT_BOX_BORDER_COLOR = (35, 39, 42)  # Couleur de la bordure des champs de texte
INPUT_TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (114, 137, 218)
BUTTON_HOVER_COLOR = (103, 123, 196)

# Définition de la taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connexion et Inscription")

# Police de caractères
font = pygame.font.Font(None, 24)
input_font = pygame.font.Font(None, 20)

# Chargement d'images Discord
discord_logo = pygame.image.load('Data/Logo Discord.png')
discord_logo = pygame.transform.scale(discord_logo, (150, 150))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
