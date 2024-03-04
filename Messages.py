import cv2
import pygame
import pygame_gui
import time
import subprocess
from pydub import AudioSegment
from pydub.playback import play
from Login import Login
import mysql.connector
import sounddevice as sd
import numpy as np
import threading
import os
import datetime

pygame.init()

largeur_fenetre = 1283
hauteur_fenetre = 762
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))

fond_ecran = cv2.VideoCapture("Data/img-son23/pop.mp4")
vitesse_decalage = 3

manager = pygame_gui.UIManager((largeur_fenetre, hauteur_fenetre))

image_bouton_vocal = pygame.image.load("Data/img-son23/micro1.png")
image_bouton_vocal = pygame.transform.scale(image_bouton_vocal, (56, 56))

class Utilisateur:
    def __init__(self, nom, couleur_message):
        self.nom = nom
        self.couleur_message = couleur_message

COULEUR_MESSAGE_LOCAL = (114, 137, 218)
COULEUR_MESSAGE_DISTANT = (0, 0, 0)

utilisateurs = [Utilisateur('Kenny', COULEUR_MESSAGE_LOCAL),
                Utilisateur('Willy', COULEUR_MESSAGE_DISTANT),
                Utilisateur('Max', (255, 0, 0))]

messages = []

police = pygame.font.Font(None, 24)

utilisateur_selectionne = None

def afficher_messages():
    largeur_rectangle = 600
    hauteur_rectangle = 400
    x_rectangle = (largeur_fenetre - largeur_rectangle) // 2
    y_rectangle = (hauteur_fenetre - hauteur_rectangle) // 2

    #  le rectangle
    couleur_rect_transparent = (255, 255, 255, 100)  # Couleur avec une opacité réduite
    pygame.draw.rect(fenetre, couleur_rect_transparent, (x_rectangle, y_rectangle, largeur_rectangle, hauteur_rectangle), 0, 8)

    #  les msg
    y = y_rectangle + 20
    for message in messages:
        utilisateur = message[0]
        texte = message[1]
        couleur_message = utilisateur.couleur_message

        texte_surface = police.render(utilisateur.nom + ": " + texte, True, couleur_message)

        x_texte = x_rectangle + (largeur_rectangle - texte_surface.get_width()) // 2
        y_texte = y + (police.get_height() // 2) - (texte_surface.get_height() // 2)  # Centrer les msg
        fenetre.blit(texte_surface, (x_texte, y_texte))
        y += texte_surface.get_height() + 10


rayon_bouton = 33
espacement_bouton = 10
decalage_x = 80
decalage_y = 20

boutons = []
for i, utilisateur in enumerate(utilisateurs):
    bouton_rect = pygame.Rect(decalage_x, decalage_y + i * (2 * rayon_bouton + espacement_bouton), 2 * rayon_bouton, 2 * rayon_bouton)
    bouton = pygame_gui.elements.UIButton(relative_rect=bouton_rect, text=utilisateur.nom, manager=manager)
    boutons.append((bouton, utilisateur.nom))

# channel
chaines_supplementaires = ["1", "2", "3"]

for i, chaine in enumerate(chaines_supplementaires):
    bouton_chaine_rect = pygame.Rect((1120, 20 + i * (rayon_bouton * 2 + espacement_bouton)), (2 * rayon_bouton, 2 * rayon_bouton))
    bouton_chaine = pygame_gui.elements.UIButton(relative_rect=bouton_chaine_rect, text=chaine, manager=manager)
    boutons.append((bouton_chaine, chaine))

bouton_message_vocal_rect = pygame.Rect((1120, 687), (50, 50))

message_zone_texte = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 700), (900, 50)),
                                                         manager=manager)

class EnregistreurVocal:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="willy",
            database="discord"
        )

        self.enregistrement_en_cours = False
        self.chemin_actuel = os.path.dirname(os.path.abspath(__file__))
        self.audio_data = []

    def enregistrer_message_vocal(self, user_id, username, chemin_audio):
        try:
            cursor = self.mydb.cursor()
            insert_query = "INSERT INTO messagesvoice (user_id, username, audio_file, send_time) VALUES (%s, %s, %s, %s)"
            self.audio_data.export(chemin_audio, format="mp3")
            send_time = datetime.datetime.now()
            cursor.execute(insert_query, (user_id, username, chemin_audio, send_time))
            self.mydb.commit()
            cursor.close()
            print("Message vocal enregistré avec succès !")
        except mysql.connector.Error as err:
            print(f"Erreur lors de l'insertion dans la base de données : {err}")

    def start_recording(self):
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.audio_data.extend(indata.copy())

        with sd.InputStream(callback=callback):
            print("Enregistrement vocal en cours...")
            input("Appuyez sur Entrée pour arrêter l'enregistrement...")
        print("Enregistrement terminé.")

    def toggle_enregistrement(self):
        self.enregistrement_en_cours = not self.enregistrement_en_cours
        if self.enregistrement_en_cours:
            t = threading.Thread(target=self.start_recording)
            t.start()
        else:
            t = threading.Thread(target=self.stop_recording)
            t.start()

    def stop_recording(self):
        print("Arrêt de l'enregistrement...")
        self.audio_data = np.array(self.audio_data)
        self.audio_data = AudioSegment(self.audio_data.tobytes(), frame_rate=44100, sample_width=2, channels=2)
        dossier_messages_vocaux = os.path.join(self.chemin_actuel, "MessagesVocaux")
        if not os.path.exists(dossier_messages_vocaux):
            os.makedirs(dossier_messages_vocaux)
        nom_fichier = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp3"
        chemin_audio = os.path.join(dossier_messages_vocaux, nom_fichier)
        login = Login()
        if login.logged_in:
            user_id = login.user_id 
            username = login.username
            self.enregistrer_message_vocal(user_id, username, chemin_audio)
        else:
            print("Aucun utilisateur connecté. Impossible d'enregistrer le message vocal.")

    def executer(self):
        print("Enregistreur vocal démarré. Maintenez le clic gauche pour enregistrer, relâchez pour terminer.")
        while True:
            user_input = input("Appuyez sur 'q' pour quitter: ")
            if user_input.lower() == 'q':
                break
            else:
                self.toggle_enregistrement()

def gerer_actions_boutons(utilisateur_nom):
    global utilisateur_selectionne
    print(f"Bouton cliqué pour l'Utilisateur/Chaîne : {utilisateur_nom}")

    utilisateur_selectionne = next((utilisateur for utilisateur in utilisateurs if utilisateur.nom == utilisateur_nom), None)
    if utilisateur_selectionne:
        messages.append((utilisateur_selectionne, "Bonjour!", utilisateur_selectionne.couleur_message))
    # Ajoutez des actions pour les chaînes supplémentaires ici si nécessaire

def afficher_image_bouton_vocal(rect):
    fenetre.blit(image_bouton_vocal, rect.topleft)

def enregistrer_message_vocal():
    subprocess.Popen(["python", "Messagevocaux.py"])

running = True
clic_long_temps = 0 
while running:
    ret, frame = fond_ecran.read()
    if not ret:
        fond_ecran.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_pygame = pygame.image.frombuffer(frame_rgb.flatten(), (frame_rgb.shape[1::-1]), 'RGB')

    frame_pygame = pygame.transform.scale(frame_pygame, (largeur_fenetre, hauteur_fenetre))

    fenetre.blit(frame_pygame, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if bouton_message_vocal_rect.collidepoint(event.pos):
                    clic_long_temps = pygame.time.get_ticks()
                    enregistrement_en_cours = True
                    enregistrer_message_vocal()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for bouton, item in boutons:
                    if event.ui_element == bouton:
                        gerer_actions_boutons(item)

            elif event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == message_zone_texte:
                    texte = event.text
                    if texte and utilisateur_selectionne:
                        messages.append((utilisateur_selectionne, texte, utilisateur_selectionne.couleur_message))
                        message_zone_texte.set_text('')

    manager.process_events(event)
    manager.update(time.time())

    afficher_messages()

    manager.draw_ui(fenetre)

    afficher_image_bouton_vocal(bouton_message_vocal_rect)

    pygame.display.flip()

    time.sleep(0.1 / vitesse_decalage)

fond_ecran.release()
pygame.quit()
