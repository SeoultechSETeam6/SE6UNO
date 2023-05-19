import pygame
import socket
import threading


class Client:
    def __init__(self):
        self.server_ip = '127.0.0.1'  # 서버 IP 주소 설정 (이 경우 로컬 IP)
        self.server_port = 10613  # 포트 번호 설정

        # 소켓 객체 생성 (TCP)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.temp1 = "1"
        self.temp2 = "2"
        self.temp3 = "3"

    def recv_data(self):
        while True:
            data = self.client_socket.recv(1024)
            print("recive : ", repr(data.decode()))

    def send_data(self):
        message = input('')
        self.client_socket.sendall(message.encode())
        self.client_socket.sendall(self.temp3.encode())
        self.client_socket.sendall(self.temp2.encode())
        self.client_socket.sendall(self.temp1.encode())

    def connect(self):
        try:
            # 서버에 연결
            self.client_socket.connect((self.server_ip, self.server_port))
            print('>> Connect Server')
            thread = threading.Thread(target=self.recv_data)
            thread.start()
        except:
            print(">> Can't Connect Server")

        # while True:
        #     pass
        #     self.client_socket.close()


game_client = Client()
game_client.connect()
while True:
    game_client.send_data()


