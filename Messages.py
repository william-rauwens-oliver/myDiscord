import cv2
import pygame
import pygame_gui
import time
import sounddevice as sd
from scipy.io.wavfile import write
import os

# Importer la classe de connexion et la méthode de déconnexion
from Login import Login
from LogOut import Logout

pygame.init()

# Déclarer les dimensions de la fenêtre
largeur_fenetre = 1283
hauteur_fenetre = 762
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))

# Charger la vidéo d'arrière-plan
fond_ecran = cv2.VideoCapture('Data/img-son23/pop.mp4')
vitesse_decalage = 3

# Créer le gestionnaire d'interface utilisateur
manager = pygame_gui.UIManager((largeur_fenetre, hauteur_fenetre))

# Charger l'image du bouton vocal et le redimensionner
image_bouton_vocal = pygame.image.load("Data/img-son23/micro1.png")
image_bouton_vocal = pygame.transform.scale(image_bouton_vocal, (56, 56))

# Définir les utilisateurs avec leurs couleurs de message
class Utilisateur:
    def __init__(self, nom, couleur_message):
        self.nom = nom
        self.couleur_message = couleur_message

COULEUR_MESSAGE_LOCAL = (114, 137, 218)
COULEUR_MESSAGE_DISTANT = (0, 0, 0)

utilisateurs = [Utilisateur('Kenny', COULEUR_MESSAGE_LOCAL),
                Utilisateur('Willy', COULEUR_MESSAGE_DISTANT),
                Utilisateur('Max', (255, 0, 0))]

messages = []  # Liste des messages

police = pygame.font.Font(None, 24)  # Police de caractères pour les messages

utilisateur_selectionne = None  # Utilisateur sélectionné

# Fonction pour afficher les messages à l'écran
def afficher_messages():
    largeur_rectangle = 600
    hauteur_rectangle = 400
    x_rectangle = (largeur_fenetre - largeur_rectangle) // 2
    y_rectangle = (hauteur_fenetre - hauteur_rectangle) // 2

    couleur_rect_transparent = (255, 255, 255, 100)
    pygame.draw.rect(fenetre, couleur_rect_transparent, (x_rectangle, y_rectangle, largeur_rectangle, hauteur_rectangle), 0, 8)

    y = y_rectangle + 20
    for message in messages:
        utilisateur = message[0]
        texte = message[1]
        couleur_message = utilisateur.couleur_message

        texte_surface = police.render(utilisateur.nom + ": " + texte, True, couleur_message)

        x_texte = x_rectangle + (largeur_rectangle - texte_surface.get_width()) // 2
        y_texte = y + (police.get_height() // 2) - (texte_surface.get_height() // 2)
        fenetre.blit(texte_surface, (x_texte, y_texte))
        y += texte_surface.get_height() + 10

rayon_bouton = 33
espacement_bouton = 10
decalage_x = 80
decalage_y = 20

boutons = []  # Liste des boutons
for i, utilisateur in enumerate(utilisateurs):
    bouton_rect = pygame.Rect(decalage_x, decalage_y + i * (2 * rayon_bouton + espacement_bouton), 2 * rayon_bouton, 2 * rayon_bouton)
    bouton = pygame_gui.elements.UIButton(relative_rect=bouton_rect, text=utilisateur.nom, manager=manager)
    boutons.append((bouton, utilisateur.nom))

chaines_supplementaires = ["1", "2", "3"]

for i, chaine in enumerate(chaines_supplementaires):
    bouton_chaine_rect = pygame.Rect((1120, 20 + i * (rayon_bouton * 2 + espacement_bouton)), (2 * rayon_bouton, 2 * rayon_bouton))
    bouton_chaine = pygame_gui.elements.UIButton(relative_rect=bouton_chaine_rect, text=chaine, manager=manager)
    boutons.append((bouton_chaine, chaine))

bouton_message_vocal_rect = pygame.Rect((1120, 687), (56, 56))  # Rectangle du bouton vocal

message_zone_texte = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 700), (900, 50)),
                                                         manager=manager)

# Définir l'état du clic de souris
clic_gauche_enfonce = False
enregistrement_en_cours = False

def gerer_actions_boutons(utilisateur_nom):
    global utilisateur_selectionne
    print(f"Bouton cliqué pour l'Utilisateur/Chaîne : {utilisateur_nom}")

    utilisateur_selectionne = next((utilisateur for utilisateur in utilisateurs if utilisateur.nom == utilisateur_nom), None)
    if utilisateur_selectionne:
        messages.append((utilisateur_selectionne, "Bonjour!", utilisateur_selectionne.couleur_message))

def afficher_image_bouton_vocal(rect):
    fenetre.blit(image_bouton_vocal, rect.topleft)

def gerer_message_vocal():
    global enregistrement_en_cours
    if not enregistrement_en_cours:
        enregistrement_en_cours = True
        pygame.mixer.init()  
        pygame.mixer.set_num_channels(1)  

        global nom_fichier_vocal
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")  # Ajout du timestamp dans le nom du fichier
        nom_fichier_vocal = f"message_vocal_{timestamp}.wav"  

        fs = 44100  
        duree_enregistrement = 5  

        print("Enregistrement du message vocal... Parlez maintenant !")
        enregistrement = sd.rec(int(duree_enregistrement * fs), samplerate=fs, channels=2)

        while True:
            # Vérifie si le clic gauche est toujours enfoncé
            if not clic_gauche_enfonce:
                break

            # Si le clic gauche est toujours enfoncé, continue l'enregistrement
            sd.wait()  
            print("Enregistrement terminé.")

            # Modification du chemin de sauvegarde pour inclure le dossier "MessagesVocaux"
            chemin_complet = os.path.join("MessagesVocaux", nom_fichier_vocal)
            write(chemin_complet, fs, enregistrement)  
            print(f"Message vocal enregistré sous : {chemin_complet}")

            if utilisateur_selectionne:
                messages.append((utilisateur_selectionne, nom_fichier_vocal, utilisateur_selectionne.couleur_message))  # Ajoutez le message vocal à la liste des messages

            enregistrement_en_cours = False
            
            # Lire le fichier audio
            pygame.mixer.music.load(chemin_complet)
            pygame.mixer.music.play()
            
            break

running = True
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

        elif event.type == pygame.USEREVENT:
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

        # Détection du clic de souris
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Bouton gauche de la souris
                if bouton_message_vocal_rect.collidepoint(event.pos):  # Vérifie si les coordonnées du clic sont dans le rectangle du bouton vocal
                    clic_gauche_enfonce = True
                    gerer_message_vocal()  # Démarrez l'enregistrement du message vocal

        # Détection du relâchement du clic de souris
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Bouton gauche de la souris
                clic_gauche_enfonce = False

        manager.process_events(event)

    manager.update(time.time())

    afficher_messages()

    manager.draw_ui(fenetre)

    afficher_image_bouton_vocal(bouton_message_vocal_rect)

    # Afficher l'adresse e-mail de l'utilisateur connecté en bas à gauche
    logged_in_email = Login.get_logged_in_user_email()  # Supposons que la méthode pour obtenir l'e-mail de l'utilisateur connecté est définie dans la classe Login
    email_surface = police.render(logged_in_email, True, (255, 255, 255))
    fenetre.blit(email_surface, (10, hauteur_fenetre - 30))  # Afficher l'adresse e-mail en bas à gauche

    pygame.display.flip()

    time.sleep(0.1 / vitesse_decalage)

fond_ecran.release()
pygame.quit()
