import pygame

class Logout:
    def __init__(self):
        pygame.init()

        self.BACKGROUND_COLOR = (54, 57, 63)
        self.TEXT_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (114, 137, 218)
        self.BUTTON_HOVER_COLOR = (103, 123, 196)
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Déconnexion")

        self.font = pygame.font.Font(None, 24)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def draw_button(self, surface, x, y, width, height, text, font, color, hover_color):
        button_rect = pygame.Rect(0, 0, width, height)
        button_rect.center = (x, y)
        pygame.draw.rect(surface, color, button_rect)
        pygame.draw.rect(surface, self.TEXT_COLOR, button_rect, 2)
        text_surface = font.render(text, True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, hover_color, button_rect, 2)

    def main(self):
        clock = pygame.time.Clock()

        running = True

        while running:
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_text("Êtes-vous sûr de vouloir vous déconnecter ?", self.font, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 3)

            self.draw_button(self.screen, self.WIDTH // 2, self.HEIGHT // 2, 200, 50, "Oui", self.font, self.BUTTON_COLOR, self.BUTTON_HOVER_COLOR)
            self.draw_button(self.screen, self.WIDTH // 2, self.HEIGHT // 2 + 70, 200, 50, "Non", self.font, self.BUTTON_COLOR, self.BUTTON_HOVER_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 300 < mouse_pos[0] < 500 and 250 < mouse_pos[1] < 300:
                        print("Déconnexion en cours...")
                        # Code pour la déconnexion ici
                        running = False
                    elif 300 < mouse_pos[0] < 500 and 320 < mouse_pos[1] < 370:
                        print("Déconnexion annulée.")
                        running = False

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    logout = Logout()
    logout.main()
