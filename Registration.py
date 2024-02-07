import pygame
import mysql.connector

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
INPUT_BOX_COLOR = (64, 68, 75)
INPUT_TEXT_COLOR = (188, 190, 196)
BUTTON_COLOR = (114, 137, 218)
BUTTON_HOVER_COLOR = (103, 123, 196)

# Définition de la taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connexion et Inscription")

# Police de caractères
font = pygame.font.Font("font/Roboto-Regular.ttf", 20)
input_font = pygame.font.Font("font/Roboto-Regular.ttf", 16)

# Fonction pour afficher du texte sur l'écran
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Fonction pour afficher les champs de texte
def draw_input_box(surface, x, y, width, height, text, font, text_input):
    input_box = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, INPUT_BOX_COLOR, input_box)
    pygame.draw.rect(surface, TEXT_COLOR, input_box, 2)
    draw_text(text, font, TEXT_COLOR, surface, x + 5, y - 20)
    text_surface = font.render(text_input, True, INPUT_TEXT_COLOR)
    surface.blit(text_surface, (x + 5, y + 5))
    return input_box

# Fonction pour dessiner un bouton
def draw_button(surface, x, y, width, height, text, font, color, hover_color):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, button_rect)
    pygame.draw.rect(surface, TEXT_COLOR, button_rect, 2)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, button_rect, 2)

# Fonction pour vérifier les informations de connexion dans la base de données
def check_login(email, password):
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()
    return result is not None

# Fonction pour insérer un nouvel utilisateur dans la base de données
def insert_user(name, first_name, email, password):
    query = "INSERT INTO users (nom, prenom, email, password) VALUES (%s, %s, %s, %s)"  # Modifier le nom des colonnes si nécessaire
    cursor.execute(query, (name, first_name, email, password))
    db.commit()

# Fonction principale
def main():
    clock = pygame.time.Clock()

    running = True
    logged_in = False

    # Initialisation des champs de texte
    name_input = ""
    first_name_input = ""
    email_input = ""
    password_input = ""

    while running:
        screen.fill(BACKGROUND_COLOR)

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

        # Affichage des champs de texte pour la connexion ou l'inscription
        if not logged_in:
            # Affichage des champs pour le nom, le prénom, l'email et le mot de passe
            name_input_box = draw_input_box(screen, 300, 200, 200, 30, "Nom:", input_font, name_input)
            first_name_input_box = draw_input_box(screen, 300, 250, 200, 30, "Prénom:", input_font, first_name_input)
            email_input_box = draw_input_box(screen, 300, 300, 200, 30, "Email:", input_font, email_input)
            password_input_box = draw_input_box(screen, 300, 350, 200, 30, "Mot de passe:", input_font, password_input)

            # Affichage du bouton pour l'inscription
            draw_button(screen, 330, 400, 150, 50, "Inscription", font, BUTTON_COLOR, BUTTON_HOVER_COLOR)

            # Gestion des interactions avec le bouton d'inscription
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if 330 < mouse_pos[0] < 480 and 400 < mouse_pos[1] < 450:
                    # Insertion des informations dans la base de données
                    insert_user(name_input, first_name_input, email_input, password_input)
                    logged_in = True

        # Affichage de l'écran principal après connexion
        else:
            # Affichage du message principal
            draw_text("Bienvenue sur Discord!", font, TEXT_COLOR, screen, 50, 50)

            # Bouton de déconnexion
            draw_button(screen, 10, 10, 120, 40, "Déconnexion", font, BUTTON_COLOR, BUTTON_HOVER_COLOR)

            # Gestion des interactions avec le bouton de déconnexion
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if 10 < mouse_pos[0] < 130 and 10 < mouse_pos[1] < 50:
                    logged_in = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
