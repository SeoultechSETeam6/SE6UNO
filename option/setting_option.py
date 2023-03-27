import pygame
import pickle
import math
from button import Button
from option import save_option as save
from option import basic_option as basic


class Option:
    def __init__(self):
        # 저장된 설정 불러오기, 만약 파일이 비어있다면 기본 설정으로 세팅
        try:
            with open("./option/save_option.pickle", "rb") as f:
                self.display_size = pickle.load(f)
                self.color_weakness = pickle.load(f)
                self.key_setting = pickle.load(f)
            with open("./option/save_option.pickle", "rb") as f:
                save.display_size = pickle.load(f)
                save.color_weakness = pickle.load(f)
                save.key_setting = pickle.load(f)
        except EOFError:
            self.display_size = basic.display_size
            self.color_weakness = basic.color_weakness
            self.key_setting = basic.key_setting
            save.display_size = basic.display_size
            save.color_weakness = basic.color_weakness
            save.key_setting = basic.key_setting

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

        self.change_screen_size = self.font.render("화면 크기 변경", True, (255, 255, 255))
        self.change_color_weakness = self.font.render("색약 모드 변경", True, (255, 255, 255))
        self.change_key_setting = self.font.render("사용 키 설정 변경", True, (255, 255, 255))
        self.screen_size_button = [
            Button(self.screen.get_width() // 3 * 2 - self.screen.get_width() // 8, self.screen.get_height() // 5,
                   self.button_size[0],
                   self.button_size[1], "1920 * 1080", self.size_1920_event, self.font_size[1]),
            Button(self.screen.get_width() // 3 * 2, self.screen.get_height() // 5, self.button_size[0],
                   self.button_size[1], "1600 * 900",
                   self.size_1600_event, self.font_size[1]),
            Button(self.screen.get_width() // 3 * 2 + self.screen.get_width() // 8, self.screen.get_height() // 5,
                   self.button_size[0],
                   self.button_size[1], "1280 * 720", self.size_1280_event, self.font_size[1])]

        if self.display_size[0] == 1920:
            self.screen_size_button[0].fill_colors['normal'] = '#333333'
        elif self.display_size[0] == 1600:
            self.screen_size_button[1].fill_colors['normal'] = '#333333'
        else:
            self.screen_size_button[2].fill_colors['normal'] = '#333333'

        if self.color_weakness:
            self.color_weakness_button = Button(self.screen.get_width() // 3 * 2, self.screen.get_height() // 5 * 2,
                                                self.button_size[0],
                                                self.button_size[1], "OFF", self.color_weakness_event,
                                                self.font_size[1])
        else:
            self.color_weakness_button = Button(self.screen.get_width() // 3 * 2, self.screen.get_height() // 5 * 2,
                                                self.button_size[0],
                                                self.button_size[1], "ON", self.color_weakness_event, self.font_size[1])
        self.key_setting_button = [
            Button(self.screen.get_width() // 3 * 2 - self.screen.get_width() // 9 * 2,
                   self.screen.get_height() * 3 // 5,
                   self.button_size[0], self.button_size[1], "UP: " + pygame.key.name(self.key_setting['up']),
                   self.key_up_event, self.font_size[1]),
            Button(self.screen.get_width() // 3 * 2 - self.screen.get_width() // 9, self.screen.get_height() * 3 // 5,
                   self.button_size[0],
                   self.button_size[1], "DOWN: " + pygame.key.name(self.key_setting['down']), self.key_down_event,
                   self.font_size[1]),
            Button(self.screen.get_width() // 3 * 2, self.screen.get_height() * 3 // 5, self.button_size[0],
                   self.button_size[1],
                   "LEFT: " + pygame.key.name(self.key_setting['left']), self.key_left_event, self.font_size[1]),
            Button(self.screen.get_width() // 3 * 2 + self.screen.get_width() // 9, self.screen.get_height() * 3 // 5,
                   self.button_size[0],
                   self.button_size[1], "RIGHT: " + pygame.key.name(self.key_setting['right']), self.key_right_event,
                   self.font_size[1]),
            Button(self.screen.get_width() // 3 * 2 + self.screen.get_width() // 9 * 2,
                   self.screen.get_height() * 3 // 5,
                   self.button_size[0], self.button_size[1], "Enter: " + pygame.key.name(self.key_setting['enter']),
                   self.key_enter_event, self.font_size[1])]
        self.reset_setting = Button(self.screen.get_width() // 4, self.screen.get_height() // 5 * 4,
                                    self.button_size[0], self.button_size[1],
                                    "설정 초기화", self.reset_event, self.font_size[1])
        self.save_setting = Button(self.screen.get_width() // 4 * 2, self.screen.get_height() // 5 * 4,
                                   self.button_size[0], self.button_size[1],
                                   "설정 저장", self.save_event, self.font_size[1])
        self.quit_setting = Button(self.screen.get_width() // 4 * 3, self.screen.get_height() // 5 * 4,
                                   self.button_size[0], self.button_size[1],
                                   "설정 나가기", self.exit_event, self.font_size[1])

        self.button_list = [[], [self.color_weakness_button], [],
                            [self.reset_setting, self.save_setting, self.quit_setting]]
        for i in self.screen_size_button:
            self.button_list[0].append(i)
        for i in self.key_setting_button:
            self.button_list[2].append(i)
        self.selected_button_vertical_index = 0
        self.selected_button_horizon_index = 0
        self.button_list[self.selected_button_vertical_index][self.selected_button_horizon_index].selected = True

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
        basic.mouse_event_remove()
        with open("./option/save_option.pickle", "wb") as rf:
            pickle.dump(basic.display_size, rf)
            pickle.dump(basic.color_weakness, rf)
            pickle.dump(basic.key_setting, rf)
        self.running = False

    def save_event(self):
        basic.mouse_event_remove()
        with open("./option/save_option.pickle", "wb") as sf:
            pickle.dump(save.display_size, sf)
            pickle.dump(save.color_weakness, sf)
            pickle.dump(save.key_setting, sf)
        self.running = False

    def exit_event(self):
        basic.mouse_event_remove()
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
        self.screen.blit(self.change_screen_size, (self.screen.get_width() // 7, self.screen.get_height() // 5))
        self.screen.blit(self.change_color_weakness, (self.screen.get_width() // 7, self.screen.get_height() // 5 * 2))
        self.screen.blit(self.change_key_setting, (self.screen.get_width() // 7, self.screen.get_height() // 5 * 3))

        for buttons in self.button_list:
            for button in buttons:
                button.process()
                self.screen.blit(button.surface, button.rect)
        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == self.key_setting['up']:
                    self.button_list[self.selected_button_vertical_index][
                        self.selected_button_horizon_index].selected = False
                    self.selected_button_vertical_index = (self.selected_button_vertical_index - 1) % len(
                        self.button_list)
                    self.selected_button_horizon_index = math.ceil(len(
                        self.button_list[self.selected_button_vertical_index]) / 2) - 1
                    self.button_list[self.selected_button_vertical_index][
                        self.selected_button_horizon_index].selected = True
                elif event.key == self.key_setting['down']:
                    self.button_list[self.selected_button_vertical_index][
                        self.selected_button_horizon_index].selected = False
                    self.selected_button_vertical_index = (self.selected_button_vertical_index + 1) % len(
                        self.button_list)
                    self.selected_button_horizon_index = math.ceil(len(
                        self.button_list[self.selected_button_vertical_index]) / 2) - 1
                    self.button_list[self.selected_button_vertical_index][
                        self.selected_button_horizon_index].selected = True
                elif event.key == self.key_setting['left']:
                    self.button_list[self.selected_button_vertical_index][
                        self.selected_button_horizon_index].selected = False
                    self.selected_button_horizon_index = (self.selected_button_horizon_index - 1) % len(
                        self.button_list[self.selected_button_vertical_index])
                    self.button_list[self.selected_button_vertical_index][
                        self.selected_button_horizon_index].selected = True
                elif event.key == self.key_setting['right']:
                    self.button_list[self.selected_button_vertical_index][
                        self.selected_button_horizon_index].selected = False
                    self.selected_button_horizon_index = (self.selected_button_horizon_index + 1) % len(
                        self.button_list[self.selected_button_vertical_index])
                    self.button_list[self.selected_button_vertical_index][
                        self.selected_button_horizon_index].selected = True
                elif event.key == self.key_setting['enter']:
                    self.button_list[self.selected_button_vertical_index][
                        self.selected_button_horizon_index].on_click_function()

    def run(self):
        while self.running:
            self.clock.tick(basic.fps)
            self.draw()
            self.event()
