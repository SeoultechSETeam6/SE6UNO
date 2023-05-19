import pygame
import math

from controller import game_data, game_view
from controller.mouse import Mouse
from ui.button import Button, ImageButton
from ui.popup import Popup

from scene.single_play import SinglePlay


class SinglePlayLobby:
    def __init__(self):
        # 게임 설정 불러오기
        self.selected_button_vertical_index = 0
        self.selected_button_horizon_index = 0
        self.settings_data = game_data.load_settings()

        # pygame 초기화
        pygame.init()
        pygame.display.set_caption(game_view.GAME_TITLE + ": Single Play Lobby")
        self.ui_size = game_view.set_size(self.settings_data["resolution"]["width"])
        self.screen = pygame.display.set_mode((self.settings_data["resolution"]["width"],
                                               self.settings_data["resolution"]["height"]))
        self.clock = pygame.time.Clock()
        self.running = True

        # 글꼴 설정
        self.font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][0])
        self.small_font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][1])

        # 컴퓨터 추가 버튼
        self.buttons_computer = [ImageButton(self.screen.get_width() * 0.1,
                                             self.screen.get_height() * 0.1,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/computer1.png",
                                             on_click_function=self.event_join_computer_1),
                                 ImageButton(self.screen.get_width() * 0.3,
                                             self.screen.get_height() * 0.1,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/computer2.png",
                                             on_click_function=self.event_join_computer_2),
                                 ImageButton(self.screen.get_width() * 0.5,
                                             self.screen.get_height() * 0.1,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/computer3.png",
                                             on_click_function=self.event_join_computer_3),
                                 ImageButton(self.screen.get_width() * 0.7,
                                             self.screen.get_height() * 0.1,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/computer4.png",
                                             on_click_function=self.event_join_computer_4),
                                 ImageButton(self.screen.get_width() * 0.9,
                                             self.screen.get_height() * 0.1,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/computer5.png",
                                             on_click_function=self.event_join_computer_5)]

        self.buttons_rule = [ImageButton(self.screen.get_width() * 0.3,
                                         self.screen.get_height() * 0.5,
                                         self.screen.get_width() // 6,
                                         self.screen.get_height() // 6,
                                         self.screen,
                                         "./resources/Image/lobby_images/computer1.png",
                                         on_click_function=self.event_rule_b),
                             ImageButton(self.screen.get_width() * 0.5,
                                         self.screen.get_height() * 0.5,
                                         self.screen.get_width() // 6,
                                         self.screen.get_height() // 6,
                                         self.screen,
                                         "./resources/Image/lobby_images/computer2.png",
                                         on_click_function=self.event_rule_c),
                             ImageButton(self.screen.get_width() * 0.7,
                                         self.screen.get_height() * 0.5,
                                         self.screen.get_width() // 6,
                                         self.screen.get_height() // 6,
                                         self.screen,
                                         "./resources/Image/lobby_images/computer3.png",
                                         on_click_function=self.event_rule_d)]

        # 시작 버튼
        self.button_start = ImageButton(self.screen.get_width() // 2,
                                        self.screen.get_height() * 0.85,
                                        self.screen.get_width() // 4,
                                        self.screen.get_height() // 4,
                                        self.screen,
                                        "./resources/Image/lobby_images/game_start.png",
                                        on_click_function=self.event_start)

        # 이름 변경 버튼
        self.button_change_player_name = Button(self.screen.get_width() * 0.25,
                                                self.screen.get_height() * 0.85,
                                                self.ui_size["button"][0],
                                                self.ui_size["button"][1],
                                                self.screen,
                                                0xffffff,
                                                'User 이름 변경',
                                                self.ui_size["font"][1],
                                                on_click_function=self.event_change_player_name)

        # 나가기 버튼
        self.button_exit = Button(self.screen.get_width() * 0.75,
                                  self.screen.get_height() * 0.85,
                                  self.ui_size["button"][0],
                                  self.ui_size["button"][1],
                                  self.screen,
                                  0xffffff,
                                  '나가기',
                                  self.ui_size["font"][1],
                                  on_click_function=self.event_exit)

        # 버튼 리스트 초기값
        self.buttons = [self.buttons_computer, self.buttons_rule, [self.button_change_player_name, self.button_exit]]
        self.buttons[self.selected_button_vertical_index][self.selected_button_horizon_index] \
            .keyboard_selected = True

        # 컴퓨터 플레이어 추가완료 이미지
        self.image_joined = pygame.transform.scale(
            pygame.image.load("./resources/Image/lobby_images/computer_enter.png"),
            (self.ui_size["logo"][0] * 0.5, self.ui_size["logo"][1] * 0.4))
        self.image_A_joined = pygame.transform.scale(
            pygame.image.load("./resources/Image/lobby_images/computer_enter_A.png"),
            (self.ui_size["logo"][0] * 0.5, self.ui_size["logo"][1] * 0.4))
        self.image_B_joined = pygame.transform.scale(
            pygame.image.load("./resources/Image/lobby_images/computer_enter_B.png"),
            (self.ui_size["logo"][0] * 0.5, self.ui_size["logo"][1] * 0.4))
        self.image_C_joined = pygame.transform.scale(
            pygame.image.load("./resources/Image/lobby_images/computer_enter_C.png"),
            (self.ui_size["logo"][0] * 0.5, self.ui_size["logo"][1] * 0.4))
        self.image_D_joined = pygame.transform.scale(
            pygame.image.load("./resources/Image/lobby_images/computer_enter_D.png"),
            (self.ui_size["logo"][0] * 0.5, self.ui_size["logo"][1] * 0.4))

        # 이름 설정 기본 값
        self.player_name = "You"
        self.player_name_temp = ""
        self.name_display = self.font.render("Player name : " + self.player_name, True, (0, 0, 0))

        # 컴퓨터 참여 정보 리스트 및 로직 리스트
        self.computers_attend_flag = [False, False, False, False, False]
        self.computers_logic = ["None", "None", "None", "None", "None"]
        self.game_rule = [None, None, None]
        self.computers_attend_count = 0

        # 이름 변경 팝업창
        self.popup = Popup(self.screen.get_width() // 2,
                           self.screen.get_height() // 2,
                           self.screen.get_width() * 0.4,
                           self.screen.get_height() * 0.4,
                           self.screen,
                           '바꿀 이름을 입력하고 확인 버튼이나 Enter/Return 키를 눌러주세요.',
                           self.ui_size["font"][1],
                           self.event_save_player_name)

    # 플레이어 이름 변경 버튼 이벤트
    def event_change_player_name(self):
        self.player_name_temp = ""
        self.popup.pop = True

    def computer_status(self, index):
        if self.computers_logic[index] == "D":
            self.computers_attend_flag[index] = False
            self.computers_logic[index] = "None"
        elif self.computers_logic[index] == "None":
            self.computers_attend_flag[index] = True
            self.computers_logic[index] = "basic"
        elif self.computers_logic[index] == "basic":
            self.computers_attend_flag[index] = True
            self.computers_logic[index] = "A"
        elif self.computers_logic[index] == "A":
            self.computers_attend_flag[index] = True
            self.computers_logic[index] = "B"
        elif self.computers_logic[index] == "B":
            self.computers_attend_flag[index] = True
            self.computers_logic[index] = "C"
        elif self.computers_logic[index] == "C":
            self.computers_attend_flag[index] = True
            self.computers_logic[index] = "D"
        self.check_computer_attend()

    # 컴퓨터 플레이어 클릭 시 참여 플래그 토글 이벤트
    def event_join_computer_1(self):
        self.computer_status(0)

    def event_join_computer_2(self):
        self.computer_status(1)

    def event_join_computer_3(self):
        self.computer_status(2)

    def event_join_computer_4(self):
        self.computer_status(3)

    def event_join_computer_5(self):
        self.computer_status(4)

    def event_rule_b(self):
        if self.game_rule[0] is None:
            self.game_rule[0] = "B"
            print(self.game_rule)
        elif self.game_rule[0] == "B":
            self.game_rule[0] = None
            print(self.game_rule)

    def event_rule_c(self):
        if self.game_rule[1] is None:
            self.game_rule[1] = "C"
            print(self.game_rule)
        elif self.game_rule[1] == "C":
            self.game_rule[1] = None
            print(self.game_rule)

    def event_rule_d(self):
        if self.game_rule[2] is None:
            self.game_rule[2] = "D"
            print(self.game_rule)
        elif self.game_rule[2] == "D":
            self.game_rule[2] = None
            print(self.game_rule)

    def check_computer_attend(self):
        self.computers_attend_count = 0
        for i in self.computers_attend_flag:
            if i is True:
                self.computers_attend_count = self.computers_attend_count + 1

    # 컴퓨터가 하나 이상 참가해야지, 버튼 리스트에 게임 스타트 버튼이 추가된다.
    def keyboard_detect_start_button(self):
        # 버튼 리스트
        if self.computers_attend_count == 0:
            self.buttons = [self.buttons_computer, self.buttons_rule, [self.button_change_player_name, self.button_exit]]
        elif self.computers_attend_count > 0:
            self.buttons = [self.buttons_computer, self.buttons_rule,
                            [self.button_change_player_name, self.button_start, self.button_exit]]

    # 플레이어 이름 변경 팝업창에서 확인 클릭 시 이벤트
    def event_save_player_name(self):
        print('플레이어 이름 변경 확인 버튼 클릭됨')
        if len(self.player_name_temp) > 0:
            self.player_name = self.player_name_temp
        self.popup.pop = False

    # 게임 시작 버튼 이벤트
    def event_start(self):
        print("게임 시작")
        # 로직이 current_player와 잘 연동되기 위해, 로직에서 None을 제거.
        self.computers_logic = [logic for logic in self.computers_logic if logic != "None"]
        print("컴퓨터 로직: ", self.computers_logic)
        print(self.computers_attend_flag, self.computers_attend_count)
        self.running = False
        SinglePlay(self.computers_attend_flag, self.player_name, self.computers_logic).run()

    # 게임 나가기 버튼 이벤트
    def event_exit(self):
        self.running = False

    def draw(self):
        self.screen.fill((100, 100, 100))

        # 컴퓨터 플레이어 버튼 그림
        for i, button in enumerate(self.buttons_computer):
            button.draw()
            # 팝업 떠있을 경우 감지하지 않음
            if not self.popup.pop:
                button.detect_event()
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

        # 게임 룰 버튼 그림
        for i, button in enumerate(self.buttons_rule):
            button.draw()
            # 팔업이 떠있을 경우 감지하지 않음
            if not self.popup.pop:
                button.detect_event()
            if self.game_rule[i] == "B":
                self.screen.blit(self.image_joined, (button.x, button.y))
            elif self.game_rule[i] == "C":
                self.screen.blit(self.image_joined, (button.x, button.y))
            elif self.game_rule[i] == "D":
                self.screen.blit(self.image_joined, (button.x, button.y))

        # 플레이어 이름 변경 버튼 그리기
        self.button_change_player_name.draw()

        # 게임 시작 버튼 그리기
        if self.computers_attend_count > 0:
            self.button_start.draw()

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

        pygame.display.flip()

    def detect_key_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.popup.pop:
                if event.type == pygame.KEYDOWN:
                    # 백스페이스 누르면 한 글자 씩 지움
                    if event.key == pygame.K_BACKSPACE:
                        self.player_name_temp = self.player_name_temp[0:len(self.player_name_temp) - 1]
                    # 엔터 누르면 닉네임 변경 저장
                    elif event.key == pygame.K_RETURN:
                        self.event_save_player_name()
                    else:
                        self.player_name_temp = self.player_name_temp + pygame.key.name(event.key)
            elif self.popup.pop is False:
                if event.type == pygame.KEYDOWN:
                    if event.key == self.settings_data["key"]['up']:
                        self.buttons[self.selected_button_vertical_index][
                            self.selected_button_horizon_index].keyboard_selected = False
                        # 위 키보드로 이동 시, 자연스러운 이동을 위한 코드, 버튼의 열을 보정한다.
                        if self.selected_button_vertical_index == 0 and self.selected_button_horizon_index in [0, 1]:
                            self.selected_button_horizon_index = 0
                        elif self.selected_button_vertical_index == 0 and self.selected_button_horizon_index == 2:
                            self.selected_button_horizon_index = 1
                        elif self.selected_button_vertical_index == 0 and self.selected_button_horizon_index in [3, 4]:
                            self.selected_button_horizon_index = 2
                        elif self.selected_button_vertical_index == 1:
                            self.selected_button_horizon_index = self.selected_button_horizon_index + 1
                        self.selected_button_vertical_index = (self.selected_button_vertical_index - 1) % len(
                            self.buttons)
                        # 행간 이동
                        if len(self.buttons[self.selected_button_vertical_index]) == self.selected_button_horizon_index:
                            self.selected_button_horizon_index = self.selected_button_horizon_index - 1
                        self.buttons[self.selected_button_vertical_index][
                            self.selected_button_horizon_index].keyboard_selected = True
                    elif event.key == self.settings_data["key"]['down']:
                        self.buttons[self.selected_button_vertical_index][
                            self.selected_button_horizon_index].keyboard_selected = False
                        # 위 키보드로 이동 시, 자연스러운 이동을 위한 코드, 버튼의 열을 보정한다.
                        if self.selected_button_vertical_index == 0 and self.selected_button_horizon_index in [0, 1]:
                            self.selected_button_horizon_index = 0
                        elif self.selected_button_vertical_index == 0 and self.selected_button_horizon_index == 2:
                            self.selected_button_horizon_index = 1
                        elif self.selected_button_vertical_index == 0 and self.selected_button_horizon_index in [3, 4]:
                            self.selected_button_horizon_index = 2
                        # 유저 이름 변경, 스타트, 나가기에서 computer_attend 버튼으로 이동시 보정
                        elif self.selected_button_vertical_index == 2:
                            if len(self.buttons[self.selected_button_vertical_index]) == 2:
                                if self.selected_button_horizon_index == 0:
                                    self.selected_button_horizon_index = self.selected_button_horizon_index + 1
                                elif self.selected_button_horizon_index == 1:
                                    self.selected_button_horizon_index = self.selected_button_horizon_index + 2
                            elif len(self.buttons[self.selected_button_vertical_index]) == 3:
                                self.selected_button_horizon_index = self.selected_button_horizon_index + 1
                        self.selected_button_vertical_index = (self.selected_button_vertical_index + 1) % len(
                            self.buttons)
                        if len(self.buttons[self.selected_button_vertical_index]) == self.selected_button_horizon_index:
                            self.selected_button_horizon_index = self.selected_button_horizon_index - 1
                        self.buttons[self.selected_button_vertical_index][
                            self.selected_button_horizon_index].keyboard_selected = True
                    elif event.key == self.settings_data["key"]['left']:
                        self.buttons[self.selected_button_vertical_index][
                            self.selected_button_horizon_index].keyboard_selected = False
                        self.selected_button_horizon_index = (self.selected_button_horizon_index - 1) % len(
                            self.buttons[self.selected_button_vertical_index])
                        self.buttons[self.selected_button_vertical_index][
                            self.selected_button_horizon_index].keyboard_selected = True
                    elif event.key == self.settings_data["key"]['right']:
                        self.buttons[self.selected_button_vertical_index][
                            self.selected_button_horizon_index].keyboard_selected = False
                        self.selected_button_horizon_index = (self.selected_button_horizon_index + 1) % len(
                            self.buttons[self.selected_button_vertical_index])
                        self.buttons[self.selected_button_vertical_index][
                            self.selected_button_horizon_index].keyboard_selected = True
                    elif event.key == self.settings_data["key"]['enter']:
                        self.buttons[self.selected_button_vertical_index][
                            self.selected_button_horizon_index].on_click_function()

    def run(self):
        while self.running:
            self.detect_key_event()
            Mouse.updateMouseState()
            self.clock.tick(game_view.FPS)
            self.keyboard_detect_start_button()
            self.draw()
