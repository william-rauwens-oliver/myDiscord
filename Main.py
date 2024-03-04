import pygame
from Login import Login
from SignUp import SignUp

class Main:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Choix de l'action")
        self.font_title = pygame.font.Font(None, 60) 
        self.font = pygame.font.Font(None, 36)
        self.login_window_closed = False 
        self.previous_window = None

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)  
        surface.blit(textobj, textrect)

    def draw_button(self, surface, x, y, width, height, text, font, color, hover_color, border_radius=10, action=None, *args):
        button_rect = pygame.Rect(0, 0, width, height)
        button_rect.center = (x, y)
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, hover_color, button_rect, border_radius=border_radius)
            if clicked and action:
                action(*args)
        else:
            pygame.draw.rect(surface, color, button_rect, border_radius=border_radius)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)

    def login_action(self):
        self.previous_window = "Main"
        login = Login()
        result = login.main()
        if result == "main":
            self.back_to_main()
        self.login_window_closed = True

    def signup_action(self):
        self.previous_window = "Main"
        signup = SignUp()
        result = signup.main()
        if result == "main": 
            self.back_to_main()
        self.login_window_closed = True

    def check_windows_closed(self):
        return self.login_window_closed

    def main(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill((54, 57, 63))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            title_text = "Bienvenue"
            title_render = self.font_title.render(title_text, True, (255, 255, 255))
            title_rect = title_render.get_rect(center=(self.WIDTH // 2, 100))
            self.screen.blit(title_render, title_rect)

            self.draw_button(self.screen, 400, 275, 200, 50, "Se connecter", self.font, (114, 137, 218), (103, 123, 196), border_radius=20, action=self.login_action)
            self.draw_button(self.screen, 400, 375, 200, 50, "S'inscrire", self.font, (114, 137, 218), (103, 123, 196), border_radius=20, action=self.signup_action)
            if self.check_windows_closed():
                running = False 
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
    def back_to_main(self):
        if self.previous_window == "Main":
            self.login_window_closed = False

if __name__ == "__main__":
    main_app = Main()
    main_app.main()