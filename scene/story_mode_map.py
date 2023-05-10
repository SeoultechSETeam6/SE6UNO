import pygame

from controller.mouse import Mouse
from controller import game_data, game_view
from ui.button import Button, ImageButton
from ui.popup import Popup
# from scene.story_mode_stage import StageA, StageB, StageC, StageD


class StoryModeMap:
    def __init__(self):
        # 게임 설정 불러오기
        self.settings_data = game_data.load_settings()

        # 클리어 데이터 불러오기
        self.clear_data = game_data.load_stage_clear()

        # Pygame 초기화
        pygame.init()
        pygame.display.set_caption(game_view.GAME_TITLE + ": Select Stage")
        self.ui_size = game_view.set_size(self.settings_data["resolution"]["width"])
        self.screen = pygame.display.set_mode((self.settings_data["resolution"]["width"],
                                               self.settings_data["resolution"]["height"]))
        self.clock = pygame.time.Clock()
        self.running = True

        # 설명창 영역
        self.description_section = pygame.Surface((self.screen.get_width() * 0.35, self.screen.get_height()))
        self.description_section.fill((50, 50, 50))

        # 글꼴 설정
        self.font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][0])

        # 스테이지 이름
        self.font_title = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][1] * 3)
        self.text_title = ['캠페인 모드', '1. 기술 도장', '2. 카드러시 도장', '3. 무지개 도장', '4. 난투 도장']

        # 스테이지 설명
        self.font_description = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][1] * 2)
        self.text_description = [
            '내 이름은 김우노. 우노 마스터가 되기 위해서 4개의 도장을 차례로 격파하기위해 여행을 다니고 있어!',
            '상대방이 나보다 더 기술카드를 더 많이 가져가고 기술카드를 조합해서 콤보를 사용을 할 수 있어서 조심해야해!',
            '이 도장에서는 3명과 싸워야하고 첫 카드를 제외하고 모든 카드를 같은 수만큼 플레이어들에게 분배가 돼. 이 도장에서는 카드를 빨리 소모하는 것이 승리의 관건이야.',
            '2명의 상대와 대전하고 5턴마다 낼 수 있는 카드의 색상이 무작위로 변경되야해서 주의해야해!',
            '이 곳에서는 쉴드 카드를 사용할 수 없게 되고, 새로운 공격카드가 추가되고 카드가 일정 매수가 넘어가면 게임오버가 되니까 주의해야 해!']

        # 버튼
        self.buttons = [Button(self.screen.get_width() * 0.07,
                               self.screen.get_height() * 0.06,
                               self.ui_size["button"][0],
                               self.ui_size["button"][1],
                               self.screen,
                               0xffffff,
                               "뒤로 가기",
                               self.ui_size["font"][1],
                               on_click_function=self.event_quit),
                        ImageButton(self.screen.get_width() * 0.15,
                                    self.screen.get_height() * 0.3,
                                    self.ui_size["stage_button"][0],
                                    self.ui_size["stage_button"][1],
                                    self.screen,
                                    "./resources/image/story_image/storygym_1.png",
                                    on_click_function=self.event_stage_1_popup)]

        self.clear_flags = []
        clear_flag = pygame.transform.scale(
            (pygame.image.load("./resources/Image/story_image/clear_mark.png")),
            (self.ui_size["stage_button"][0] * 0.95, self.ui_size["stage_button"][1] * 0.5))

        # 클리어 체크 후 버튼 표시 및 클리어 여부 표시
        if self.clear_data["1st"] > 0:
            self.buttons.append(ImageButton(self.screen.get_width() * 0.2,
                                            self.screen.get_height() * 0.67,
                                            self.ui_size["stage_button"][0],
                                            self.ui_size["stage_button"][1],
                                            self.screen,
                                            "./resources/image/story_image/storygym_2.png",
                                            on_click_function=self.event_stage_2_popup))
            self.clear_flags.append(clear_flag)
        if self.clear_data["2nd"] > 0:
            self.buttons.append(ImageButton(self.screen.get_width() * 0.45,
                                            self.screen.get_height() * 0.35,
                                            self.ui_size["stage_button"][0],
                                            self.ui_size["stage_button"][1],
                                            self.screen,
                                            "./resources/image/story_image/storygym_3.png",
                                            on_click_function=self.event_stage_3_popup))
            self.clear_flags.append(clear_flag)
        if self.clear_data["3rd"] > 0:
            self.buttons.append(ImageButton(self.screen.get_width() * 0.5,
                                            self.screen.get_height() * 0.72,
                                            self.ui_size["stage_button"][0],
                                            self.ui_size["stage_button"][1],
                                            self.screen,
                                            "./resources/image/story_image/storygym_4.png",
                                            on_click_function=self.event_stage_4_popup))
            self.clear_flags.append(clear_flag)
        if self.clear_data["4th"] > 0:
            self.clear_flags.append(clear_flag)

        # 클릭한 버튼ㅅ index를 저장하는 변수
        self.selected_stage_number = 0

        # 팝업 초기 설정
        self.popup = Popup(self.screen.get_width() // 2,
                           self.screen.get_height() // 2,
                           self.screen.get_width() * 0.4,
                           self.screen.get_height() * 0.4,
                           self.screen,
                           '스테이지에 정말 입장하시겠습니까?',
                           self.ui_size["font"][1],
                           self.event_stage_entry)

        # 키보드로 선택한 버튼 index 변수
        self.selected_button_index = 0
        self.buttons[self.selected_button_index].keyboard_selected = True

    def event_quit(self):
        print('캠페인 맵 메뉴에서 나가기 버튼 클릭 됨')
        self.running = False

    def event_stage_entry(self):
        self.popup.pop = False
        # if self.selected_stage_number == 1:
        #     stage_1 = StageA()
        #     stage_1.run()
        # elif self.selected_stage_number == 2:
        #     stage_2 = StageB()
        #     stage_2.run()
        # elif self.selected_stage_number == 3:
        #     stage_3 = StageC()
        #     stage_3.run()
        # else:
        #     stage_4 = StageD()
        #     stage_4.run()

    def event_stage_1_popup(self):
        print('1스테이지 입장버튼 클릭됨')
        self.selected_stage_number = 1
        self.popup.pop = True

    def event_stage_2_popup(self):
        print('2스테이지 입장버튼 클릭됨')
        self.selected_stage_number = 2
        self.popup.pop = True

    def event_stage_3_popup(self):
        print('3스테이지 입장버튼 클릭됨')
        self.selected_stage_number = 3
        self.popup.pop = True

    def event_stage_4_popup(self):
        print('4스테이지 입장버튼 클릭됨')
        self.selected_stage_number = 4
        self.popup.pop = True

    def draw(self):
        # 배경 색상
        self.screen.fill((255, 255, 255))

        # 설명창 영역
        self.screen.blit(self.description_section, (self.screen.get_width() * 0.65, 0))

        # 스테이지 이름
        title = self.font_title.render(self.text_title[self.selected_button_index], True, pygame.Color('white'))
        self.screen.blit(title, (self.screen.get_width() * 0.67, self.screen.get_height() * 0.2))

        # 스테이지 설명
        self.blit_text(self.screen, self.text_description[self.selected_button_index],
                       (self.screen.get_width() * 0.67, self.screen.get_height() * 0.4), self.font_description,
                       pygame.Color('white'))

        # 버튼 표시
        for button in self.buttons:
            button.draw()
            # 팝업이 떠 있지 않을 경우 버튼 선택 가능
            if not self.popup.pop:
                button.detect_event()

        # 클리어 스테이지 표시
        for i in range(0, len(self.clear_flags)):
            self.screen.blit(self.clear_flags[i],
                             self.clear_flags[i].get_rect(x=self.buttons[i + 1].x * 1.05,
                                                          y=self.buttons[i + 1].y * 1.1))

        self.screen.blit(self.buttons[self.selected_button_index].selected_image,
                         self.buttons[self.selected_button_index].rect)

        # 선택되면 팝업 띄우고 바깥은 비활성화
        if self.popup.pop:
            self.popup.open()

        # 매 프레임마다 화면 업데이트
        pygame.display.flip()

    # 자동 개행 text 함수
    def blit_text(self, surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and self.popup.pop == False:
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
            self.event()
            self.draw()
