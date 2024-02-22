import os
import pygame
import pygame_gui

pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (220, 220, 220)

# Taille
largeur_fenetre, hauteur_fenetre = 1283, 762

# La fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Discord Interface")


# Boucle principale
en_cours = True
horloge = pygame.time.Clock()
while en_cours:
    temps_passe = horloge.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False


    fenetre.fill(GRIS_CLAIR)

 

    pygame.display.flip()

pygame.quit()