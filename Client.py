import threading
import socket

_ip = input("ip (leave blank for localhost): ").strip()
if _ip == "":
    _ip = "127.0.0.1"
_port = input("port (leave blank for 8080): ")
if _port == "":
    _port = 8080
alias = input('Enter what you want to be seen as: ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((_ip, int(_port)))


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error connecting to server')
            client.close()
            break


def client_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()