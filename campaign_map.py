import pygame
import json
import pickle
from button import ButtonWithImg
from button import Button
from option import basic_option as basic


class CampaignMap:
    def __init__(self):
        # Pygame 초기화
        self.display_size = None
        self.color_weakness = None
        self.key_setting = None
        self.font_size = None
        self.button_size = None
        self.screen = None
        self.buttons = []
        self.selected_button_index = 0
        self.font = None
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()

        self.file_path = "./game_data.json"
        try:
            with open(self.file_path) as fr:
                self.clear_data = json.load(fr)["campaign_cleared_status"]
        except FileNotFoundError:
            clear_data = {
                "campaign_cleared_status": {
                    "1st": 0,
                    "2nd": 0,
                    "3rd": 0,
                    "4th": 0
                }
            }
            with open(self.file_path, 'w') as fw:
                json.dump(clear_data, fw, indent=4)

    def button_click_event(self):
        print('버튼 클릭됨')

    def exit_event(self):
        print('캠페인 맵 메뉴에서 나가기 버튼 클릭 됨')
        basic.mouse_event_remove()
        self.running = False

    def setting(self):
        # 창 관련 설정 불러오기
        try:
            with open("./option/save_option.pickle", "rb") as f:
                self.display_size = pickle.load(f)
                self.color_weakness = pickle.load(f)
                self.key_setting = pickle.load(f)
        except EOFError:
            self.display_size = basic.display_size
            self.color_weakness = basic.color_weakness
            self.key_setting = basic.key_setting

        if self.display_size[0] == 1920:
            self.font_size = basic.font_size[0]
            self.button_size = basic.button_size[0]
            self.campaign_map_button_size = basic.campaign_map_button_size[0]
        elif self.display_size[0] == 1600:
            self.font_size = basic.font_size[1]
            self.button_size = basic.button_size[1]
            self.campaign_map_button_size = basic.campaign_map_button_size[1]
        else:
            self.font_size = basic.font_size[2]
            self.button_size = basic.button_size[2]
            self.campaign_map_button_size = basic.campaign_map_button_size[2]

        # 화면 표시
        self.screen = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption(basic.game_title)

        # 폰트 설정
        self.font = pygame.font.Font("./resources/maplestory_font.ttf", self.font_size[1])

        # 버튼
        self.buttons = [Button(self.display_size[0] * 0.07, self.display_size[1] * 0.04, self.button_size[0],
                               self.button_size[1], "뒤로 가기", self.exit_event, self.font_size[1]),
                        ButtonWithImg(self.display_size[0] * 0.3, self.display_size[1] * 0.05,
                                      self.campaign_map_button_size[0],
                                      self.campaign_map_button_size[1], "resources/image/story_image/storygym_1.jpg",
                                      self.button_click_event)]

        # 클리어 체크 후 버튼 표시
        if self.clear_data["1st"] > 0:
            self.buttons.append(ButtonWithImg(self.display_size[0] * 0.35, self.display_size[1] * 0.5,
                                self.campaign_map_button_size[0],
                                self.campaign_map_button_size[1], "resources/image/story_image/storygym_2.jpg",
                                self.button_click_event))
        if self.clear_data["2nd"] > 0:
            self.buttons.append(ButtonWithImg(self.display_size[0] * 0.7, self.display_size[1] * 0.15,
                                self.campaign_map_button_size[0],
                                self.campaign_map_button_size[1], "resources/image/story_image/storygym_3.jpg",
                                self.button_click_event))
        if self.clear_data["3rd"] > 0:
            self.buttons.append(ButtonWithImg(self.display_size[0] * 0.75, self.display_size[1] * 0.6,
                                self.campaign_map_button_size[0],
                                self.campaign_map_button_size[1], "resources/image/story_image/storygym_4.jpg",
                                self.button_click_event))

        self.selected_button_index = 0
        self.buttons[self.selected_button_index].selected = True

    def draw(self):
        # 배경 색상
        self.screen.fill((255, 255, 255))

        # 버튼 표시
        for button in self.buttons:
            button.process()
            # 이미지 버튼일 경우 img_rect 사용
            if isinstance(button, ButtonWithImg):
                self.screen.blit(button.image, button.img_rect)
            self.screen.blit(button.surface, button.rect)

        # 매 프레임마다 화면 업데이트
        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == self.key_setting['up']:
                    self.buttons[self.selected_button_index].selected = False
                    self.selected_button_index = (self.selected_button_index - 1) % len(self.buttons)
                    self.buttons[self.selected_button_index].selected = True
                elif event.key == self.key_setting['down']:
                    self.buttons[self.selected_button_index].selected = False
                    self.selected_button_index = (self.selected_button_index + 1) % len(self.buttons)
                    self.buttons[self.selected_button_index].selected = True

                ## 좌우 방향키 키보드 조작
                # elif event.key == self.key_setting['left']:
                #     self.buttons[self.selected_button_index].selected = False
                #     if self.selected_button_index == 0 or 1:
                #         self.selected_button_index -= 1
                #     elif self.selected_button_index == 2:
                #         self.selected_button_index += 1
                #     else:
                #         self.selected_button_index = (self.selected_button_index - 2) % len(self.buttons)
                #     self.buttons[self.selected_button_index].selected = True
                # elif event.key == self.key_setting['right']:
                #     self.buttons[self.selected_button_index].selected = False
                #     if self.selected_button_index == 0:
                #         self.selected_button_index = 1
                #     elif self.selected_button_index == 3:
                #         self.selected_button_index = 2
                #     elif self.selected_button_index == 4:
                #         self.selected_button_index = 0
                #     else:
                #         self.selected_button_index = (self.selected_button_index + 2) % len(self.buttons)
                #     self.buttons[self.selected_button_index].selected = True

                elif event.key == self.key_setting['enter']:
                    self.buttons[self.selected_button_index].on_click_function()

    def run(self):
        self.setting()
        # 메인 화면 표시
        while self.running:
            self.clock.tick(basic.fps)
            self.event()
            self.draw()
