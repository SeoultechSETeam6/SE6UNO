import socket
import threading
import pygame
import pickle

from ui.button import Button, ImageButton
from controller import game_view
from controller.mouse import Mouse
from scene.single_play import SinglePlay
from scene.single_play_lobby import SinglePlayLobby


class LobbyClient(SinglePlayLobby):
    def __init__(self, ip):
        super().__init__()
        self.server_ip = ip  # 서버 IP 주소 설정 (이 경우 로컬 IP)
        self.server_port = 10613  # 포트 번호 설정

        # 소켓 객체 생성 (TCP)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.game_start = False

        self.clients_attend_flag = [0,0,0,0,0]
        self.computers_attend_flag = [0, 0, 0, 0, 0]
        self.user_name = ['','','','','']
        self.player_name = "You"
        self.user_name_display = [self.small_font.render("User name : " + self.user_name[0], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[1], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[2], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[3], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[4], True, (0, 0, 0))]

        self.image_player_joined = pygame.transform.scale(
            pygame.image.load("./resources/Image/lobby_images/user_enter.png"),
            (self.ui_size["logo"][0] * 0.5, self.ui_size["logo"][1] * 0.4))

    def recv_data(self):
        while self.running:
            self.player_name = pickle.loads(self.client_socket.recv(1024))
            self.clients_attend_flag = pickle.loads(self.client_socket.recv(1024))
            self.computers_attend_flag = pickle.loads(self.client_socket.recv(1024))
            self.user_name = pickle.loads(self.client_socket.recv(1024))


    def connect(self):
        try:
            # 서버에 연결
            self.client_socket.connect((self.server_ip, self.server_port))
            print('>> Connect Server')
            thread = threading.Thread(target=self.recv_data)
            thread.start()
            self.client_socket.sendall(self.player_name.encode())
            self.run()
        except:
            print(">> Can't Connect Server")
            self.client_socket.close()
            self.running = False

    def event_save_player_name(self):
        super().event_save_player_name()
        self.client_socket.sendall(self.player_name.encode())

    def event_join_computer_1(self):
        pass

    def event_join_computer_2(self):
        pass

    def event_join_computer_3(self):
        pass

    def event_join_computer_4(self):
        pass

    def event_join_computer_5(self):
        pass

    def event_exit(self):
        super().event_exit()
        self.client_socket.close()

    def draw(self):
        self.screen.fill((100, 100, 100))
        # 컴퓨터 플레이어 버튼 그림
        for i, button in enumerate(self.buttons_computer):
            button.draw()
            # 팝업 떠있을 경우 감지하지 않음
            if not self.popup.pop:
                button.detect_event()
            if self.clients_attend_flag[i]:
                self.screen.blit(self.image_player_joined, (button.x, button.y))
            if self.computers_attend_flag[i]:
                if self.computers_logic[i] == "basic":
                    self.screen.blit(self.image_joined, (button.x, button.y))
                elif self.computers_logic[i] == "A":
                    self.screen.blit(self.image_A_joined, (button.x, button.y))
                elif self.computers_logic[i] == "B":
                    self.screen.blit(self.image_B_joined, (button.x, button.y))
                elif self.computers_logic[i] == "C":
                    self.screen.blit(self.image_C_joined, (button.x, button.y))
                elif self.computers_logic[i] == "D":
                    self.screen.blit(self.image_D_joined, (button.x, button.y))

        self.user_name_display = [self.small_font.render("User name : " + self.user_name[0], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[1], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[2], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[3], True, (0, 0, 0)),
                                  self.small_font.render("User name : " + self.user_name[4], True, (0, 0, 0))]

        for i, name in enumerate(self.user_name_display):
            if self.clients_attend_flag[i]:
                self.screen.blit(name, (self.screen.get_width() * 0.05 * (4 * i + 1), self.screen.get_height() * 0.3))

        # 플레이어 이름 변경 버튼 그리기
        self.button_change_player_name.draw()

        # 나가기 버튼 그리기
        self.button_exit.draw()

        # 이름 변경 팝업이 열렸을 경우 버튼 클릭 방지
        if not self.popup.pop:
            self.button_change_player_name.detect_event()
            if self.computers_attend_count > 0:
                self.button_start.detect_event()
            self.button_exit.detect_event()
        else:
            self.popup.open()
            temp_name_display = self.small_font.render("변경할 이름: " + self.player_name_temp, True, (0, 0, 0))
            self.screen.blit(temp_name_display, (self.screen.get_width() // 2.4, self.screen.get_height() // 2))

        self.name_display = self.font.render("User name: " + self.player_name, True, (0, 0, 0))
        self.screen.blit(self.name_display, (self.screen.get_width() * 0.02, self.screen.get_height() * 0.92))

        self.screen.blit(self.buttons[self.selected_button_vertical_index]
                         [self.selected_button_horizon_index].selected_image,
                         (self.buttons[self.selected_button_vertical_index][
                              self.selected_button_horizon_index].rect.x,
                          self.buttons[self.selected_button_vertical_index][
                              self.selected_button_horizon_index].rect.y - self.ui_size["font"][1]))
