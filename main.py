import pygame
import sys
import pickle

from single_play_lobby import Lobby
from mouse import Mouse
from button import Button
from option import basic_option as basic
from option.setting_option import Option


class Main:
    def __init__(self):
        # Pygame 초기화
        self.display_size = None
        self.color_weakness = None
        self.key_setting = None
        self.font_size = None
        self.button_size = None
        self.logo_size = None
        self.screen = None

        self.buttons = []
        self.selected_button_index = 0
        self.logo = None
        self.logo_rect = None
        self.font = None
        self.key_setting_up = None
        self.key_setting_down = None
        self.key_setting_enter = None
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.background_music = pygame.mixer.Sound("./resources/Music/main.ogg")
        self.sound_volume = None
        self.background_volume = None
        self.effect_volume = None

    def settings_button_click_event(self):
        self.background_music.stop()
        print('설정 버튼 클릭됨')
        option = Option()
        option.run()
        self.setting()

    def exit_button_click_event(self):
        print('나가기 버튼 클릭됨')
        self.running = False

    def in_game_button_click_event(self):
        print('싱글 플레이 버튼 클릭됨')
        single_game_instance = Lobby()
        single_game_instance.run()

    def setting(self):
        # 설정 불러오기
        try:
            with open("./option/save_option.pickle", "rb") as f:
                self.display_size = pickle.load(f)
                self.color_weakness = pickle.load(f)
                self.key_setting = pickle.load(f)
                self.sound_volume = pickle.load(f)
                self.background_volume = pickle.load(f)
                self.effect_volume = pickle.load(f)
        except EOFError:

            self.display_size = basic.display_size
            self.color_weakness = basic.color_weakness
            self.key_setting = basic.key_setting
            self.sound_volume = basic.sound_volume
            self.background_volume = basic.background_volume
            self.effect_volume = basic.effect_volume

        if self.display_size[0] == 1920:
            self.font_size = basic.font_size[0]
            self.button_size = basic.button_size[0]
            self.logo_size = basic.logo_size[0]
        elif self.display_size[0] == 1600:
            self.font_size = basic.font_size[1]
            self.button_size = basic.button_size[1]
            self.logo_size = basic.logo_size[1]
        else:
            self.font_size = basic.font_size[2]
            self.button_size = basic.button_size[2]
            self.logo_size = basic.logo_size[2]

        self.background_music.set_volume(self.sound_volume * self.background_volume)
        self.background_music.play(-1)

        # 화면 표시
        self.screen = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption(basic.game_title)

        # 로고 표시
        self.logo = pygame.image.load("resources/Image/logo.png")
        self.logo = pygame.transform.scale(self.logo, self.logo_size)
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = ((self.display_size[0] // 2), self.logo_rect.height // 2)

        # 버튼 조작 키 표시
        self.font = pygame.font.Font("./resources/maplestory_font.ttf", self.font_size[1])
        self.key_setting_up = self.font.render("UP: " + pygame.key.name(self.key_setting['up']), True, (255, 255, 255))
        self.key_setting_down = self.font.render("DOWN: " + pygame.key.name(self.key_setting['down']), True, (255, 255, 255))
        self.key_setting_enter = self.font.render("Enter: " + pygame.key.name(self.key_setting['enter']), True, (255, 255, 255))

        # 버튼
        self.buttons = [
            Button(self.display_size[0] // 2, self.display_size[1] // 2, self.button_size[0], self.button_size[1],
                   '싱글 플레이', self.in_game_button_click_event, self.font_size[1]),
            Button(self.display_size[0] // 2, self.display_size[1] // 2 * 1.3, self.button_size[0],
                   self.button_size[1], '설정', self.settings_button_click_event, self.font_size[1]),
            Button(self.display_size[0] // 2, self.display_size[1] // 2 * 1.6, self.button_size[0],
                   self.button_size[1], '나가기', self.exit_button_click_event, self.font_size[1])]

        self.buttons[self.selected_button_index].keyboard_selected = True

    def draw(self):
        # 배경 색상
        self.screen.fill((20, 20, 20))
        # 버튼 조작 키 업데이트
        self.screen.blit(self.key_setting_up, (50, self.screen.get_height() // 30 * 26))
        self.screen.blit(self.key_setting_down, (50, self.screen.get_height() // 30 * 27))
        self.screen.blit(self.key_setting_enter, (50, self.screen.get_height() // 30 * 28))
        self.screen.blit(self.logo, self.logo_rect)
        for button in self.buttons:
            button.process()
            self.screen.blit(button.surface, button.rect)

        self.screen.blit(self.buttons[self.selected_button_index].selected_image,
                         (self.buttons[self.selected_button_index].rect.x, self.buttons[self.selected_button_index].rect.y - self.font_size[1]))
        # 매 프레임마다 화면 업데이트
        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == self.key_setting['up']:
                    self.buttons[self.selected_button_index].keyboard_selected = False
                    self.selected_button_index = (self.selected_button_index - 1) % len(self.buttons)
                    self.buttons[self.selected_button_index].keyboard_selected = True
                elif event.key == self.key_setting['down']:
                    self.buttons[self.selected_button_index].keyboard_selected = False
                    self.selected_button_index = (self.selected_button_index + 1) % len(self.buttons)
                    self.buttons[self.selected_button_index].keyboard_selected = True
                elif event.key == self.key_setting['enter']:
                    self.buttons[self.selected_button_index].on_click_function()

    def run(self):
        self.setting()
        # 메인 화면 표시
        while self.running:
            Mouse.updateMouseState()
            self.clock.tick(basic.fps)
            self.event()
            self.draw()
        # 나가기
        pygame.quit()
        sys.exit()


main = Main()
main.run()
