import pygame

from controller import game_data, game_view
from controller.mouse import Mouse
from ui.button import Button
from ui.popup import Popup
from multi_play_lobby_host import LobbyHost
from multi_play_lobby_client import LobbyClient


class SelectMode:
    def __init__(self):
        # 게임 설정 불러오기
        self.settings_data = game_data.load_settings()

        # pygame 초기화
        pygame.init()
        pygame.display.set_caption(game_view.GAME_TITLE + ": Multiple Play")
        self.ui_size = game_view.set_size(self.settings_data["resolution"]["width"])
        self.screen = pygame.display.set_mode((self.settings_data["resolution"]["width"],
                                               self.settings_data["resolution"]["height"]))
        self.clock = pygame.time.Clock()
        self.running = True

        # 글꼴 설정
        self.font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][0])
        self.small_font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][1])

        # 버튼 설정
        self.buttons = [
            Button(self.screen.get_width() * 0.07,
                   self.screen.get_height() * 0.06,
                   self.ui_size["button"][0],
                   self.ui_size["button"][1],
                   self.screen,
                   0xffffff,
                   '나가기',
                   self.ui_size["font"][1],
                   on_click_function=self.event_exit),
            Button(self.screen.get_width() * 0.3,
                   self.screen.get_height() // 2,
                   self.ui_size["button"][0] * 1.5,
                   self.ui_size["button"][0] * 1.5,
                   self.screen,
                   0xffffff,
                   '방 만들기',
                   self.ui_size["font"][0],
                   on_click_function=self.event_create_server),
            Button(self.screen.get_width() * 0.6,
                   self.screen.get_height() // 2,
                   self.ui_size["button"][0] * 1.5,
                   self.ui_size["button"][0] * 1.5,
                   self.screen,
                   0xffffff,
                   '방 들어가기',
                   self.ui_size["font"][0],
                   on_click_function=self.event_popup_input_ip)
        ]

        # 팝업 설정
        self.popup = Popup(self.screen.get_width() // 2,
                           self.screen.get_height() // 2,
                           self.screen.get_width() * 0.4,
                           self.screen.get_height() * 0.4,
                           self.screen,
                           '들어갈 방의 IP를 입력하고 확인 버튼이나 Enter/Return 키를 눌러주세요.',
                           self.ui_size["font"][1],
                           self.event_join)
        self.ip = ""

        self.selected_button_index = 0

    def event_create_server(self):
        print("서버 만들기")
        LobbyHost().run()

    def event_join(self):
        if len(self.ip) > 0:
            print(self.ip + "로 접속")
        self.popup.pop = False
        LobbyClient(self.ip).connect()

    def event_popup_input_ip(self):
        self.ip = ""
        self.popup.pop = True

    # 게임 나가기 버튼 이벤트
    def event_exit(self):
        self.running = False

    def draw(self):
        self.screen.fill((20, 20, 20))

        for button in self.buttons:
            button.draw()
            if not self.popup.pop:
                button.detect_event()

        self.screen.blit(self.buttons[self.selected_button_index].selected_image,
                         (self.buttons[self.selected_button_index].rect.x,
                          self.buttons[self.selected_button_index].rect.y - self.ui_size["font"][1]))
        if self.popup.pop:
            self.popup.open()
            text = self.small_font.render("들어갈 방 주소: " + self.ip, True, (0, 0, 0))
            self.screen.blit(text, (self.screen.get_width() // 2.4, self.screen.get_height() // 2))

        # 매 프레임마다 화면 업데이트
        pygame.display.flip()

    def run(self):
        # 메인 화면 표시
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.popup.pop:
                    if event.type == pygame.KEYDOWN:
                        # 백스페이스 누르면 한 글자 씩 지움
                        if event.key == pygame.K_BACKSPACE:
                            if len(self.ip) > 0:
                                self.ip = self.ip[0:len(self.ip) - 1]
                            else:
                                pass
                        # 엔터 누르면 닉네임 변경 저장
                        elif event.key == pygame.K_RETURN:
                            if len(self.ip) > 0:
                                self.event_join()
                            else:
                                self.popup.pop = False
                        else:
                            self.ip = self.ip + pygame.key.name(event.key)
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == self.settings_data["key"]['left']:
                            self.buttons[self.selected_button_index].keyboard_selected = False
                            self.selected_button_index = (self.selected_button_index - 1) % len(self.buttons)
                            self.buttons[self.selected_button_index].keyboard_selected = True
                        elif event.key == self.settings_data["key"]['right']:
                            self.buttons[self.selected_button_index].keyboard_selected = False
                            self.selected_button_index = (self.selected_button_index + 1) % len(self.buttons)
                            self.buttons[self.selected_button_index].keyboard_selected = True
                        elif event.key == self.settings_data["key"]['enter']:
                            self.buttons[self.selected_button_index].on_click_function()

            Mouse.updateMouseState()
            self.clock.tick(game_view.FPS)
            self.draw()
