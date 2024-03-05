import pygame
import os
import cv2
import pygame_gui
import subprocess

pygame.init()

new_var = 1283, 762
largeur_fenetre, hauteur_fenetre = new_var
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))

gestionnaire = pygame_gui.UIManager((largeur_fenetre, hauteur_fenetre))

bouton_image = pygame.image.load("Data/img-son23/inscription.png")
bouton_image = pygame.transform.scale(bouton_image, (80, 40))  
bouton2_image = pygame.image.load("Data/img-son23/connect.png")
bouton2_image = pygame.transform.scale(bouton2_image, (80, 40))  

video_path = "Data/img-son23/geek.mp4"
cap = cv2.VideoCapture(video_path)

largeur_video = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
hauteur_video = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

en_cours = True
lecture_video = True
video_terminee = False

pygame.mixer.music.load("Data/img-son23/music.mp3")
pygame.mixer.music.set_volume(3)
pygame.mixer.music.play(1)

while en_cours:
    delta_temps = pygame.time.Clock().tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

        gestionnaire.process_events(event)

    gestionnaire.update(delta_temps)

    if lecture_video and not video_terminee:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

            video_terminee = True

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (largeur_fenetre, hauteur_fenetre))
        frame_surface = pygame.image.frombuffer(frame.tobytes(), (largeur_fenetre, hauteur_fenetre), 'RGB')
        fenetre.blit(frame_surface, (0, 0))

    gestionnaire.update(delta_temps)

    pygame.display.update()
    
    if video_terminee:
        en_cours = False

cap.release()
cv2.destroyAllWindows()
pygame.quit()

subprocess.run(["python", "Messages.py"])