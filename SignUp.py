import pygame
import os
from DataBase import Database

class SignUp:
    def __init__(self):
        self.db = Database()
        pygame.init()
        self.BACKGROUND_COLOR = (54, 57, 63)
        self.TEXT_COLOR = (255, 255, 255)
        self.INPUT_BOX_COLOR = (44, 47, 51)
        self.INPUT_BOX_BORDER_COLOR = (35, 39, 42)
        self.INPUT_TEXT_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (114, 137, 218)
        self.BUTTON_HOVER_COLOR = (103, 123, 196)
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Connexion et Inscription")
        self.font = pygame.font.Font(None, 24)
        self.input_font = pygame.font.Font(None, 20)
        self.discord_logo = pygame.image.load('Data/Logo Discord.png')
        self.discord_logo = pygame.transform.scale(self.discord_logo, (150, 150))

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def draw_input_box(self, surface, x, y, width, height, text, font, text_input):
        input_box = pygame.Rect(0, 0, width, height)
        input_box.center = (x, y)
        pygame.draw.rect(surface, self.INPUT_BOX_COLOR, input_box)
        pygame.draw.rect(surface, self.INPUT_BOX_BORDER_COLOR, input_box, 2)

        if text_input == "":
            default_text = font.render("Entrez votre " + text.lower(), True, (128, 128, 128))
            surface.blit(default_text, default_text.get_rect(center=input_box.center))
        else:
            text_surface = font.render(text_input, True, self.INPUT_TEXT_COLOR)
            surface.blit(text_surface, text_surface.get_rect(center=input_box.center))
        
        return input_box

    def draw_button(self, surface, x, y, width, height, text, font, color, hover_color):
        button_rect = pygame.Rect(0, 0, width, height)
        button_rect.center = (x, y)
        pygame.draw.rect(surface, color, button_rect)
        pygame.draw.rect(surface, self.INPUT_BOX_BORDER_COLOR, button_rect, 2)
        text_surface = font.render(text, True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, hover_color, button_rect, 2)

    def main(self):
        clock = pygame.time.Clock()

        running = True
        logged_in = False

        name_input = ""
        first_name_input = ""
        email_input = ""
        password_input = ""

        while running:
            self.screen.fill(self.BACKGROUND_COLOR)
            self.screen.blit(self.discord_logo, (325, 50))

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

                name_input_box = self.draw_input_box(self.screen, 400, 250, 300, 40, "Nom", self.input_font, name_input)
                first_name_input_box = self.draw_input_box(self.screen, 400, 310, 300, 40, "Prénom", self.input_font, first_name_input)
                email_input_box = self.draw_input_box(self.screen, 400, 370, 300, 40, "Email", self.input_font, email_input)
                password_input_box = self.draw_input_box(self.screen, 400, 430, 300, 40, "Mot de passe", self.input_font, password_input)

                self.draw_button(self.screen, 400, 500, 200, 50, "S'inscrire", self.font, self.BUTTON_COLOR, self.BUTTON_HOVER_COLOR)
                mouse_pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if 350 < mouse_pos[0] < 550 and 500 < mouse_pos[1] < 550:
                        self.db.insert_user(name_input, first_name_input, email_input, password_input)
                        logged_in = True
                        os.system("python MainMessages.py")

            else:
                self.draw_text("Bienvenue sur Discord!", self.font, self.TEXT_COLOR, self.screen, 50, 50)
                self.draw_button(self.screen, 10, 10, 120, 40, "Déconnexion", self.font, self.BUTTON_COLOR, self.BUTTON_HOVER_COLOR)
                mouse_pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if 10 < mouse_pos[0] < 130 and 10 < mouse_pos[1] < 50:
                        logged_in = False

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    inscription = SignUp()
    inscription.main()
