import pygame
import socket
import threading

server_ip = '127.0.0.1'  # 서버 IP 주소 설정 (이 경우 로컬 IP)
server_port = 10613  # 포트 번호 설정

# 소켓 객체 생성 (TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 주소 재사용을 위한 설정
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# IP 주소와 포트를 바인딩
server_socket.bind((server_ip, server_port))

# 소켓이 연결 요청을 기다리도록 설정
server_socket.listen(5)

print(f"[*] Listening on {server_ip}:{server_port}")

# 클라이언트 연결 수락
client_socket, client_address = server_socket.accept()
print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

# 클라이언트로부터 메시지 수신
message = client_socket.recv(1024)
print(f"[*] Received: {message.decode()}")

# 소켓 닫기
client_socket.close()
server_socket.close()
