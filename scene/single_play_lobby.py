import pygame

from controller import game_data, game_view
from controller.mouse import Mouse
from ui.button import Button, ImageButton
from ui.popup import Popup

from scene.single_play import SinglePlay


class SinglePlayLobby:
    def __init__(self):
        # 게임 설정 불러오기
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
        self.buttons_computer = [ImageButton(self.screen.get_width() * 0.9,
                                             self.screen.get_height() * 0.1,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/computer1.png",
                                             on_click_function=self.event_join_computer_1),
                                 ImageButton(self.screen.get_width() * 0.9,
                                             self.screen.get_height() * 0.3,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/computer2.png",
                                             on_click_function=self.event_join_computer_2),
                                 ImageButton(self.screen.get_width() * 0.9,
                                             self.screen.get_height() * 0.5,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/computer3.png",
                                             on_click_function=self.event_join_computer_3),
                                 ImageButton(self.screen.get_width() * 0.9,
                                             self.screen.get_height() * 0.7,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/computer4.png",
                                             on_click_function=self.event_join_computer_4),
                                 ImageButton(self.screen.get_width() * 0.9,
                                             self.screen.get_height() * 0.9,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/computer5.png",
                                             on_click_function=self.event_join_computer_5)]

        # 시작 버튼
        self.button_start = ImageButton(self.screen.get_width() // 2,
                                        self.screen.get_height() // 2,
                                        self.screen.get_width() // 4,
                                        self.screen.get_height() // 4,
                                        self.screen,
                                        "./resources/Image/lobby_images/game_start.png",
                                        on_click_function=self.event_start)

        # 이름 변경 버튼
        self.button_change_player_name = Button(self.screen.get_width() * 0.07,
                                                self.screen.get_height() * 0.87,
                                                self.ui_size["button"][0],
                                                self.ui_size["button"][1],
                                                self.screen,
                                                0xffffff,
                                                'User 이름 변경',
                                                self.ui_size["font"][1],
                                                on_click_function=self.event_change_player_name)

        # 이름 변경 버튼
        self.button_exit = Button(self.screen.get_width() * 0.07,
                                  self.screen.get_height() * 0.07,
                                  self.ui_size["button"][0],
                                  self.ui_size["button"][1],
                                  self.screen,
                                  0xffffff,
                                  '나가기',
                                  self.ui_size["font"][1],
                                  on_click_function=self.event_exit)

        # 컴퓨터 플레이어 추가완료 이미지
        self.image_joined = pygame.transform.scale(
            pygame.image.load("./resources/Image/lobby_images/computer_enter.png"),
            (self.ui_size["logo"][0] * 0.5, self.ui_size["logo"][1] * 0.4))

        # 이름 설정 기본 값
        self.player_name = "You"
        self.player_name_temp = ""
        self.name_display = self.font.render("Player name : " + self.player_name, True, (0, 0, 0))

        # 컴퓨터 참여 정보 리스트
        self.computers_attend_flag = [False, False, False, False, False]
        self.computers_attend_count = 0

        # 이름 변경 팝업창
        self.popup = Popup(self.screen.get_width() // 2,
                           self.screen.get_height() // 2,
                           self.screen.get_width() * 0.4,
                           self.screen.get_height() * 0.4,
                           self.screen,
                           '바꿀 이름을 입력하고 확인 버튼을 눌러주세요.',
                           self.ui_size["font"][1],
                           self.event_save_player_name)

    # 플레이어 이름 변경 버튼 이벤트
    def event_change_player_name(self):
        self.player_name_temp = ""
        self.popup.pop = True

    # 컴퓨터 플레이어 클릭 시 참여 플래그 토글 이벤트
    def event_join_computer_1(self):
        if self.computers_attend_flag[0]:
            self.computers_attend_flag[0] = False
            self.computers_attend_count -= 1
        else:
            self.computers_attend_flag[0] = True
            self.computers_attend_count += 1

    def event_join_computer_2(self):
        if self.computers_attend_flag[1]:
            self.computers_attend_flag[1] = False
            self.computers_attend_count -= 1
        else:
            self.computers_attend_flag[1] = True
            self.computers_attend_count += 1

    def event_join_computer_3(self):
        if self.computers_attend_flag[2]:
            self.computers_attend_flag[2] = False
            self.computers_attend_count -= 1
        else:
            self.computers_attend_flag[2] = True
            self.computers_attend_count += 1

    def event_join_computer_4(self):
        if self.computers_attend_flag[3]:
            self.computers_attend_flag[3] = False
            self.computers_attend_count -= 1
        else:
            self.computers_attend_flag[3] = True
            self.computers_attend_count += 1

    def event_join_computer_5(self):
        if self.computers_attend_flag[4]:
            self.computers_attend_flag[4] = False
            self.computers_attend_count -= 1
        else:
            self.computers_attend_flag[4] = True
            self.computers_attend_count += 1

    # 플레이어 이름 변경 팝업창에서 확인 클릭 시 이벤트
    def event_save_player_name(self):
        print('플레이어 이름 변경 확인 버튼 클릭됨')
        if len(self.player_name_temp) > 0:
            self.player_name = self.player_name_temp
        self.popup.pop = False

    # 게임 시작 버튼 이벤트
    def event_start(self):
        print("게임 시작")
        SinglePlay(self.computers_attend_flag, self.player_name).run()
        self.running = False

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

        pygame.display.flip()

    def run(self):
        while self.running:
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

            Mouse.updateMouseState()
            self.clock.tick(game_view.FPS)
            self.draw()
