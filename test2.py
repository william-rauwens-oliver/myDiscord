import threading
import socket

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 33002))

def receive(nickname):  
    while True:
        try:
            message = client.recv(1024).decode('UTF-8')
            if message == 'NICK':
                client.send(nickname.encode('UTF-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break


def run(self, nickname):  
    print("Server is running on port", self.PORT)
    thread_reception = threading.Thread(target=self.recevoir, args=(nickname,))  # Passer le pseudonyme
    thread_reception.start()
    thread_reception.join()


def write():
    while True:
        try:
            recipients = input("Enter recipient(s) separated by comma (or leave blank for all): ").split(',')
            message_content = input("Enter message: ")

            message = f"{';'.join(recipients)}|{nickname}: {message_content}"
            client.send(message.encode('UTF-8'))
        except OSError as e:
            print("An error occurred:", e)
            break

receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

receive_thread.start()
write_thread.start()

receive_thread.join()
write_thread.join()


print("Program ended.")
