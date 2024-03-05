from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys


class Client:
    def __init__(self, host, port, name):
        self.HOST = host
        self.PORT = port
        self.name = name
        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.receive_thread = Thread(target=self.receive_messages)
        self.receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                print(msg)
            except OSError: 
                break 

    def send_message(self, msg):
        self.client_socket.send(bytes(msg, "utf8"))

    def start(self):
        while True:
            msg = input("%s: " % self.name) 
            if msg == "{quit}":
                self.client_socket.close()
                sys.exit()
            self.send_message(msg)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 33002
    name = input("Enter your name: ") 
    client = Client(HOST, PORT, name)
    client.start()
    