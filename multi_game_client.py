import pygame
import socket

server_ip = '127.0.0.1'  # 서버 IP 주소 설정 (이 경우 로컬 IP)
server_port = 10613  # 포트 번호 설정

# 소켓 객체 생성 (TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((server_ip, server_port))

# 메시지 전송
message = "Hello, Server!"
client_socket.sendall(message.encode())

# 소켓 닫기
client_socket.close()
