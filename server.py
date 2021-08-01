import threading
import socket

host = '127.0.0.1'
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
usernames = []


def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle clients'connections


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            print(f'[NEW MESSAGE] -> {client}: {message}\n')
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = usernames[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            print(f"[CONNECTION CLOSED] -> {alias} has left the chat room!\n")
            usernames.remove(alias)
            break
# Main function to receive the clients connection


def receive():
    while True:
        print(f'[SERVER STARTING] -> Server hosted on {host}:{port}\n\n')
        client, address = server.accept()
        print(f'[NEW CONNECTION] -> Connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        usernames.append(alias)
        clients.append(client)
        print(f'    The username of this client is {alias}\n'.encode('utf-8'))
        broadcast(f'\n{alias} has connected to the chat room\n'.encode('utf-8'))
        client.send('Successfully connected to chatroom!\n'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()