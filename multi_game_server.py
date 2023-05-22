import socket
import threading
import pygame

from scene.single_play import SinglePlay


class Server:
    def __init__(self):
        self.server_ip = '127.0.0.1'  # 서버 IP 주소 설정 (이 경우 로컬 IP)
        self.server_port = 10613  # 포트 번호 설정

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(5)

        self.clients = []
        self.clients_lock = threading.Lock()

        self.game_start = False

    def client_handler(self, client_socket, addr):
        with self.clients_lock:
            self.clients.append(client_socket)
        try:
            while True:
                data = client_socket.recv(1024)
                print(data)
                if data is not None:
                    if self.game_start:
                        for client in self.clients:
                            if client is not client_socket:
                                client.sendall(data)
                    if client_socket is self.clients[0]:
                        msg = data.decode('utf-8')
                        if msg == 'start_game':
                            self.game_start = True
                            for client in self.clients:
                                client.sendall('start_game'.encode('utf-8'))
                    else:
                        client_socket.sendall('not_host'.encode('utf-8'))

        except:
            print(f"Client {addr} disconnected")
        finally:
            with self.clients_lock:
                self.clients.remove(client_socket)
            client_socket.close()

    def connect(self):
        print("Waiting for clients...")
        client_socket, addr = self.server_socket.accept()
        print(f"Client {addr} connected")

        thread = threading.Thread(target=self.client_handler, args=(client_socket, addr))
        thread.start()


game_server = Server()
while True:
    game_server.connect()
