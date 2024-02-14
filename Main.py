import pygame
from Login import Login
from SignUp import SignUp

class Main:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 800, 600  # Modification de la taille de la fenêtre
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Choix de l'action")
        self.font = pygame.font.Font(None, 36)  # Ajustement de la taille de la police

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)  # Centrer le texte
        surface.blit(textobj, textrect)

    def main(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill((30, 30, 30))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 300 <= event.pos[0] <= 500 and 400 <= event.pos[1] <= 450:
                        login = Login()
                        login.main()
                    elif 300 <= event.pos[0] <= 500 and 500 <= event.pos[1] <= 550:
                        signup = SignUp()
                        signup.main()

            # Ajuster les positions des textes
            self.draw_text("Se connecter", self.font, (255, 255, 255), self.screen, self.WIDTH // 2, 450)
            self.draw_text("S'inscrire", self.font, (255, 255, 255), self.screen, self.WIDTH // 2, 550)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    main_app = Main()
    main_app.main()