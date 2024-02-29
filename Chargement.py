import pygame
import pygame_gui

pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (220, 220, 220)
BLEU = (114, 137, 218)

# Taille
largeur_fenetre, hauteur_fenetre = 1283, 762

# La fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Discord Interface")


manager = pygame_gui.UIManager((largeur_fenetre, hauteur_fenetre))


utilisateurs = ['Kenny', 'Willy', 'Max']

# Boutons ronds
rayon_bouton = 33
espacement_bouton = 10
nombre_boutons = len(utilisateurs)
decalage_x = 80
decalage_y = 20

boutons = []


for i, utilisateur in enumerate(utilisateurs):
    bouton_rect = pygame.Rect(decalage_x, decalage_y + i * (2 * rayon_bouton + espacement_bouton), 2 * rayon_bouton, 2 * rayon_bouton)
    bouton = pygame_gui.elements.UIButton(relative_rect=bouton_rect, text=utilisateur)
    boutons.append((bouton, utilisateur))  # Ajout de l'utilisateur associé à chaque bouton

# Liste des messages
messages = []

# Police 
police = pygame.font.Font(None, 24)


COULEUR_MESSAGE_LOCAL = BLEU
COULEUR_MESSAGE_DISTANT = NOIR
utilisateur_selectionne = None

# msg center
def afficher_messages():
    taille_carré = 400  
    x_carré = (largeur_fenetre - taille_carré) // 2  
    y_carré = (hauteur_fenetre - taille_carré) // 2  

    # Dessiner le carré
    pygame.draw.rect(fenetre, BLANC, (x_carré, y_carré, taille_carré, taille_carré))
    
    # les mgs
    y = y_carré + 20  
    for message in messages:
        texte_surface = police.render(message[0] + ": " + message[1], True, message[2])
        
        x_texte = x_carré + (taille_carré - texte_surface.get_width()) // 2
        fenetre.blit(texte_surface, (x_texte, y))
        y += texte_surface.get_height() + 10


envoyer_bouton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 700), (150, 50)),
                                               text='Envoyer',
                                               manager=manager)


message_zone_texte = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 700), (900, 50)),
                                                         manager=manager)


def gerer_actions_boutons(utilisateur):
    global utilisateur_selectionne
    print(f"Bouton cliqué pour l'Utilisateur : {utilisateur}")
    utilisateur_selectionne = utilisateur  

# Boucle principale
en_cours = True
horloge = pygame.time.Clock()
while en_cours:
    temps_passe = horloge.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == envoyer_bouton:
                    if utilisateur_selectionne is not None:
                        message = message_zone_texte.get_text()
                        messages.append((utilisateur_selectionne, message, COULEUR_MESSAGE_LOCAL))  
                        message_zone_texte.set_text('')
                else:
                    for bouton, utilisateur in boutons:
                        if event.ui_element == bouton:
                            gerer_actions_boutons(utilisateur)

        manager.process_events(event)

    manager.update(temps_passe)
    fenetre.fill(GRIS_CLAIR)
    afficher_messages()
    manager.draw_ui(fenetre)
    
    pygame.display.flip()  

pygame.quit()
