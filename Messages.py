import cv2
import pygame
import pygame_gui
import time
import sounddevice as sd
from scipy.io.wavfile import write
import os
from socket import AF_INET, socket, SOCK_STREAM
from ServeurGlobal import Server

class Application:
    def __init__(self):
        pygame.init()

    def run(self):
        raise NotImplementedError("La méthode 'run' doit être implémentée dans les sous-classes.")

class Utilisateur:
    def __init__(self, nom, couleur_message):
        self.nom = nom
        self.couleur_message = couleur_message

class Fenetre:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.fenetre = pygame.display.set_mode((largeur, hauteur))

    def afficher(self, frame_pygame, position):
        self.fenetre.blit(frame_pygame, position)

class InterfaceUtilisateur:
    def __init__(self, largeur_fenetre, hauteur_fenetre, manager):
        self.largeur_fenetre = largeur_fenetre
        self.hauteur_fenetre = hauteur_fenetre
        self.manager = manager

    def ajouter_bouton_utilisateur(self, decalage_x, decalage_y, rayon_bouton, espacement_bouton, utilisateurs):
        boutons = []
        for i, utilisateur in enumerate(utilisateurs):
            bouton_rect = pygame.Rect(decalage_x, decalage_y + i * (2 * rayon_bouton + espacement_bouton), 2 * rayon_bouton, 2 * rayon_bouton)
            bouton = pygame_gui.elements.UIButton(relative_rect=bouton_rect, text=utilisateur.nom, manager=self.manager)
            boutons.append((bouton, utilisateur.nom))
        return boutons

    def ajouter_bouton_chaine(self, rayon_bouton, espacement_bouton, chaines_supplementaires):
        boutons = []
        for i, chaine in enumerate(chaines_supplementaires):
            bouton_chaine_rect = pygame.Rect((1120, 20 + i * (rayon_bouton * 2 + espacement_bouton)), (2 * rayon_bouton, 2 * rayon_bouton))
            bouton_chaine = pygame_gui.elements.UIButton(relative_rect=bouton_chaine_rect, text=chaine, manager=self.manager)
            boutons.append((bouton_chaine, chaine))
        return boutons

    def ajouter_bouton_message_vocal(self):
        bouton_message_vocal_rect = pygame.Rect((1120, 687), (56, 56))
        message_zone_texte = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 700), (900, 50)),
                                                                 manager=self.manager)
        return bouton_message_vocal_rect, message_zone_texte

class Chat:
    def __init__(self, police, utilisateur_selectionne, messages):
        self.police = police
        self.utilisateur_selectionne = utilisateur_selectionne
        self.messages = messages

    def afficher(self, fenetre):
        largeur_rectangle = 600
        hauteur_rectangle = 400
        x_rectangle = (fenetre.largeur - largeur_rectangle) // 2
        y_rectangle = (fenetre.hauteur - hauteur_rectangle) // 2

        couleur_rect_transparent = (255, 255, 255, 100)
        pygame.draw.rect(fenetre.fenetre, couleur_rect_transparent, (x_rectangle, y_rectangle, largeur_rectangle, hauteur_rectangle), 0, 8)

        y = y_rectangle + 20
        for message in self.messages:
            utilisateur = message[0]
            texte = message[1]
            couleur_message = utilisateur.couleur_message

            texte_surface = self.police.render(utilisateur.nom + ": " + texte, True, couleur_message)

            x_texte = x_rectangle + (largeur_rectangle - texte_surface.get_width()) // 2
            y_texte = y + (self.police.get_height() // 2) - (texte_surface.get_height() // 2)
            fenetre.fenetre.blit(texte_surface, (x_texte, y_texte))
            y += texte_surface.get_height() + 10

class EnregistrementVocal:
    def __init__(self):
        self.clic_gauche_enfonce = False
        self.enregistrement_en_cours = False
        self.nom_fichier_vocal = None

    def gerer_message_vocal(self, utilisateur_selectionne, messages):
        if not self.enregistrement_en_cours:
            self.enregistrement_en_cours = True
            pygame.mixer.init()  
            pygame.mixer.set_num_channels(1)  

            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            self.nom_fichier_vocal = f"message_vocal_{timestamp}.wav"  

            fs = 44100  
            duree_enregistrement = 5  

            print("Enregistrement du message vocal... Parlez maintenant !")
            enregistrement = sd.rec(int(duree_enregistrement * fs), samplerate=fs, channels=2)

            while True:
                if not self.clic_gauche_enfonce:
                    break

                sd.wait()  
                print("Enregistrement terminé.")
                chemin_complet = os.path.join("MessagesVocaux", self.nom_fichier_vocal)
                write(chemin_complet, fs, enregistrement)  
                print(f"Message vocal enregistré sous : {chemin_complet}")

                if utilisateur_selectionne:
                    messages.append((utilisateur_selectionne, self.nom_fichier_vocal, utilisateur_selectionne.couleur_message))  # Ajoutez le message vocal à la liste des messages

                self.enregistrement_en_cours = False
                break

class MainApplication(Application):
    def __init__(self):
        super().__init__()

    def run(self):
        largeur_fenetre = 1283
        hauteur_fenetre = 762
        fenetre = Fenetre(largeur_fenetre, hauteur_fenetre)
        fond_ecran = cv2.VideoCapture('Data/img-son23/pop.mp4')
        vitesse_decalage = 3
        manager = pygame_gui.UIManager((largeur_fenetre, hauteur_fenetre))
        COULEUR_MESSAGE_LOCAL = (114, 137, 218)
        COULEUR_MESSAGE_DISTANT = (0, 0, 0)
        utilisateurs = [Utilisateur('Kenny', COULEUR_MESSAGE_LOCAL),
                        Utilisateur('Willy', COULEUR_MESSAGE_DISTANT),
                        Utilisateur('Max', (255, 0, 0))]
        messages = []

        police = pygame.font.Font(None, 24)
        utilisateur_selectionne = None
        interface_utilisateur = InterfaceUtilisateur(largeur_fenetre, hauteur_fenetre, manager)

        rayon_bouton = 33
        espacement_bouton = 10
        decalage_x = 80
        decalage_y = 20
        boutons_utilisateurs = interface_utilisateur.ajouter_bouton_utilisateur(decalage_x, decalage_y, rayon_bouton, espacement_bouton, utilisateurs)
        chaines_supplementaires = ["1", "2", "3"]
        boutons_chaines = interface_utilisateur.ajouter_bouton_chaine(rayon_bouton, espacement_bouton, chaines_supplementaires)
        bouton_message_vocal_rect, message_zone_texte = interface_utilisateur.ajouter_bouton_message_vocal()
        enregistrement_vocal = EnregistrementVocal()

        running = True
        while running:
            ret, frame = fond_ecran.read()
            if not ret:
                fond_ecran.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pygame = pygame.image.frombuffer(frame_rgb.flatten(), (frame_rgb.shape[1::-1]), 'RGB')
            frame_pygame = pygame.transform.scale(frame_pygame, (largeur_fenetre, hauteur_fenetre))

            fenetre.afficher(frame_pygame, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        for bouton, item in boutons_utilisateurs + boutons_chaines:
                            if event.ui_element == bouton:
                                utilisateur_selectionne = next((utilisateur for utilisateur in utilisateurs if utilisateur.nom == item), None)
                                if utilisateur_selectionne:
                                    messages.append((utilisateur_selectionne, "Bonjour!", utilisateur_selectionne.couleur_message))

                    elif event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                        if event.ui_element == message_zone_texte:
                            texte = event.text
                            if texte and utilisateur_selectionne:
                                messages.append((utilisateur_selectionne, texte, utilisateur_selectionne.couleur_message))
                                message_zone_texte.set_text('')

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if bouton_message_vocal_rect.collidepoint(event.pos): 
                            enregistrement_vocal.clic_gauche_enfonce = True
                            enregistrement_vocal.gerer_message_vocal(utilisateur_selectionne, messages)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        enregistrement_vocal.clic_gauche_enfonce = False

                manager.process_events(event)

            manager.update(time.time())

            chat = Chat(police, utilisateur_selectionne, messages)
            chat.afficher(fenetre)

            manager.draw_ui(fenetre.fenetre)

            pygame.display.flip()

            time.sleep(0.1 / vitesse_decalage)

        fond_ecran.release()
        pygame.quit()

if __name__ == "__main__":
    app = MainApplication()
    app.run()