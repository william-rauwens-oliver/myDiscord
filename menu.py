import pygame
import os
import cv2
import pygame_gui


pygame.init()

# Fenêtre
largeur_fenetre, hauteur_fenetre = 800, 800
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))

# pygame_gui
gestionnaire = pygame_gui.UIManager((largeur_fenetre, hauteur_fenetre))

# Bouton
bouton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, hauteur_fenetre -120), (150, 50)),
                                      text='se connecter',
                                      manager=gestionnaire)
# Bouton2
bouton2 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((largeur_fenetre - 160, hauteur_fenetre - 120), (150, 50)),
    text='Inscription',
    manager=gestionnaire
)





video_path = "img-son23/geek.mp4"
cap = cv2.VideoCapture(video_path)

largeur_video = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
hauteur_video = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Variables 
en_cours = True
aller_a_pendu = False
aller_a_niveau = False
lecture_video = True

# Bande son
pygame.mixer.music.load("img-son23/music.mp3")
pygame.mixer.music.set_volume(3)
pygame.mixer.music.play(1)  

while en_cours:
    delta_temps = pygame.time.Clock().tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

        gestionnaire.process_events(event)

        # Le bouton
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == bouton:
                    en_cours = False  # Sortir de la boucle while

    gestionnaire.update(delta_temps)

    if lecture_video:
        ret, frame = cap.read()
        if not ret:
            # Réinitialiser la capture vidéo pour lire la vidéo depuis le début
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (largeur_fenetre, hauteur_fenetre))
        frame_surface = pygame.image.frombuffer(frame.tobytes(), (largeur_fenetre, hauteur_fenetre), 'RGB')
        fenetre.blit(frame_surface, (0, 0))

    # Mettre à jour l'interface utilisateur pygame_gui
    gestionnaire.update(delta_temps)
    gestionnaire.draw_ui(fenetre)

    pygame.display.update()

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
pygame.quit()