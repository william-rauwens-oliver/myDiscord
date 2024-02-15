import pygame
from Login import Login
from SignUp import SignUp

class Main:
    def __init__(self):
        pygame.init()  # Initialisation de pygame en premier

        self.WIDTH, self.HEIGHT = 800, 600  
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Choix de l'action")

        # Assurez-vous que pygame est initialisé avant d'initialiser la police
        self.font = pygame.font.Font(None, 36)  

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)  
        surface.blit(textobj, textrect)

    def main(self):
        clock = pygame.time.Clock()
        running = True

        login_window_closed = False  # Ajout d'un indicateur pour savoir si la fenêtre de connexion est fermée

        while running:
            self.screen.fill((30, 30, 30))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 300 <= event.pos[0] <= 500 and 250 <= event.pos[1] <= 300:
                        login = Login()
                        login.main()
                        login_window_closed = True
                    elif 300 <= event.pos[0] <= 500 and 350 <= event.pos[1] <= 400:
                        signup = SignUp()
                        signup.main()

            center_x = self.WIDTH // 2
            center_y = self.HEIGHT // 2

            self.draw_text("Se connecter", self.font, (255, 255, 255), self.screen, center_x, center_y)
            self.draw_text("S'inscrire", self.font, (255, 255, 255), self.screen, center_x, center_y + 100)

            if login_window_closed:
                running = False

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    main_app = Main()
    main_app.main()