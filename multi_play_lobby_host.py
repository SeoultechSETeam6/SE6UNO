import socket
import threading
import pygame
import multiprocessing

from controller import game_view
from controller.mouse import Mouse
from scene.single_play import SinglePlay
from scene.single_play_lobby import SinglePlayLobby


class MultiPlayLobbyServer(SinglePlayLobby):
    def __init__(self):
        super().__init__()
        self.server_ip = '127.0.0.1'  # 서버 IP 주소 설정 (이 경우 로컬 IP)
        self.server_port = 10613  # 포트 번호 설정

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(5)

        self.clients = []
        self.clients_attend_flag = [False, False, False, False, False]
        self.clients_lock = threading.Lock()

        self.game_start = False

        self.image_player_joined = pygame.transform.scale(
            pygame.image.load("./resources/Image/lobby_images/player_enter.png"),
            (self.ui_size["logo"][0] * 0.5, self.ui_size["logo"][1] * 0.4))

    def event_join_computer_1(self):
        if not self.clients_attend_flag[0]:
            super().event_join_computer_1()

    def event_join_computer_2(self):
        if not self.clients_attend_flag[1]:
            super().event_join_computer_2()

    def event_join_computer_3(self):
        if not self.clients_attend_flag[2]:
            super().event_join_computer_3()

    def event_join_computer_4(self):
        if not self.clients_attend_flag[3]:
            super().event_join_computer_4()

    def event_join_computer_5(self):
        if not self.clients_attend_flag[4]:
            super().event_join_computer_5()

    def event_start(self):
        print("게임 시작")

    def client_handler(self, client_socket, addr):
        with self.clients_lock:
            self.clients_attend_flag[len(self.clients)] = True
            self.computers_attend_flag[len(self.clients)] = False
            self.clients.append(client_socket)
        try:
            pass
        except:
            print(f"Client {addr} disconnected")
        finally:
            with self.clients_lock:
                self.clients.remove(client_socket)
                self.clients_attend_flag[len(self.clients)] = False
            for client in self.clients:
                client.sendall(str(self.clients.index(client_socket)).encode())
            client_socket.close()

    def connect(self):
        while True:
            print("Waiting for clients...")

            client_socket, addr = self.server_socket.accept()
            print(f"Client {addr} connected")

            thread = threading.Thread(target=self.client_handler, args=(client_socket, addr))
            thread.start()
            client_socket.sendall(str(self.clients.index(client_socket)).encode())

    def draw(self):
        for i, button in enumerate(self.buttons_computer):
            # 팝업 떠있을 경우 감지하지 않음
            if not self.popup.pop:
                button.detect_event()
            if self.clients_attend_flag[i]:
                self.screen.blit(self.image_player_joined, (button.x, button.y))
        super().draw()

    def exec(self):
        process_run = multiprocessing.Process(target=self.run)
        process_run.start()
        process_connect = multiprocessing.Process(target=self.connect)
        process_connect.start()

        process_run.join()
        process_connect.join()


lobby_server = MultiPlayLobbyServer()
lobby_server.exec()
