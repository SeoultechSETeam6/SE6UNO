import socket
import threading
import pygame

server_ip = '127.0.0.1'  # 서버 IP 주소 설정 (이 경우 로컬 IP)
server_port = 10614  # 포트 번호 설정

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)

clients = []
clients_lock = threading.Lock()

clients.append(server_socket)

def client_handler(client_socket, addr):
    global clients
    with clients_lock:
        clients.append(client_socket)

    try:
        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg == 'start_game':
                with clients_lock:
                    for client in clients:
                        client.sendall('game_started'.encode('utf-8'))
            else:
                print(f"Message from {addr}: {msg}")
    except:
        print(f"Client {addr} disconnected")
    finally:
        with clients_lock:
            clients.remove(client_socket)
        client_socket.close()

while True:
    print("Waiting for clients...")
    client_socket, addr = server_socket.accept()
    print(f"Client {addr} connected")

    thread = threading.Thread(target=client_handler, args=(client_socket, addr))
    thread.start()

    if len(clients) == 0:
        client_socket.sendall("you_are_host".encode('utf-8'))
    else:
        client_socket.sendall('you_are_guest'.encode('utf-8'))

    message = input('')
    if message == 'quit':
        close_data = message
        break
    client_socket.send(message.encode())
