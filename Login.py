import pygame
import subprocess
from DataBase import Database
from LogOut import Logout

class UIComponent:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 24)
        self.input_font = pygame.font.Font(None, 20)
        self.BUTTON_COLOR = (114, 137, 218)
        self.BUTTON_HOVER_COLOR = (103, 123, 196)
        self.BACKGROUND_COLOR = (54, 57, 63)
        self.TEXT_COLOR = (255, 255, 255)
        self.INPUT_BOX_COLOR = (44, 47, 51)
        self.INPUT_BOX_BORDER_COLOR = (35, 39, 42)
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Connexion et Inscription")
        self.discord_logo = pygame.image.load('Data/Logo Discord.png')
        self.discord_logo = pygame.transform.scale(self.discord_logo, (150, 150))

    def draw_text(self, text, x, y):
        textobj = self.font.render(text, True, self.TEXT_COLOR)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        self.screen.blit(textobj, textrect)

    def draw_input_box(self, x, y, width, height, text, text_input, border_radius=0):
        input_box = pygame.Rect(0, 0, width, height)
        input_box.center = (x, y)
        pygame.draw.rect(self.screen, self.INPUT_BOX_COLOR, input_box, border_radius=border_radius)
        pygame.draw.rect(self.screen, self.INPUT_BOX_BORDER_COLOR, input_box, 2, border_radius=border_radius)

        if text_input == "":
            default_text = self.font.render("Entrez votre " + text.lower(), True, (128, 128, 128))
            self.screen.blit(default_text, default_text.get_rect(center=input_box.center))
        else:
            text_surface = self.input_font.render(text_input, True, self.TEXT_COLOR)
            self.screen.blit(text_surface, text_surface.get_rect(center=input_box.center))

        return input_box

    def draw_button(self, x, y, width, height, text, border_radius=0):
        button_rect = pygame.Rect(0, 0, width, height)
        button_rect.center = (x, y)
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, button_rect, border_radius=border_radius)
        pygame.draw.rect(self.screen, self.INPUT_BOX_BORDER_COLOR, button_rect, 2, border_radius=border_radius)
        text_surface = self.font.render(text, True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.BUTTON_HOVER_COLOR, button_rect, 2, border_radius=border_radius)

class Login(UIComponent):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.logout_screen = Logout()

    def check_login(self, email, password):
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        return self.db.check_login(email, password)

    def get_logged_in_user_email(self):
        query = "SELECT email FROM users LIMIT 1"
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def main(self):
        clock = pygame.time.Clock()

        running = True
        logged_in = False
        email_input = ""
        password_input = ""
        error_message = ""

        while running:
            self.screen.fill(self.BACKGROUND_COLOR)
            self.screen.blit(self.discord_logo, (325, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if not logged_in:
                        if event.key == pygame.K_BACKSPACE:
                            if email_input_box.collidepoint(pygame.mouse.get_pos()):
                                email_input = email_input[:-1]
                            elif password_input_box.collidepoint(pygame.mouse.get_pos()):
                                password_input = password_input[:-1]
                        elif len(email_input) < 50 and email_input_box.collidepoint(pygame.mouse.get_pos()):
                            email_input += event.unicode
                        elif len(password_input) < 20 and password_input_box.collidepoint(pygame.mouse.get_pos()):
                            password_input += event.unicode

            if not logged_in:
                email_input_box = self.draw_input_box(400, 300, 300, 40, "Email", email_input, border_radius=20)
                password_input_box = self.draw_input_box(400, 370, 300, 40, "Mot de passe", password_input, border_radius=20)
                self.draw_button(400, 450, 200, 50, "Se connecter", border_radius=20)
                mouse_pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if 350 < mouse_pos[0] < 550 and 450 < mouse_pos[1] < 500:
                        if email_input.strip() == "" or password_input.strip() == "":
                            error_message = "Veuillez entrer une adresse e-mail et un mot de passe."
                        elif self.check_login(email_input, password_input):
                            logged_in = True
                            error_message = ""
                            print("Connexion réussie!")
                            subprocess.run(["python", "Menu.py"])
                        else:
                            error_message = "Email ou mot de passe incorrect."
            else:
                self.draw_text("Bienvenue sur Discord!", self.WIDTH / 2, self.HEIGHT / 2)
                self.draw_button(self.WIDTH / 2, self.HEIGHT / 2 + 100, 120, 40, "Déconnexion", border_radius=20)
                mouse_pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if self.WIDTH / 2 - 60 < mouse_pos[0] < self.WIDTH / 2 + 60 and self.HEIGHT / 2 + 80 < mouse_pos[1] < self.HEIGHT / 2 + 120:
                        self.logout_screen.main()
                        logged_in = False
            self.draw_text(error_message, 400, 500)

            if pygame.display.get_init():
                pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    login = Login()
    login.main()