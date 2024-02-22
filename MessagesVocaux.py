import mysql.connector
import pygame
import pyaudio
import threading
from pydub import AudioSegment
import os
import datetime
from Login import Login

class EnregistreurVocal:
    def __init__(self):
        pygame.init()

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="willy",
            database="discord"
        )

        self.largeur, self.hauteur = 400, 300
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Enregistrement et Ecoute")

        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        self.police = pygame.font.SysFont('Arial', 24)
        self.enregistrement_en_cours = False
        self.chemin_actuel = os.path.dirname(os.path.abspath(__file__))

    def enregistrer_message_vocal(self, user_id, username, chemin_audio):
        try:
            cursor = self.mydb.cursor()
            insert_query = "INSERT INTO messagesvoice (user_id, username, audio_file, send_time) VALUES (%s, %s, %s, %s)"
            with open(chemin_audio, 'rb') as f:
                audio_data = f.read()
                send_time = datetime.datetime.now()
                cursor.execute(insert_query, (user_id, username, audio_data, send_time))
            self.mydb.commit()
            cursor.close()
            print("Message vocal enregistré avec succès !")
        except mysql.connector.Error as err:
            print(f"Erreur lors de l'insertion dans la base de données : {err}")

    def enregistrer_audio(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100

        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        frames = []

        print("Enregistrement vocal en cours...")

        while self.enregistrement_en_cours:
            data = stream.read(CHUNK)
            frames.append(data)

        print("Enregistrement terminé.")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        audio_data = b''.join(frames)
        audio_segment = AudioSegment(data=audio_data, sample_width=2, frame_rate=RATE, channels=CHANNELS)
        return audio_segment

    def toggle_enregistrement(self):
        self.enregistrement_en_cours = not self.enregistrement_en_cours
        if self.enregistrement_en_cours:
            t = threading.Thread(target=self.demarrer_enregistrement)
            t.start()

    def demarrer_enregistrement(self):
        audio_segment = self.enregistrer_audio()
        dossier_messages_vocaux = os.path.join(self.chemin_actuel, "MessagesVocaux")
        if not os.path.exists(dossier_messages_vocaux):
            os.makedirs(dossier_messages_vocaux)
        nom_fichier = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
        chemin_audio = os.path.join(dossier_messages_vocaux, nom_fichier)
        if self.enregistrement_en_cours:
            login = Login()
            if login.logged_in:
                user_id = login.user_id 
                username = login.username
                self.enregistrer_message_vocal(user_id, username, chemin_audio)
            else:
                print("Aucun utilisateur connecté. Impossible d'enregistrer le message vocal.")

    def executer(self):
        running = True
        while running:
            self.fenetre.fill(self.BLANC)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.toggle_enregistrement()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.toggle_enregistrement()

            texte = self.police.render("Cliquez et maintenez pour enregistrer un message vocal", True, self.NOIR)
            self.fenetre.blit(texte, (20, 20))

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    enregistreur = EnregistreurVocal()
    enregistreur.executer()