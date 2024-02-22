import os
import pygame
import pygame_gui



pygame.init()

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (220, 220, 220)

# Taille
largeur_fenetre, hauteur_fenetre = 1283, 762

# La fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Messages Discord")

moitie_largeur = largeur_fenetre // 2
epaisseur_ligne = 2

# Ajustement pour la partie gauche
largeur_partie_gauche = moitie_largeur - 40  
partie_gauche = pygame.Rect(0, 20, largeur_partie_gauche, hauteur_fenetre)
partie_droite = pygame.Rect(moitie_largeur, 0, moitie_largeur, hauteur_fenetre)

ligne_x = moitie_largeur

gestionnaire = pygame_gui.UIManager((largeur_fenetre, hauteur_fenetre))

# Boutons ronds
rayon_bouton = 20
espacement_bouton = 10
nombre_boutons = 7
decalage_x = 80
decalage_y = 20



boutons = []
for i in range(nombre_boutons):
    bouton_rect = pygame.Rect(decalage_x, decalage_y + i * (2 * rayon_bouton + espacement_bouton), 2 * rayon_bouton, 2 * rayon_bouton)
    bouton = pygame_gui.elements.UIButton(relative_rect=bouton_rect, text=str(i+1), manager=gestionnaire)
    boutons.append(bouton)

# Boucle principale
en_cours = True
horloge = pygame.time.Clock()
while en_cours:
    temps_passe = horloge.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

        gestionnaire.process_events(event)

    fenetre.fill(GRIS_CLAIR)

    # Dessiner la ligne de séparation
    pygame.draw.rect(fenetre, NOIR,(0,0,200,380),border_radius=50)

    gestionnaire.update(temps_passe)
    gestionnaire.draw_ui(fenetre)

    pygame.display.flip()

pygame.quit()