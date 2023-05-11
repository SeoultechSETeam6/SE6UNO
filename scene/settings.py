import math
import pygame

from controller import game_data, game_view
from controller.mouse import Mouse
from ui.button import Button
from ui.slider import Slider
from ui.popup import Popup


class Settings:
    def __init__(self):
        # 게임 설정 불러오기
        self.settings_data = game_data.load_settings()

        # pygame 초기화
        pygame.init()
        pygame.display.set_caption(game_view.GAME_TITLE + ": Settings")
        self.ui_size = game_view.set_size(self.settings_data["resolution"]["width"])
        self.screen = pygame.display.set_mode((self.settings_data["resolution"]["width"],
                                               self.settings_data["resolution"]["height"]))
        self.clock = pygame.time.Clock()
        self.running = True

        # 글꼴 설정
        self.font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][0])
        self.font_small = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][1])

        # 텍스트 설정
        self.text_resolution = self.font.render("해상도 변경", True, (255, 255, 255))
        self.text_color_weakness = self.font.render("색약 모드 변경", True, (255, 255, 255))
        self.text_key_setting = self.font.render("사용 키 설정 변경", True, (255, 255, 255))
        self.text_sound_volume = self.font.render("전체 소리 볼륨 변경", True, (255, 255, 255))
        self.text_background_volume = self.font.render("배경 음악 볼륨 변경", True, (255, 255, 255))
        self.text_effect_volume = self.font.render("효과음 볼륨 변경", True, (255, 255, 255))

        # 해상도 선택 버튼
        self.button_resolution = [
            Button(self.screen.get_width() // 3 * 2 - self.screen.get_width() // 8,
                   self.screen.get_height() // 8,
                   self.ui_size["button"][0],
                   self.ui_size["button"][1],
                   self.screen,
                   0xffffff,
                   "1920 * 1080",
                   self.ui_size["font"][1],
                   on_click_function=self.event_change_resolution_1920),
            Button(self.screen.get_width() // 3 * 2,
                   self.screen.get_height() // 8,
                   self.ui_size["button"][0],
                   self.ui_size["button"][1],
                   self.screen,
                   0xffffff,
                   "1600 * 900",
                   self.ui_size["font"][1],
                   on_click_function=self.event_change_resolution_1600),
            Button(self.screen.get_width() // 3 * 2 + self.screen.get_width() // 8,
                   self.screen.get_height() // 8,
                   self.ui_size["button"][0],
                   self.ui_size["button"][1],
                   self.screen,
                   0xffffff,
                   "1280 * 720",
                   self.ui_size["font"][1],
                   on_click_function=self.event_change_resolution_1280)]
        if self.settings_data["resolution"]["width"] == 1920:
            self.button_resolution[0].colors['normal'] = int(0xffffff * 0.3)
        elif self.settings_data["resolution"]["width"] == 1600:
            self.button_resolution[1].colors['normal'] = int(0xffffff * 0.3)
        else:
            self.button_resolution[2].colors['normal'] = int(0xffffff * 0.3)

        # 색약 모드 버튼
        self.button_color_weakness = Button(self.screen.get_width() // 3 * 2,
                                            self.screen.get_height() // 8 * 2,
                                            self.ui_size["button"][0],
                                            self.ui_size["button"][1],
                                            self.screen,
                                            0xffffff,
                                            "ON",
                                            self.ui_size["font"][1],
                                            on_click_function=self.event_color_weakness)
        if self.settings_data["color_weakness"]:
            self.button_color_weakness.text = "ON"

        # 키 설정 변경 버튼
        self.button_key = [Button(self.screen.get_width() // 3 * 2 - self.screen.get_width() // 9 * 2,
                                  self.screen.get_height() * 3 // 8,
                                  self.ui_size["button"][0],
                                  self.ui_size["button"][1],
                                  self.screen,
                                  0xffffff,
                                  "UP: " + pygame.key.name(self.settings_data["key"]["up"]),
                                  self.ui_size["font"][1],
                                  on_click_function=self.event_key_up),
                           Button(self.screen.get_width() // 3 * 2 - self.screen.get_width() // 9,
                                  self.screen.get_height() * 3 // 8,
                                  self.ui_size["button"][0],
                                  self.ui_size["button"][1],
                                  self.screen,
                                  0xffffff,
                                  "DOWN: " + pygame.key.name(self.settings_data["key"]["down"]),
                                  self.ui_size["font"][1],
                                  on_click_function=self.event_key_down),
                           Button(self.screen.get_width() // 3 * 2,
                                  self.screen.get_height() * 3 // 8,
                                  self.ui_size["button"][0],
                                  self.ui_size["button"][1],
                                  self.screen,
                                  0xffffff,
                                  "LEFT: " + pygame.key.name(self.settings_data["key"]["left"]),
                                  self.ui_size["font"][1],
                                  on_click_function=self.event_key_left),
                           Button(self.screen.get_width() // 3 * 2 + self.screen.get_width() // 9,
                                  self.screen.get_height() * 3 // 8,
                                  self.ui_size["button"][0],
                                  self.ui_size["button"][1],
                                  self.screen,
                                  0xffffff,
                                  "RIGHT: " + pygame.key.name(self.settings_data["key"]["right"]),
                                  self.ui_size["font"][1],
                                  on_click_function=self.event_key_right),
                           Button(self.screen.get_width() // 3 * 2 + self.screen.get_width() // 9 * 2,
                                  self.screen.get_height() * 3 // 8,
                                  self.ui_size["button"][0],
                                  self.ui_size["button"][1],
                                  self.screen,
                                  0xffffff,
                                  "ENTER: " + pygame.key.name(self.settings_data["key"]["enter"]),
                                  self.ui_size["font"][1],
                                  on_click_function=self.event_key_enter)]

        # 키 변경 팝업
        self.popup_key_change = Popup(self.screen.get_width() // 2,
                                      self.screen.get_height() // 2,
                                      self.screen.get_width() * 0.4,
                                      self.screen.get_height() * 0.4,
                                      self.screen,
                                      '바꾸고자 하는 키를 입력한 후 확인을 눌러주세요.',
                                      on_click_function=self.event_save_key)

        # 볼륨 조절 slider
        self.slider_volume = [Slider(self.screen,
                                     self.screen.get_width() // 3 * 2,
                                     self.screen.get_height() * 4 // 8,
                                     self.screen.get_width() // 3,
                                     self.screen.get_height() // 40,
                                     self.settings_data["volume"]["sound"],
                                     self.ui_size["font"][1]),
                              Slider(self.screen,
                                     self.screen.get_width() // 3 * 2,
                                     self.screen.get_height() * 5 // 8,
                                     self.screen.get_width() // 3,
                                     self.screen.get_height() // 40,
                                     self.settings_data["volume"]["background"],
                                     self.ui_size["font"][1]),
                              Slider(self.screen,
                                     self.screen.get_width() // 3 * 2,
                                     self.screen.get_height() * 6 // 8,
                                     self.screen.get_width() // 3,
                                     self.screen.get_height() // 40,
                                     self.settings_data["volume"]["effect"],
                                     self.ui_size["font"][1])]

        # 설정 저장 초기화 버튼
        self.button_reset = Button(self.screen.get_width() // 4,
                                   self.screen.get_height() // 8 * 7,
                                   self.ui_size["button"][0],
                                   self.ui_size["button"][1],
                                   self.screen,
                                   0xffffff,
                                   "설정 초기화",
                                   self.ui_size["font"][1],
                                   on_click_function=self.event_reset)
        self.button_save = Button(self.screen.get_width() // 4 * 2,
                                  self.screen.get_height() // 8 * 7,
                                  self.ui_size["button"][0],
                                  self.ui_size["button"][1],
                                  self.screen,
                                  0xffffff,
                                  "설정 저장",
                                  self.ui_size["font"][1],
                                  on_click_function=self.event_save)
        self.button_quit = Button(self.screen.get_width() // 4 * 3,
                                  self.screen.get_height() // 8 * 7,
                                  self.ui_size["button"][0],
                                  self.ui_size["button"][1],
                                  self.screen,
                                  0xffffff,
                                  "설정 나가기",
                                  self.ui_size["font"][1],
                                  on_click_function=self.event_quit)

        # 팝업의 확인을 누르기 전까지 키 설정을 저장할 변수
        self.selected_key = self.settings_data["key"]

        # 어떤 키 변경 버튼을 눌렀는지 저장할 변수
        self.current_setting_key = "key_name", 10   # key_button_index

        # 키보드 조작 관련 변수
        self.setting_obj_list = []
        self.setting_obj_list.append(self.button_resolution)
        self.setting_obj_list.append([self.button_color_weakness])
        self.setting_obj_list.append(self.button_key)
        for i in self.slider_volume:
            self.setting_obj_list.append([i])
        self.setting_obj_list.append([self.button_reset, self.button_save, self.button_quit])

        self.selected_object_vertical_index = 0
        self.selected_object_horizon_index = 0
        self.setting_obj_list[self.selected_object_vertical_index][self.selected_object_horizon_index] \
            .keyboard_selected = True

    # 해상도 변경 이벤트
    def event_change_resolution_1920(self):
        self.settings_data["resolution"]["width"] = 1920
        self.settings_data["resolution"]["height"] = 1080
        self.button_resolution[0].colors['normal'] = int(0xffffff * 0.3)
        self.button_resolution[1].colors['normal'] = 0xffffff
        self.button_resolution[2].colors['normal'] = 0xffffff

    def event_change_resolution_1600(self):
        self.settings_data["resolution"]["width"] = 1600
        self.settings_data["resolution"]["height"] = 900
        self.button_resolution[0].colors['normal'] = 0xffffff
        self.button_resolution[1].colors['normal'] = int(0xffffff * 0.3)
        self.button_resolution[2].colors['normal'] = 0xffffff

    def event_change_resolution_1280(self):
        self.settings_data["resolution"]["width"] = 1280
        self.settings_data["resolution"]["height"] = 720
        self.button_resolution[0].colors['normal'] = 0xffffff
        self.button_resolution[1].colors['normal'] = 0xffffff
        self.button_resolution[2].colors['normal'] = int(0xffffff * 0.3)

    # 색약 설정 이벤트
    def event_color_weakness(self):
        if self.settings_data["color_weakness"]:
            self.button_color_weakness.text = "OFF"
            self.settings_data["color_weakness"] = False
        else:
            self.button_color_weakness.text = "ON"
            self.settings_data["color_weakness"] = True

    # 키 설정 이벤트
    def event_key_up(self):
        self.popup_key_change.pop = True
        self.current_setting_key = "up", 0

    def event_key_down(self):
        self.popup_key_change.pop = True
        self.current_setting_key = "down", 1

    def event_key_left(self):
        self.popup_key_change.pop = True
        self.current_setting_key = "left", 2

    def event_key_right(self):
        self.popup_key_change.pop = True
        self.popup_key_change.on_click_function = self.event_save_key
        self.current_setting_key = "right", 3

    def event_key_enter(self):
        self.popup_key_change.pop = True
        self.popup_key_change.on_click_function = self.event_save_key
        self.current_setting_key = "enter", 4

    # 키 설정 팝업의 확인 버튼 이벤트
    # 확인을 눌러야 램에 반영하고, 저장을 눌러야 최종적으로 게임 전체에 반영
    def event_save_key(self):
        self.settings_data["key"] = self.selected_key
        self.button_key[self.current_setting_key[1]].text =\
            self.current_setting_key[0].upper() + ": " + pygame.key.name(self.settings_data["key"][self.current_setting_key[0]])
        self.popup_key_change.pop = False

    # 리셋 버튼 이벤트
    def event_reset(self):
        game_data.save_settings(game_data.INIT_GAME_DATA["settings"])
        self.running = False

    # 나가기 버튼 이벤트
    def event_quit(self):
        self.running = False

    # 저장 버튼 이벤트
    def event_save(self):
        # 볼륨 조정한 결과 저장
        self.settings_data["volume"]["sound"] = self.slider_volume[0].value
        self.settings_data["volume"]["background"] = self.slider_volume[1].value
        self.settings_data["volume"]["effect"] = self.slider_volume[2].value

        game_data.save_settings(self.settings_data)
        self.running = False

    # 버튼과 글자, 기타 오브젝트를 그리는 메서드
    def draw(self):
        self.screen.fill((0, 0, 0))

        # 글자 그림
        self.screen.blit(self.text_resolution, (self.screen.get_width() // 7, self.screen.get_height() // 8))
        self.screen.blit(self.text_color_weakness, (self.screen.get_width() // 7, self.screen.get_height() // 8 * 2))
        self.screen.blit(self.text_key_setting, (self.screen.get_width() // 7, self.screen.get_height() // 8 * 3))
        self.screen.blit(self.text_sound_volume, (self.screen.get_width() // 7, self.screen.get_height() // 8 * 4))
        self.screen.blit(self.text_background_volume, (self.screen.get_width() // 7, self.screen.get_height() // 8 * 5))
        self.screen.blit(self.text_effect_volume, (self.screen.get_width() // 7, self.screen.get_height() // 8 * 6))

        # 버튼과 슬라이더 그림
        for objects in self.setting_obj_list:
            for obj in objects:
                obj.draw()
                if self.popup_key_change.pop:
                    self.popup_key_change.open()
                else:
                    obj.detect_event()

        self.screen.blit(self.setting_obj_list[self.selected_object_vertical_index][
                             self.selected_object_horizon_index].selected_image,
                         (self.setting_obj_list[self.selected_object_vertical_index][
                              self.selected_object_horizon_index].rect.x,
                          self.setting_obj_list[self.selected_object_vertical_index][
                              self.selected_object_horizon_index].rect.y - self.ui_size["font"][1]))
        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.popup_key_change.pop:
                    self.selected_key[self.current_setting_key[0]] = event.key
                else:
                    if event.key == self.settings_data["key"]['up']:
                        self.setting_obj_list[self.selected_object_vertical_index][
                            self.selected_object_horizon_index].keyboard_selected = False
                        self.selected_object_vertical_index = (self.selected_object_vertical_index - 1) % len(
                            self.setting_obj_list)
                        self.selected_object_horizon_index = math.ceil(len(
                            self.setting_obj_list[self.selected_object_vertical_index]) / 2) - 1
                        self.setting_obj_list[self.selected_object_vertical_index][
                            self.selected_object_horizon_index].keyboard_selected = True
                    elif event.key == self.settings_data["key"]['down']:
                        self.setting_obj_list[self.selected_object_vertical_index][
                            self.selected_object_horizon_index].keyboard_selected = False
                        self.selected_object_vertical_index = (self.selected_object_vertical_index + 1) % len(
                            self.setting_obj_list)
                        self.selected_object_horizon_index = math.ceil(len(
                            self.setting_obj_list[self.selected_object_vertical_index]) / 2) - 1
                        self.setting_obj_list[self.selected_object_vertical_index][
                            self.selected_object_horizon_index].keyboard_selected = True
                    elif event.key == self.settings_data["key"]['left']:
                        if isinstance(self.setting_obj_list[self.selected_object_vertical_index][
                                          self.selected_object_horizon_index], Button):
                            self.setting_obj_list[self.selected_object_vertical_index][
                                self.selected_object_horizon_index].keyboard_selected = False
                            self.selected_object_horizon_index = (self.selected_object_horizon_index - 1) % len(
                                self.setting_obj_list[self.selected_object_vertical_index])
                            self.setting_obj_list[self.selected_object_vertical_index][
                                self.selected_object_horizon_index].keyboard_selected = True
                        elif isinstance(self.setting_obj_list[self.selected_object_vertical_index][
                                            self.selected_object_horizon_index], Slider):
                            self.setting_obj_list[self.selected_object_vertical_index][
                                self.selected_object_horizon_index].value = \
                                self.setting_obj_list[self.selected_object_vertical_index][
                                    self.selected_object_horizon_index].value - 0.05
                            self.setting_obj_list[self.selected_object_vertical_index][
                                self.selected_object_horizon_index].value = max(
                                min(self.setting_obj_list[self.selected_object_vertical_index][
                                        self.selected_object_horizon_index].value,
                                    self.setting_obj_list[self.selected_object_vertical_index][
                                        self.selected_object_horizon_index].max),
                                self.setting_obj_list[self.selected_object_vertical_index][
                                    self.selected_object_horizon_index].min)
                    elif event.key == self.settings_data["key"]['right']:
                        if isinstance(self.setting_obj_list[self.selected_object_vertical_index][
                                          self.selected_object_horizon_index], Button):
                            self.setting_obj_list[self.selected_object_vertical_index][
                                self.selected_object_horizon_index].keyboard_selected = False
                            self.selected_object_horizon_index = (self.selected_object_horizon_index + 1) % len(
                                self.setting_obj_list[self.selected_object_vertical_index])
                            self.setting_obj_list[self.selected_object_vertical_index][
                                self.selected_object_horizon_index].keyboard_selected = True
                        elif isinstance(self.setting_obj_list[self.selected_object_vertical_index][
                                            self.selected_object_horizon_index], Slider):
                            self.setting_obj_list[self.selected_object_vertical_index][
                                self.selected_object_horizon_index].value = \
                                self.setting_obj_list[self.selected_object_vertical_index][
                                    self.selected_object_horizon_index].value + 0.05
                            self.setting_obj_list[self.selected_object_vertical_index][
                                self.selected_object_horizon_index].value = max(
                                min(self.setting_obj_list[self.selected_object_vertical_index][
                                        self.selected_object_horizon_index].value,
                                    self.setting_obj_list[self.selected_object_vertical_index][
                                        self.selected_object_horizon_index].max),
                                self.setting_obj_list[self.selected_object_vertical_index][
                                    self.selected_object_horizon_index].min)
                    elif event.key == self.settings_data["key"]['enter']:
                        self.setting_obj_list[self.selected_object_vertical_index][
                            self.selected_object_horizon_index].on_click_function()

    def run(self):
        while self.running:
            Mouse.updateMouseState()
            self.clock.tick(game_view.FPS)
            self.draw()
            self.event()
