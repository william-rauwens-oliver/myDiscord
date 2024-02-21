from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import mysql.connector
import time

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

    def accept_incoming_connections(self):
        while True:
            client, client_address = self.SERVER.accept()
            print("%s:%s has connected." % client_address)
            client.send(bytes("Welcome to the chat room! Please type your name and press Enter to join.", "utf8"))
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        name = client.recv(self.BUFSIZ).decode("utf8")
        if not name:
            client.send(bytes("Please enter a valid name.", "utf8"))
            client.close()
            return

        welcome_msg = "Welcome, %s! If you ever want to quit, type {quit} to exit." % name
        client.send(bytes(welcome_msg, "utf8"))
        self.broadcast(bytes("%s has joined the chat!" % name, "utf8"))

        while True:
            msg = client.recv(self.BUFSIZ)
            if msg.strip() == bytes("{quit}", "utf8"):
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del self.clients[client]
                self.broadcast(bytes("%s has left the chat." % name, "utf8"))
                break
            else:
                self.broadcast(msg, name+": ")
                self.insert_message_into_db(name, time.strftime('%Y-%m-%d %H:%M:%S'), msg.decode("utf8"))
                print("Message received from %s: %s" % (name, msg.decode("utf8")))
                print("Message inserted into database by %s: %s" % (name, msg.decode("utf8")))


    def broadcast(self, msg, prefix=""):
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)

    def insert_message_into_db(self, author, timestamp, content):
        cursor = self.mydb.cursor()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO messages (author, content, timestamp) VALUES (%s, %s, %s)"
        cursor.execute(sql, (author, content, timestamp))
        self.mydb.commit()
        
    
    def run(self):
        self.SERVER.listen(100)
        print("Waiting for connection...")
        ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.SERVER.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 33002
    server = Server(HOST, PORT)
    server.run()
    
    

