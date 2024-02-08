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

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_input_box(surface, x, y, width, height, text, font, text_input):
    input_box = pygame.Rect(0, 0, width, height)
    input_box.center = (x, y)
    pygame.draw.rect(surface, INPUT_BOX_COLOR, input_box)
    pygame.draw.rect(surface, INPUT_BOX_BORDER_COLOR, input_box, 2)
    
    if text_input == "":
        default_text = font.render("Entrez votre " + text.lower(), True, (128, 128, 128))
        surface.blit(default_text, default_text.get_rect(center=input_box.center))
    else:
        text_surface = font.render(text_input, True, INPUT_TEXT_COLOR)
        surface.blit(text_surface, text_surface.get_rect(center=input_box.center))
    
    return input_box

def draw_button(surface, x, y, width, height, text, font, color, hover_color):
    button_rect = pygame.Rect(0, 0, width, height)
    button_rect.center = (x, y)
    pygame.draw.rect(surface, color, button_rect)
    pygame.draw.rect(surface, INPUT_BOX_BORDER_COLOR, button_rect, 2)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, button_rect, 2)

def check_login(email, password):
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()
    return result is not None
