import pygame
import os
import cv2
import pygame_gui

pygame.init()


new_var = 1283, 762
largeur_fenetre, hauteur_fenetre = new_var
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))


gestionnaire = pygame_gui.UIManager((largeur_fenetre, hauteur_fenetre))

# Centre
x_bouton1 = (largeur_fenetre - 310) // 2
x_bouton2 = (largeur_fenetre + 160) // 2


bouton_image = pygame.image.load("img-son23/inscription.png")
bouton_image = pygame.transform.scale(bouton_image, (80, 40))  
bouton2_image = pygame.image.load("img-son23/connect.png")
bouton2_image = pygame.transform.scale(bouton2_image, (80, 40))  

# Bouton1
bouton_rect = pygame.Rect((x_bouton1, hauteur_fenetre - 120), (150, 50))
bouton = pygame_gui.elements.UIButton(relative_rect=bouton_rect,
                                      text='connexion',
                                      manager=gestionnaire)
bouton.set_image(bouton_image)

# Bouton2
bouton2_rect = pygame.Rect((x_bouton2, hauteur_fenetre - 120), (150, 50))
bouton2 = pygame_gui.elements.UIButton(relative_rect=bouton2_rect,
                                       text='Inscription',
                                       manager=gestionnaire)
bouton2.set_image(bouton2_image)

video_path = "img-son23/geek.mp4"
cap = cv2.VideoCapture(video_path)

largeur_video = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
hauteur_video = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

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
                    en_cours = False

    gestionnaire.update(delta_temps)

    if lecture_video:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (largeur_fenetre, hauteur_fenetre))
        frame_surface = pygame.image.frombuffer(frame.tobytes(), (largeur_fenetre, hauteur_fenetre), 'RGB')
        fenetre.blit(frame_surface, (0, 0))

    gestionnaire.update(delta_temps)
    gestionnaire.draw_ui(fenetre)

    pygame.display.update()

cap.release()
cv2.destroyAllWindows()
pygame.quit()
