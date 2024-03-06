from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import mysql.connector
import time

class Server:
    def __init__(self, host='localhost', port=33002):
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
            'password': 'willy',
            'database': 'myDiscord'
        }
        self.mydb = mysql.connector.connect(**self.db_config)
        self.messages = []

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

        tchat = True
        while tchat:
            msg = client.recv(self.BUFSIZ)
            if msg.strip() != bytes("{quit}", "utf8"):
                author, message = msg.decode("utf8").split(":")
                if author in self.clients.values():
                    self.broadcast(msg, author + ": ")
                self.messages.append((author, message))
                print("Message received from %s: %s" % (author, message))
                print("Received message:", message)
                if message:
                    self.insert_messages_into_db(author, message)
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del self.clients[client]
                self.broadcast(bytes("%s has left the chat." % name, "utf8"))
                print("Client disconnected.")
                tchat = False

    def broadcast(self, msg, prefix=""):
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)

    def insert_messages_into_db(self, author, message):
        cursor = self.mydb.cursor()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO messages (author, content, timestamp) VALUES (%s, %s, %s)"
        cursor.execute(sql, (author, message, timestamp))
        self.mydb.commit()

    def delete_messages_from_db(self):
        cursor = self.mydb.cursor()
        for author, content in self.messages:
            sql = "DELETE FROM messages WHERE author = %s AND content = %s"
            cursor.execute(sql, (author, content))
            self.mydb.commit()
    
    def update_messages_in_db(self):
        cursor = self.mydb.cursor()
        for author, content, new_content in self.messages:
            sql = "UPDATE messages SET content = %s WHERE author = %s AND content = %s"
            cursor.execute(sql, (new_content, author, content))
            self.mydb.commit()

    def check_login(self, email, password):
        cursor = self.mydb.cursor()
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

    def insert_user(self, name, first_name, email, password):
        cursor = self.mydb.cursor()
        query = "INSERT INTO users (name, first_name, email, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, first_name, email, password))
        self.mydb.commit()

    def run(self):
        self.SERVER.listen(100)
        print("Waiting for connection...")
        ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.SERVER.close()


if __name__ == "__main__":
    server = Server()
    server.run()