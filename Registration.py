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

def insert_user(name, first_name, email, password):
    query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, first_name, email, password))
    db.commit()

def main():
    clock = pygame.time.Clock()

    running = True
    logged_in = False

    name_input = ""
    first_name_input = ""
    email_input = ""
    password_input = ""

    while running:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(discord_logo, (325, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not logged_in:
                    if event.key == pygame.K_BACKSPACE:
                        if name_input_box.collidepoint(pygame.mouse.get_pos()):
                            name_input = name_input[:-1]
                        elif first_name_input_box.collidepoint(pygame.mouse.get_pos()):
                            first_name_input = first_name_input[:-1]
                        elif email_input_box.collidepoint(pygame.mouse.get_pos()):
                            email_input = email_input[:-1]
                        elif password_input_box.collidepoint(pygame.mouse.get_pos()):
                            password_input = password_input[:-1]
                    elif len(name_input) < 30 and name_input_box.collidepoint(pygame.mouse.get_pos()):
                        name_input += event.unicode
                    elif len(first_name_input) < 30 and first_name_input_box.collidepoint(pygame.mouse.get_pos()):
                        first_name_input += event.unicode
                    elif len(email_input) < 50 and email_input_box.collidepoint(pygame.mouse.get_pos()):
                        email_input += event.unicode
                    elif len(password_input) < 20 and password_input_box.collidepoint(pygame.mouse.get_pos()):
                        password_input += event.unicode

        if not logged_in:

            name_input_box = draw_input_box(screen, 400, 250, 300, 40, "Nom", input_font, name_input)
            first_name_input_box = draw_input_box(screen, 400, 310, 300, 40, "Prénom", input_font, first_name_input)
            email_input_box = draw_input_box(screen, 400, 370, 300, 40, "Email", input_font, email_input)
            password_input_box = draw_input_box(screen, 400, 430, 300, 40, "Mot de passe", input_font, password_input)

            draw_button(screen, 400, 500, 200, 50, "S'inscrire", font, BUTTON_COLOR, BUTTON_HOVER_COLOR)
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if 350 < mouse_pos[0] < 550 and 500 < mouse_pos[1] < 550:
                    insert_user(name_input, first_name_input, email_input, password_input)
                    logged_in = True
                    os.system("python MainMessages.py")

        else:
            draw_text("Bienvenue sur Discord!", font, TEXT_COLOR, screen, 50, 50)
            draw_button(screen, 10, 10, 120, 40, "Déconnexion", font, BUTTON_COLOR, BUTTON_HOVER_COLOR)
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if 10 < mouse_pos[0] < 130 and 10 < mouse_pos[1] < 50:
                    logged_in = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()