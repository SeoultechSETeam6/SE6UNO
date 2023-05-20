import pygame
import sys

from controller import game_data, game_view
from controller.mouse import Mouse
from scene.multiple_play_select_mode import SelectMode
from ui.button import Button

from scene.single_play_lobby import SinglePlayLobby
from scene.story_mode_map import StoryModeMap
from scene.settings import Settings
from scene.achievement import Achievement


class Main:
    def __init__(self):
        # 게임 설정 불러오기
        self.settings_data = game_data.load_settings()

        # pygame 초기화
        pygame.init()
        pygame.display.set_caption(game_view.GAME_TITLE)
        self.ui_size = game_view.set_size(self.settings_data["resolution"]["width"])
        self.screen = pygame.display.set_mode((self.settings_data["resolution"]["width"],
                                               self.settings_data["resolution"]["height"]))
        self.clock = pygame.time.Clock()
        self.running = True

        # 글꼴 설정
        self.font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][1])

        # 로고 표시
        self.logo = pygame.image.load("./resources/Image/logo.png")
        self.logo = pygame.transform.scale(self.logo, self.ui_size["logo"])
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = ((self.screen.get_width() // 2), self.logo_rect.height // 2)

        # 음악
        self.music = pygame.mixer.Sound("./resources/Music/main.ogg")
        self.music.set_volume(self.settings_data["volume"]["sound"] * self.settings_data["volume"]["background"])
        self.music.play(-1)

        # 현재 조작 키 표시
        self.key_setting_up = self.font.render("UP: " + pygame.key.name(self.settings_data["key"]['up']), True, (255, 255, 255))
        self.key_setting_down = self.font.render("DOWN: " + pygame.key.name(self.settings_data["key"]['down']), True, (255, 255, 255))
        self.key_setting_enter = self.font.render("Enter: " + pygame.key.name(self.settings_data["key"]['enter']), True, (255, 255, 255))
        self.screen.get_height()

        # 버튼
        self.buttons = [
            Button(self.screen.get_width() // 2,
                   self.screen.get_height() // 2 * 0.92,
                   self.ui_size["button"][0],
                   self.ui_size["button"][1],
                   self.screen,
                   0xffffff,
                   '스토리 모드',
                   self.ui_size["font"][1],
                   on_click_function=self.event_story_mode),
            Button(self.screen.get_width() // 2,
                   self.screen.get_height() // 2 * 1.1,
                   self.ui_size["button"][0],
                   self.ui_size["button"][1],
                   self.screen,
                   0xffffff,
                   '싱글 플레이',
                   self.ui_size["font"][1],
                   on_click_function=self.event_single_play_mode),
            Button(self.screen.get_width() // 2,
                   self.screen.get_height() // 2 * 1.28,
                   self.ui_size["button"][0],
                   self.ui_size["button"][1],
                   self.screen,
                   0xffffff,
                   '멀티 플레이',
                   self.ui_size["font"][1],
                   on_click_function=self.event_multiple_play_mode),
            Button(self.screen.get_width() // 2,
                   self.screen.get_height() // 2 * 1.46,
                   self.ui_size["button"][0],
                   self.ui_size["button"][1],
                   self.screen,
                   0xffffff,
                   '업적',
                   self.ui_size["font"][1],
                   on_click_function=self.event_achievement),
            Button(self.screen.get_width() // 2,
                   self.screen.get_height() // 2 * 1.64,
                   self.ui_size["button"][0],
                   self.ui_size["button"][1],
                   self.screen,
                   0xffffff,
                   '설정',
                   self.ui_size["font"][1],
                   on_click_function=self.event_settings),
            Button(self.screen.get_width() // 2,
                   self.screen.get_height() // 2 * 1.82,
                   self.ui_size["button"][0],
                   self.ui_size["button"][1],
                   self.screen,
                   0xffffff,
                   '나가기',
                   self.ui_size["font"][1],
                   on_click_function=self.event_quit)
        ]

        self.selected_button_index = 0
        self.buttons[self.selected_button_index].keyboard_selected = True

    def event_story_mode(self):
        self.music.stop()
        print('스토리 모드 버튼 클릭됨')
        flag = True
        while flag:
            flag = StoryModeMap().run()

    def event_single_play_mode(self):
        self.music.stop()
        print('싱글 플레이 버튼 클릭됨')
        SinglePlayLobby().run()

    def event_multiple_play_mode(self):
        self.music.stop()
        print('멀티 플레이 버튼 클릭됨')
        SelectMode().run()

    def event_achievement(self):
        self.music.stop()
        print('업적 버튼 클릭됨')
        Achievement().run()

    def event_settings(self):
        self.music.stop()
        print('설정 버튼 클릭됨')
        Settings().run()
        if game_view.resolution_changed:
            self.running = False

    def event_quit(self):
        print('나가기 버튼 클릭됨')
        self.running = False

    def draw(self):
        # 배경 색상
        self.screen.fill((20, 20, 20))

        # 버튼 조작 키 업데이트
        self.screen.blit(self.key_setting_up, (50, self.screen.get_height() // 30 * 26))
        self.screen.blit(self.key_setting_down, (50, self.screen.get_height() // 30 * 27))
        self.screen.blit(self.key_setting_enter, (50, self.screen.get_height() // 30 * 28))
        self.screen.blit(self.logo, self.logo_rect)
        for button in self.buttons:
            button.draw()
            button.detect_event()
        self.screen.blit(self.buttons[self.selected_button_index].selected_image,
                         (self.buttons[self.selected_button_index].rect.x, self.buttons[self.selected_button_index].rect.y - self.ui_size["font"][1]))
        # 매 프레임마다 화면 업데이트
        pygame.display.flip()

    # 키 입력 감지
    def detect_key_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == self.settings_data["key"]['up']:
                    self.buttons[self.selected_button_index].keyboard_selected = False
                    self.selected_button_index = (self.selected_button_index - 1) % len(self.buttons)
                    self.buttons[self.selected_button_index].keyboard_selected = True
                elif event.key == self.settings_data["key"]['down']:
                    self.buttons[self.selected_button_index].keyboard_selected = False
                    self.selected_button_index = (self.selected_button_index + 1) % len(self.buttons)
                    self.buttons[self.selected_button_index].keyboard_selected = True
                elif event.key == self.settings_data["key"]['enter']:
                    self.buttons[self.selected_button_index].on_click_function()

    def run(self):
        # 메인 화면 표시
        while self.running:
            Mouse.updateMouseState()
            self.clock.tick(game_view.FPS)
            self.detect_key_event()
            self.draw()
