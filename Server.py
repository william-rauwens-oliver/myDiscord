from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class Server:
    @staticmethod
    def accept_incoming_connections(server):
        while True:
            client, client_address = server.accept()
            print("%s:%s has connected." % client_address)
            client.send(bytes(welcome, "utf8"))
            client.send(bytes("Enter your name:", "utf8"))
            addresses[client] = client_address
            Thread(target=Server.handle_client, args=(client,)).start()

    @staticmethod
    def handle_client(client):
        name = client.recv(BUFSIZ).decode("utf8")
        welcome_msg = "Welcome, %s! If you ever want to quit, type {quit} to exit." % name
        client.send(bytes(welcome_msg, "utf8"))
        msg = "%s has joined the chat!" % name
        Server.broadcast(bytes(msg, "utf8"))
        clients[client] = name
        while True:
            msg = client.recv(BUFSIZ)
            if msg.strip() != bytes("{quit}", "utf8"):
                Server.broadcast(msg, name+": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                Server.broadcast(bytes("%s has left the chat." % name, "utf8"))
                break

    @staticmethod
    def broadcast(msg, prefix=""):
        for sock in clients:
            sock.send(bytes(prefix, "utf8") + msg)

clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    welcome = "Welcome to the chat room! Please type your name and press Enter to join."
    SERVER.listen(100)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=Server.accept_incoming_connections, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
