from socket import AF_INET, socket, SOCK_STREAM

HOST = '127.0.0.1'  # Adresse IP du serveur
PORT = 33000  # Le port sur lequel le serveur écoute
BUFSIZ = 1024  # La taille du buffer de réception

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    message = input("Enter message (type {quit} to exit): ")
    client_socket.send(bytes(message, "utf8"))
    if message == "{quit}":
        break
    data = client_socket.recv(BUFSIZ)
    print("Received:", data.decode("utf8"))

client_socket.close()
