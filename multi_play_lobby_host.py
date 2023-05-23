import socket
import threading
import pygame
import multiprocessing
import pickle

from ui.button import Button, ImageButton
from controller import game_view
from controller.mouse import Mouse
from scene.single_play import SinglePlay
from scene.single_play_lobby import SinglePlayLobby


class LobbyHost(SinglePlayLobby):
    def __init__(self):
        super().__init__()
        self.server = MultiPlayLobbyServer()
        self.process_connect = None
        self.parent_pipe, self.chile_pipe = multiprocessing.Pipe()

        self.game_start = False

        self.computers_attend_flag = [0,0,0,0,0]
        self.clients_attend_flag = [0,0,0,0,0]
        self.user_name = ['','','','','']

        self.image_player_joined = pygame.transform.scale(
            pygame.image.load("./resources/Image/lobby_images/user_enter.png"),
            (self.ui_size["logo"][0] * 0.5, self.ui_size["logo"][1] * 0.4))

        self.user_name_display = [self.small_font.render("User name : " + self.user_name[0], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[1], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[2], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[3], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[4], True, (0, 0, 0))]

        self.buttons_out = [Button(self.screen.get_width() * 0.1,
                                   self.screen.get_height() * 0.4,
                                   self.ui_size["button"][0],
                                   self.ui_size["button"][1],
                                   self.screen,
                                   0xffffff,
                                   'User1 강퇴',
                                   self.ui_size["font"][1],
                                   on_click_function=self.event_change_player_name),
                            Button(self.screen.get_width() * 0.3,
                                   self.screen.get_height() * 0.4,
                                   self.ui_size["button"][0],
                                   self.ui_size["button"][1],
                                   self.screen,
                                   0xffffff,
                                   'User2 강퇴',
                                   self.ui_size["font"][1],
                                   on_click_function=self.event_change_player_name),
                            Button(self.screen.get_width() * 0.5,
                                   self.screen.get_height() * 0.4,
                                   self.ui_size["button"][0],
                                   self.ui_size["button"][1],
                                   self.screen,
                                   0xffffff,
                                   'User3 강퇴',
                                   self.ui_size["font"][1],
                                   on_click_function=self.event_change_player_name),
                            Button(self.screen.get_width() * 0.7,
                                   self.screen.get_height() * 0.4,
                                   self.ui_size["button"][0],
                                   self.ui_size["button"][1],
                                   self.screen,
                                   0xffffff,
                                   'User4 강퇴',
                                   self.ui_size["font"][1],
                                   on_click_function=self.event_change_player_name),
                            Button(self.screen.get_width() * 0.9,
                                   self.screen.get_height() * 0.4,
                                   self.ui_size["button"][0],
                                   self.ui_size["button"][1],
                                   self.screen,
                                   0xffffff,
                                   'User5 강퇴',
                                   self.ui_size["font"][1],
                                   on_click_function=self.event_exit),]

    def event_join_computer_1(self):
        if not self.clients_attend_flag[0]:
            super().event_join_computer_1()
            self.parent_pipe.send(self.computers_attend_flag)
            self.parent_pipe.send(self.player_name.encode())

    def event_join_computer_2(self):
        if not self.clients_attend_flag[1]:
            super().event_join_computer_2()
            self.parent_pipe.send(self.computers_attend_flag)
            self.parent_pipe.send(self.player_name.encode())

    def event_join_computer_3(self):
        if not self.clients_attend_flag[2]:
            super().event_join_computer_3()
            self.parent_pipe.send(self.computers_attend_flag)
            self.parent_pipe.send(self.player_name.encode())

    def event_join_computer_4(self):
        if not self.clients_attend_flag[3]:
            super().event_join_computer_4()
            self.parent_pipe.send(self.computers_attend_flag)
            self.parent_pipe.send(self.player_name.encode())

    def event_join_computer_5(self):
        if not self.clients_attend_flag[4]:
            super().event_join_computer_5()
            self.parent_pipe.send(self.computers_attend_flag)
            self.parent_pipe.send(self.player_name.encode())

    def event_start(self):
        print("게임 시작")

    def event_exit(self):
        self.server.server_socket.close()
        self.process_connect.terminate()
        super().event_exit()

    def event_save_player_name(self):
        super().event_save_player_name()
        self.parent_pipe.send(self.computers_attend_flag)
        self.parent_pipe.send(self.player_name.encode())

    def draw(self):
        super().draw()
        for i, button in enumerate(self.buttons_computer):
            # 팝업 떠있을 경우 감지하지 않음
            if not self.popup.pop:
                button.detect_event()
            if self.clients_attend_flag[i]:
                self.screen.blit(self.image_player_joined, (button.x, button.y))
        for i, button in enumerate(self.buttons_out):
            if self.clients_attend_flag[i]:
                button.draw()
        self.user_name_display = [self.small_font.render("User name : " + self.user_name[0], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[1], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[2], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[3], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[4], True, (0, 0, 0))]
        for i, name in enumerate(self.user_name_display):
            if self.clients_attend_flag[i]:
                self.screen.blit(name, (self.screen.get_width() * 0.05 * (4 * i + 1), self.screen.get_height() * 0.3))

    def rev_flag(self):
        while self.running:
            self.clients_attend_flag = self.parent_pipe.recv()
            self.user_name = self.parent_pipe.recv()

    def run(self):
        self.process_connect = multiprocessing.Process(target=self.server.connect, args=(self.chile_pipe,))
        self.process_connect.start()
        self.parent_pipe.send(self.computers_attend_flag)
        self.parent_pipe.send(self.player_name.encode())
        threading.Thread(target=self.rev_flag).start()
        super().run()


class MultiPlayLobbyServer:
    def __init__(self):
        self.server_ip = '127.0.0.1'  # 서버 IP 주소 설정 (이 경우 로컬 IP)
        self.server_port = 10613  # 포트 번호 설정

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(5)

        self.clients = []
        self.clients_attend_flag = [0,0,0,0,0]
        self.computers_attend_flag = [0,0,0,0,0]
        self.user_name = ['','','','','']
        self.player_name = "You"

        self.running = True
        self.game_start = False

    def client_handler(self, client_socket, addr, pipe):
        self.clients_attend_flag[len(self.clients)] = 1
        self.clients.append(client_socket)
        try:
            while self.running:
                data = client_socket.recv(1024)
                self.user_name[self.clients.index(client_socket)] = data.decode()
                client_socket.sendall(pickle.dumps(self.player_name))
                client_socket.sendall(pickle.dumps(self.clients_attend_flag))
                client_socket.sendall(pickle.dumps(self.computers_attend_flag))
                client_socket.sendall(pickle.dumps(self.user_name))
                pipe.send(self.clients_attend_flag)
                pipe.send(self.user_name)
        except:
            print(f"Client {addr} disconnected")
        finally:
            print("finally")
            del self.user_name[self.clients.index(client_socket)]
            self.user_name.append('')
            self.clients.remove(client_socket)
            self.clients_attend_flag[len(self.clients)] = 0
            for client in self.clients:
                client.sendall(self.player_name.encode())
                client.sendall(pickle.dumps(self.clients_attend_flag))
                client.sendall(pickle.dumps(self.computers_attend_flag))
                client.sendall(pickle.dumps(self.user_name))
            pipe.send(self.clients_attend_flag)
            pipe.send(self.user_name)
            client_socket.close()

    def rev_flag(self, pipe):
        while self.running:
            self.computers_attend_flag = pipe.recv()
            self.player_name = pipe.recv()

    def connect(self, pipe):
        try:
            while True:
                print("Waiting for clients...")
                client_socket, addr = self.server_socket.accept()
                print(f"Client {addr} connected")

                thread = threading.Thread(target=self.client_handler, args=(client_socket, addr, pipe))
                thread.start()
                threading.Thread(target=self.rev_flag, args=(pipe,))
                pipe.send(self.clients_attend_flag)
                pipe.send(self.user_name)
        except:
            self.running = False
            self.server_socket.close()


if __name__=='__main__':
    multiprocessing.freeze_support()
    lobby_server = LobbyHost()
    lobby_server.run()
