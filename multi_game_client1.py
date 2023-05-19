import pygame
import socket
import threading

server_ip = '127.0.0.1'  # 서버 IP 주소 설정 (이 경우 로컬 IP)
server_port = 10613  # 포트 번호 설정

# 소켓 객체 생성 (TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((server_ip, server_port))


def recv_data(client_socket) :
    while True :
        data = client_socket.recv(1024)

        print("recive : ", repr(data.decode()))


thread = threading.Thread(target=recv_data, args=(client_socket, ))
thread.start()
print('>> Connect Server')


while True:
    message = input('')
    if message == 'quit':
        close_data = message
        break
    client_socket.send(message.encode())


client_socket.close()