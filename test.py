import threading
from socket import AF_INET, socket, SOCK_STREAM
import time
import mysql.connector

class Server:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind(self.ADDR)
        self.clients = {}
        self.addresses = {}
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'database': 'myDiscord'
        }
        self.mydb = mysql.connector.connect(**self.db_config)

    def insert_message_into_db(self, author, timestamp, content):
        cursor = self.mydb.cursor()
        sql = "INSERT INTO messages (author, content, timestamp) VALUES (%s, %s, %s)"
        cursor.execute(sql, (author, content, timestamp))
        self.mydb.commit()
        cursor.close()

    def run(self):
        self.SERVER.listen()
        print("Server is running on port", self.PORT)
        thread_reception = threading.Thread(target=self.recevoir)
        thread_reception.start()
        thread_reception.join()  
        if __name__ == "__main__":
            HOST = '127.0.0.1'
            PORT = 33002
            nickname = input("Choose your nickname: ")
            server = Server(HOST, PORT)
            server.run(nickname)  

    def recevoir(self):
        while True:
            client, adresse = self.SERVER.accept()
            print("Connecté avec {}".format(str(adresse)))
            client.send('NICK'.encode('ascii'))
            surnom = client.recv(1024).decode('ascii')
            self.addresses[client] = adresse
            self.clients[client] = surnom
            print("Le surnom est {}".format(surnom))
            self.diffusion("{} a rejoint!".format(surnom).encode('ascii'))
            client.send('Connecté au serveur!'.encode('ascii'))
            thread = threading.Thread(target=self.gerer, args=(client,))
            thread.start()

    def gerer(self, client):
        while True:
            try:
                message = client.recv(1024)
                if message:
                    destinataires, contenu_message = message.decode('UTF-8').split('|')
                    destinataires = destinataires.split(';')
                    self.envoyer_a_destinataires(contenu_message.encode('UTF-8'), client, destinataires)
            except:
                surnom = self.clients[client]
                self.diffusion('{} left!'.format(surnom).encode('UTF-8'))
                del self.clients[client]
                client.close()
                break

    def diffusion(self, message):
        for client in self.clients:
            client.send(message)

    def envoyer_a_destinataires(self, message, client_expediteur, destinataires):
        for client, surnom in zip(self.clients, self.clients.values()):
            if surnom in destinataires and client != client_expediteur:
                try:
                    client.send(message)
                except:
                    index = list(self.clients.keys()).index(client)
                    del self.clients[client]
                    client.close()
                    surnom_supprime = list(self.clients.values())[index]
                    self.diffusion('{} left!'.format(surnom_supprime).encode('UTF-8'))


