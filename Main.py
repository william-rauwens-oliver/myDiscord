import pygame
from Login import Login
from SignUp import SignUp

class Main:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 400, 200
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Choix de l'action")
        self.font = pygame.font.Font(None, 24)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
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
                    if 50 <= event.pos[0] <= 150 and 80 <= event.pos[1] <= 120:
                        login = Login()
                        login.main()
                    elif 250 <= event.pos[0] <= 350 and 80 <= event.pos[1] <= 120:
                        signup = SignUp()
                        signup.main()

            self.draw_text("Se connecter", self.font, (255, 255, 255), self.screen, 50, 80)
            self.draw_text("S'inscrire", self.font, (255, 255, 255), self.screen, 250, 80)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    main_app = Main()
    main_app.main()