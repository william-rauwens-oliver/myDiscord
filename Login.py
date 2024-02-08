import pygame
import mysql.connector
import os

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="willy",
    database="discord"
)
cursor = db.cursor()

pygame.init()

BACKGROUND_COLOR = (54, 57, 63)
TEXT_COLOR = (255, 255, 255)
INPUT_BOX_COLOR = (44, 47, 51)
INPUT_BOX_BORDER_COLOR = (35, 39, 42)
INPUT_TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (114, 137, 218)
BUTTON_HOVER_COLOR = (103, 123, 196)


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connexion et Inscription")

font = pygame.font.Font(None, 24)
input_font = pygame.font.Font(None, 20)

discord_logo = pygame.image.load('Data/Logo Discord.png')
discord_logo = pygame.transform.scale(discord_logo, (150, 150))