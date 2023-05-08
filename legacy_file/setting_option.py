import pygame
import pickle
import math
from controller.mouse_controller import Mouse
from ui.slider import Slider
from ui.button import Button
from legacy_file import save_option as save
from legacy_file import basic_option as basic


class Option:
    def __init__(self):
        # 저장된 설정 불러오기, 만약 파일이 비어있다면 기본 설정으로 세팅
        try:
            with open("./legacy_file/save_option.pickle", "rb") as f:
                self.display_size = pickle.load(f)
                self.color_weakness = pickle.load(f)
                self.key_setting = pickle.load(f)
                self.sound_volume = pickle.load(f)
                self.background_volume = pickle.load(f)
                self.effect_volume = pickle.load(f)
            with open("./legacy_file/save_option.pickle", "rb") as f:
                save.display_size = pickle.load(f)
                save.color_weakness = pickle.load(f)
                save.key_setting = pickle.load(f)
        except EOFError:
            self.display_size = basic.display_size
            self.color_weakness = basic.color_weakness
            self.key_setting = basic.key_setting
            self.sound_volume = basic.sound_volume
            self.background_volume = basic.background_volume
            self.effect_volume = basic.effect_volume
            save.display_size = basic.display_size
            save.color_weakness = basic.color_weakness
            save.key_setting = basic.key_setting

        # 회면 크기 별 폰트와 버튼 크기 설정
        if self.display_size[0] == 1920:
            self.font_size = basic.font_size[0]
            self.button_size = basic.button_size[0]
        elif self.display_size[0] == 1600:
            self.font_size = basic.font_size[1]
            self.button_size = basic.button_size[1]
        else:
            self.font_size = basic.font_size[2]
            self.button_size = basic.button_size[2]

        # pygame 초기화
        pygame.init()
        self.font = pygame.font.Font("./resources/maplestory_font.ttf", self.font_size[0])
        self.small_font = pygame.font.Font("./resources/maplestory_font.ttf", self.font_size[1])

        self.screen = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption(basic.game_title)
        self.clock = pygame.time.Clock()
        self.running = True

        # 안내 글자
        self.change_screen_size = self.font.render("화면 크기 변경", True, (255, 255, 255))
        self.change_color_weakness = self.font.render("색약 모드 변경", True, (255, 255, 255))
        self.change_key_setting = self.font.render("사용 키 설정 변경", True, (255, 255, 255))
        self.sound_volume_setting = self.font.render("전체 소리 볼륨 변경", True, (255, 255, 255))
        self.background_volume_setting = self.font.render("배경 음악 볼륨 변경", True, (255, 255, 255))
        self.effect_volume_setting = self.font.render("효과음 볼륨 변경", True, (255, 255, 255))

        # 화면 크기 버튼
        self.screen_size_button = [
            Button(self.screen.get_width() // 3 * 2 - self.screen.get_width() // 8, self.screen.get_height() // 8,
                   self.button_size[0],
                   self.button_size[1], "1920 * 1080", self.size_1920_event, self.font_size[1]),
            Button(self.screen.get_width() // 3 * 2, self.screen.get_height() // 8, self.button_size[0],
                   self.button_size[1], "1600 * 900",
                   self.size_1600_event, self.font_size[1]),
            Button(self.screen.get_width() // 3 * 2 + self.screen.get_width() // 8, self.screen.get_height() // 8,
                   self.button_size[0],
                   self.button_size[1], "1280 * 720", self.size_1280_event, self.font_size[1])]

        if self.display_size[0] == 1920:
            self.screen_size_button[0].fill_colors['normal'] = '#333333'
        elif self.display_size[0] == 1600:
            self.screen_size_button[1].fill_colors['normal'] = '#333333'
        else:
            self.screen_size_button[2].fill_colors['normal'] = '#333333'

        # 색약 모드 버튼
        if self.color_weakness:
            self.color_weakness_button = Button(self.screen.get_width() // 3 * 2, self.screen.get_height() // 8 * 2,
                                                self.button_size[0],
                                                self.button_size[1], "OFF", self.color_weakness_event,
                                                self.font_size[1])
        else:
            self.color_weakness_button = Button(self.screen.get_width() // 3 * 2, self.screen.get_height() // 8 * 2,
                                                self.button_size[0],
                                                self.button_size[1], "ON", self.color_weakness_event,
                                                self.font_size[1])

        # 키 설정 변경 버튼
        self.key_setting_button = [
            Button(self.screen.get_width() // 3 * 2 - self.screen.get_width() // 9 * 2,
                   self.screen.get_height() * 3 // 8,
                   self.button_size[0], self.button_size[1], "UP: " + pygame.key.name(self.key_setting['up']),
                   self.key_up_event, self.font_size[1]),
            Button(self.screen.get_width() // 3 * 2 - self.screen.get_width() // 9, self.screen.get_height() * 3 // 8,
                   self.button_size[0],
                   self.button_size[1], "DOWN: " + pygame.key.name(self.key_setting['down']), self.key_down_event,
                   self.font_size[1]),
            Button(self.screen.get_width() // 3 * 2, self.screen.get_height() * 3 // 8, self.button_size[0],
                   self.button_size[1],
                   "LEFT: " + pygame.key.name(self.key_setting['left']), self.key_left_event, self.font_size[1]),
            Button(self.screen.get_width() // 3 * 2 + self.screen.get_width() // 9, self.screen.get_height() * 3 // 8,
                   self.button_size[0],
                   self.button_size[1], "RIGHT: " + pygame.key.name(self.key_setting['right']), self.key_right_event,
                   self.font_size[1]),
            Button(self.screen.get_width() // 3 * 2 + self.screen.get_width() // 9 * 2,
                   self.screen.get_height() * 3 // 8,
                   self.button_size[0], self.button_size[1], "Enter: " + pygame.key.name(self.key_setting['enter']),
                   self.key_enter_event, self.font_size[1])]

        # 볼륨 조절 slider
        self.volume_slider = [Slider(self.screen, self.screen.get_width() // 3 * 2, self.screen.get_height() * 4 // 8, self.screen.get_width() // 3, self.screen.get_height() // 40, self.sound_volume, self.font_size[1]),
                              Slider(self.screen, self.screen.get_width() // 3 * 2, self.screen.get_height() * 5 // 8, self.screen.get_width() // 3, self.screen.get_height() // 40, self.background_volume, self.font_size[1]),
                              Slider(self.screen, self.screen.get_width() // 3 * 2, self.screen.get_height() * 6 // 8, self.screen.get_width() // 3, self.screen.get_height() // 40, self.effect_volume, self.font_size[1])]

        # 설정 저장 초기화 버튼
        self.reset_setting = Button(self.screen.get_width() // 4, self.screen.get_height() // 8 * 7,
                                    self.button_size[0], self.button_size[1],
                                    "설정 초기화", self.reset_event, self.font_size[1])
        self.save_setting = Button(self.screen.get_width() // 4 * 2, self.screen.get_height() // 8 * 7,
                                   self.button_size[0], self.button_size[1],
                                   "설정 저장", self.save_event, self.font_size[1])
        self.quit_setting = Button(self.screen.get_width() // 4 * 3, self.screen.get_height() // 8 * 7,
                                   self.button_size[0], self.button_size[1],
                                   "설정 나가기", self.exit_event, self.font_size[1])

        self.setting_obj_list = []
        self.setting_obj_list.append(self.screen_size_button)
        self.setting_obj_list.append([self.color_weakness_button])
        self.setting_obj_list.append(self.key_setting_button)
        for i in self.volume_slider:
            self.setting_obj_list.append([i])
        self.setting_obj_list.append([self.reset_setting, self.save_setting, self.quit_setting])

        self.selected_object_vertical_index = 0
        self.selected_object_horizon_index = 0
        self.setting_obj_list[self.selected_object_vertical_index][self.selected_object_horizon_index].keyboard_selected = True

    # 버튼 클릭시 메소드 구현
    def size_1920_event(self):
        save.display_size = [1920, 1080]
        self.screen_size_button[0].fill_colors['normal'] = '#666666'
        self.screen_size_button[1].fill_colors['normal'] = '#ffffff'
        self.screen_size_button[2].fill_colors['normal'] = '#ffffff'

    def size_1600_event(self):
        save.display_size = [1600, 900]
        self.screen_size_button[0].fill_colors['normal'] = '#ffffff'
        self.screen_size_button[1].fill_colors['normal'] = '#666666'
        self.screen_size_button[2].fill_colors['normal'] = '#ffffff'

    def size_1280_event(self):
        save.display_size = [1280, 720]
        self.screen_size_button[0].fill_colors['normal'] = '#ffffff'
        self.screen_size_button[1].fill_colors['normal'] = '#ffffff'
        self.screen_size_button[2].fill_colors['normal'] = '#666666'

    def color_weakness_event(self):
        if save.color_weakness:
            self.color_weakness_button.font = self.small_font.render("ON", True, (0, 0, 0))
            save.color_weakness = False
        else:
            self.color_weakness_button.font = self.small_font.render("OFF", True, (0, 0, 0))
            save.color_weakness = True

    def key_up_event(self):
        self.pop_up('up')
        self.key_setting_button[0].font = self.small_font.render("UP: " + pygame.key.name(save.key_setting['up']),
                                                                 True, (0, 0, 0))

    def key_down_event(self):
        self.pop_up('down')
        self.key_setting_button[1].font = self.small_font.render("DOWN: " + pygame.key.name(save.key_setting['down']),
                                                                 True, (0, 0, 0))

    def key_left_event(self):
        self.pop_up('left')
        self.key_setting_button[2].font = self.small_font.render("LEFT: " + pygame.key.name(save.key_setting['left']),
                                                                 True, (0, 0, 0))

    def key_right_event(self):
        self.pop_up('right')
        self.key_setting_button[3].font = self.small_font.render(
            "RIGHT: " + pygame.key.name(save.key_setting['right']), True, (0, 0, 0))

    def key_enter_event(self):
        self.pop_up('enter')
        self.key_setting_button[4].font = self.small_font.render(
            "ENTER: " + pygame.key.name(save.key_setting['enter']), True, (0, 0, 0))

    def reset_event(self):
        with open("./legacy_file/save_option.pickle", "wb") as rf:
            pickle.dump(basic.display_size, rf)
            pickle.dump(basic.color_weakness, rf)
            pickle.dump(basic.key_setting, rf)
            pickle.dump(basic.sound_volume, rf)
            pickle.dump(basic.background_volume, rf)
            pickle.dump(basic.effect_volume, rf)
        self.running = False

    def save_event(self):
        with open("./legacy_file/save_option.pickle", "wb") as sf:
            pickle.dump(save.display_size, sf)
            pickle.dump(save.color_weakness, sf)
            pickle.dump(save.key_setting, sf)
            pickle.dump(self.volume_slider[0].value, sf)
            pickle.dump(self.volume_slider[1].value, sf)
            pickle.dump(self.volume_slider[2].value, sf)
        self.running = False

    def exit_event(self):
        self.running = False

    def pop_up(self, direction):
        popup = self.font.render("바꾸고자하는 키를 입력하시오.", True, (0, 0, 0))
        self.screen.fill((255, 255, 255))
        self.screen.blit(popup, (self.screen.get_width() // 2 - popup.get_size()[0] // 2,
                                 self.screen.get_height() // 2))
        pygame.display.flip()
        popup_running = True
        while popup_running:
            for popup_event in pygame.event.get():
                if popup_event.type == pygame.KEYDOWN:
                    save.key_setting[direction] = popup_event.key
                    popup_running = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.change_screen_size, (self.screen.get_width() // 7, self.screen.get_height() // 8))
        self.screen.blit(self.change_color_weakness, (self.screen.get_width() // 7, self.screen.get_height() // 8 * 2))
        self.screen.blit(self.change_key_setting, (self.screen.get_width() // 7, self.screen.get_height() // 8 * 3))
        self.screen.blit(self.sound_volume_setting, (self.screen.get_width() // 7, self.screen.get_height() // 8 * 4))
        self.screen.blit(self.background_volume_setting, (self.screen.get_width() // 7, self.screen.get_height() // 8 * 5))
        self.screen.blit(self.effect_volume_setting, (self.screen.get_width() // 7, self.screen.get_height() // 8 * 6))

        for objects in self.setting_obj_list:
            for obj in objects:
                if isinstance(obj, Button):
                    obj.process()
                    self.screen.blit(obj.surface, obj.rect)
                elif isinstance(obj, Slider):
                    obj.draw()
                    obj.process()

        self.screen.blit(self.setting_obj_list[self.selected_object_vertical_index][self.selected_object_horizon_index].selected_image,
                         (self.setting_obj_list[self.selected_object_vertical_index][self.selected_object_horizon_index].rect.x, self.setting_obj_list[self.selected_object_vertical_index][self.selected_object_horizon_index].rect.y - self.font_size[1]))
        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == self.key_setting['up']:
                    self.setting_obj_list[self.selected_object_vertical_index][
                        self.selected_object_horizon_index].keyboard_selected = False
                    self.selected_object_vertical_index = (self.selected_object_vertical_index - 1) % len(
                        self.setting_obj_list)
                    self.selected_object_horizon_index = math.ceil(len(
                        self.setting_obj_list[self.selected_object_vertical_index]) / 2) - 1
                    self.setting_obj_list[self.selected_object_vertical_index][
                        self.selected_object_horizon_index].keyboard_selected = True
                elif event.key == self.key_setting['down']:
                    self.setting_obj_list[self.selected_object_vertical_index][
                        self.selected_object_horizon_index].keyboard_selected = False
                    self.selected_object_vertical_index = (self.selected_object_vertical_index + 1) % len(
                        self.setting_obj_list)
                    self.selected_object_horizon_index = math.ceil(len(
                        self.setting_obj_list[self.selected_object_vertical_index]) / 2) - 1
                    self.setting_obj_list[self.selected_object_vertical_index][
                        self.selected_object_horizon_index].keyboard_selected = True
                elif event.key == self.key_setting['left']:
                    if isinstance(self.setting_obj_list[self.selected_object_vertical_index][self.selected_object_horizon_index], Button):
                        self.setting_obj_list[self.selected_object_vertical_index][
                            self.selected_object_horizon_index].keyboard_selected = False
                        self.selected_object_horizon_index = (self.selected_object_horizon_index - 1) % len(
                            self.setting_obj_list[self.selected_object_vertical_index])
                        self.setting_obj_list[self.selected_object_vertical_index][
                            self.selected_object_horizon_index].keyboard_selected = True
                    elif isinstance(self.setting_obj_list[self.selected_object_vertical_index][self.selected_object_horizon_index], Slider):
                        self.setting_obj_list[self.selected_object_vertical_index][self.selected_object_horizon_index].value = self.setting_obj_list[self.selected_object_vertical_index][self.selected_object_horizon_index].value - 0.05
                        self.setting_obj_list[self.selected_object_vertical_index][
                            self.selected_object_horizon_index].value = max(min(self.setting_obj_list[self.selected_object_vertical_index][
                                self.selected_object_horizon_index].value, self.setting_obj_list[self.selected_object_vertical_index][
                                    self.selected_object_horizon_index].max), self.setting_obj_list[self.selected_object_vertical_index][
                                        self.selected_object_horizon_index].min)
                elif event.key == self.key_setting['right']:
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
                elif event.key == self.key_setting['enter']:
                    self.setting_obj_list[self.selected_object_vertical_index][
                        self.selected_object_horizon_index].on_click_function()

    def run(self):
        while self.running:
            Mouse.updateMouseState()
            self.clock.tick(basic.fps)
            self.draw()
            self.event()