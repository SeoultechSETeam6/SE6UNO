import pygame
import json
import pickle
from button import ButtonWithImg
from button import Button
from option import basic_option as basic
from popup import Popup


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
        self.popup = None
        self.clear_flags = []

        # 스테이지 진행 상황 불러오기
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
            # 0일 경우 미클리어, 1 이상일 경우 클리어
            with open(self.file_path, 'w') as fw:
                json.dump(clear_data, fw, indent=4)

    def exit_event(self):
        basic.mouse_event_remove()
        print('캠페인 맵 메뉴에서 나가기 버튼 클릭 됨')
        self.running = False

    def start_1st_stage_event(self):
        print('1스테이지 입장 버튼 클릭됨')
        self.popup = Popup(self.display_size[0] * 0.5, self.display_size[1] * 0.5,
                           self.display_size[0] * 0.4, self.display_size[1] * 0.4,
                           '1스테이지 설명', self.check_event)
        self.popup.pop = True

    def start_2nd_stage_event(self):
        print('2스테이지 입장 버튼 클릭됨')
        self.popup = Popup(self.display_size[0] * 0.5, self.display_size[1] * 0.5,
                           self.display_size[0] * 0.4, self.display_size[1] * 0.4,
                           '2스테이지 설명', self.check_event)
        self.popup.pop = True

    def start_3rd_stage_event(self):
        print('3스테이지 입장 버튼 클릭됨')
        self.popup = Popup(self.display_size[0] * 0.5, self.display_size[1] * 0.5,
                           self.display_size[0] * 0.4, self.display_size[1] * 0.4,
                           '3스테이지 설명', self.check_event)
        self.popup.pop = True

    def start_4th_stage_event(self):
        print('4스테이지 입장 버튼 클릭됨')
        self.popup = Popup(self.display_size[0] * 0.5, self.display_size[1] * 0.5,
                           self.display_size[0] * 0.4, self.display_size[1] * 0.4,
                           '4스테이지 설명', self.check_event)
        self.popup.pop = True

    def check_event(self):
        basic.mouse_event_remove()
        print('스테이지 입장버튼 클릭됨')
        self.popup = Popup(self.display_size[0] * 0.5, self.display_size[1] * 0.5,
                           self.display_size[0] * 0.4, self.display_size[1] * 0.4,
                           '정말 입장하시겠습니까?', self.exit_event)
        self.popup.pop = True

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

        # 디스플레이 설정 불러오기
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

        # 팝업 초기 설정
        self.popup = Popup(self.display_size[0] * 0.5, self.display_size[1] * 0.5,
                           self.display_size[0] * 0.4, self.display_size[1] * 0.4)

        # 화면 표시
        self.screen = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption(basic.game_title)

        # 폰트 설정
        self.font = pygame.font.Font("./resources/maplestory_font.ttf", self.font_size[1])

        # 버튼
        self.buttons = [Button(self.display_size[0] * 0.07, self.display_size[1] * 0.06, self.button_size[0],
                               self.button_size[1], "뒤로 가기", self.exit_event, self.font_size[1]),
                        ButtonWithImg(self.display_size[0] * 0.15, self.display_size[1] * 0.3,
                                      self.campaign_map_button_size[0],
                                      self.campaign_map_button_size[1],
                                      "resources/image/story_image/storygym_1.jpg",
                                      self.check_event)]

        clear_flag = pygame.transform.scale(
                (pygame.image.load("resources/image/story_image/clear_mark.png")),
                (self.campaign_map_button_size[0] * 0.95, self.campaign_map_button_size[1] * 0.5))

        # 클리어 체크 후 버튼 표시 및 클리어 여부 표시
        if self.clear_data["1st"] > 0:
            self.buttons.append(ButtonWithImg(self.display_size[0] * 0.2, self.display_size[1] * 0.67,
                                              self.campaign_map_button_size[0],
                                              self.campaign_map_button_size[1],
                                              "resources/image/story_image/storygym_2.jpg",
                                              self.check_event))
            self.clear_flags.append(clear_flag)
        if self.clear_data["2nd"] > 0:
            self.buttons.append(ButtonWithImg(self.display_size[0] * 0.45, self.display_size[1] * 0.35,
                                              self.campaign_map_button_size[0],
                                              self.campaign_map_button_size[1],
                                              "resources/image/story_image/storygym_3.jpg",
                                              self.check_event))
            self.clear_flags.append(clear_flag)
        if self.clear_data["3rd"] > 0:
            self.buttons.append(ButtonWithImg(self.display_size[0] * 0.5, self.display_size[1] * 0.72,
                                              self.campaign_map_button_size[0],
                                              self.campaign_map_button_size[1],
                                              "resources/image/story_image/storygym_4.jpg",
                                              self.check_event))
            self.clear_flags.append(clear_flag)
        if self.clear_data["4th"] > 0:
            self.clear_flags.append(clear_flag)

        self.selected_button_index = 0
        self.buttons[self.selected_button_index].selected = True

    def draw(self):
        # 배경 색상
        self.screen.fill((255, 255, 255))

        # 설명창
        description_section = pygame.Surface((self.display_size[0] * 0.35, self.display_size[1]))
        description_section.fill((50, 50, 50))
        description_text = ['내 이름은 김우노. 우노 마스터가 되기 위해서\n'
                            '4개의 도장을 차례로 격파하기위해 여행을 다니고 있어!',
                            '1. 기술 도장: 상대방이 나보다 더 기술카드를 더 많이\n'
                            '가져가고 기술카드를 조합해서 콤보를 사용을 할 수 있어서 조심해야해!',
                            '2. 카드 러쉬 도장: 이 도장에서는 3명과 싸워야하고\n'
                            '첫 카드를 제외하고 모든 카드를 같은 수만큼 플레이어들에게\n'
                            '분배가 돼. 이 도장에서는 카드를 빨리 소모하는 것이 승리의 관건이야.',
                            '3. 색깔 도장: 2명의 상대와 대전하고 5턴마다 낼 수 있는\n'
                            '카드의 색상이 무작위로 변경되야해서 주의해야해!',
                            '4. 난투 도장: 이 곳에서는 쉴드 카드를 사용할 수 없게 되고,\n'
                            ' 새로운 공격카드가 추가되고 카드가 일정 매수가 넘어가면\n'
                            '게임오버가 되니까 주의해야 해!']

        description = [self.font.render(description_text[0], True, (255, 255, 255)),
                       self.font.render(description_text[1], True, (255, 255, 255)),
                       self.font.render(description_text[2], True, (255, 255, 255)),
                       self.font.render(description_text[3], True, (255, 255, 255)),
                       self.font.render(description_text[4], True, (255, 255, 255))]
        self.screen.blit(description_section, (self.display_size[0] * 0.65, 0))
        self.screen.blit(description[self.selected_button_index], [
            self.display_size[0] * 0.8 - description[self.selected_button_index].get_rect().width / 2,
            self.display_size[1] * 0.5 - description[self.selected_button_index].get_rect().height / 2])

        # 버튼 표시
        for button in self.buttons:
            # 팝업이 떠 있지 않을 경우 버튼 선택 가능
            if not self.popup.pop:
                button.process()

            # 이미지 버튼일 경우 img_rect도 포함
            if isinstance(button, ButtonWithImg):
                self.screen.blit(button.image, button.img_rect)
            self.screen.blit(button.surface, button.rect)

        # 클리어 스테이지 표시
        for i in range(0, len(self.clear_flags)):
            self.screen.blit(self.clear_flags[i],
                             self.clear_flags[i].get_rect(x=self.buttons[i + 1].x * 1.05, y=self.buttons[i + 1].y * 1.1))

        # 선택되면 팝업 띄우고 바깥은 비활성화
        if self.popup.pop:
            self.screen.blit(self.popup.surface, self.popup.rect)
            self.screen.blit(self.popup.font, [
                self.display_size[0] * 0.5 - self.popup.font.get_rect().width / 2,
                self.display_size[1] * 0.48 - self.popup.font.get_rect().height / 2])
            self.screen.blit(self.popup.accept_button.surface, self.popup.accept_button.rect)
            self.screen.blit(self.popup.close_button.surface, self.popup.close_button.rect)
            self.popup.open()

        # 매 프레임마다 화면 업데이트
        pygame.display.flip()

    def blit_text(self, surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and self.popup.pop == False:
                if event.key == self.key_setting['up']:
                    self.buttons[self.selected_button_index].selected = False
                    self.selected_button_index = (self.selected_button_index - 1) % len(self.buttons)
                    self.buttons[self.selected_button_index].selected = True
                elif event.key == self.key_setting['down']:
                    self.buttons[self.selected_button_index].selected = False
                    self.selected_button_index = (self.selected_button_index + 1) % len(self.buttons)
                    self.buttons[self.selected_button_index].selected = True
                elif event.key == self.key_setting['enter']:
                    self.buttons[self.selected_button_index].on_click_function()

    def run(self):
        self.setting()
        # 메인 화면 표시
        while self.running:
            self.clock.tick(basic.fps)
            self.event()
            self.draw()
