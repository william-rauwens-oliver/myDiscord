import mysql.connector
import sounddevice as sd
import numpy as np
import threading
import os
import datetime
from pydub import AudioSegment
from pydub.playback import play
from Login import Login

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

if __name__ == "__main__":
    enregistreur = EnregistreurVocal()
    enregistreur.executer()
