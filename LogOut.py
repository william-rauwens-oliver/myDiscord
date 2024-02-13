import pygame

class Logout:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Déconnexion")

        self.font = pygame.font.Font(None, 24)
        self.BUTTON_COLOR = (114, 137, 218)
        self.BUTTON_HOVER_COLOR = (103, 123, 196)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def draw_button(self, surface, x, y, width, height, text, font, color, hover_color):
        button_rect = pygame.Rect(0, 0, width, height)
        button_rect.center = (x, y)
        pygame.draw.rect(surface, color, button_rect)
        pygame.draw.rect(surface, (35, 39, 42), button_rect, 2)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, hover_color, button_rect, 2)

    def main(self):
        clock = pygame.time.Clock()

        running = True

        while running:
            self.screen.fill((54, 57, 63))

            self.draw_text("Êtes-vous sûr de vouloir vous déconnecter ?", self.font, (255, 255, 255), self.screen, self.WIDTH // 2, self.HEIGHT // 3)

            self.draw_button(self.screen, self.WIDTH // 2, self.HEIGHT // 2, 200, 50, "Déconnexion", self.font, self.BUTTON_COLOR, self.BUTTON_HOVER_COLOR)
            self.draw_button(self.screen, self.WIDTH // 2, self.HEIGHT // 2 + 70, 200, 50, "Annuler", self.font, self.BUTTON_COLOR, self.BUTTON_HOVER_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if 300 < mouse_pos[0] < 500 and 250 < mouse_pos[1] < 300:
                            print("Déconnexion...")
                            running = False  # Quitte la boucle de déconnexion

            if pygame.display.get_init():
                pygame.display.flip()

            clock.tick(60)

if __name__ == "__main__":
    logout = Logout()
    logout.main()
    pygame.quit()