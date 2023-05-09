import pygame

from controller import game_data_controller, game_view_controller
from controller.mouse_controller import Mouse, MouseState
from ui.button import Button, ImageButton

from scene.single_play_legacy import SinglePlay
from scene.story_mode_stage import StageA, StageB, StageC
from scene.single_play import SinglePlay

class Lobby:
    def __init__(self):
        # 게임 설정 불러오기
        self.settings_data = game_data_controller.load_settings_data()

        # pygame 초기화
        pygame.init()
        pygame.display.set_caption(game_view_controller.GAME_TITLE + ": Single Play Lobby")
        self.ui_size = game_view_controller.set_size(self.settings_data["resolution"]["width"])
        self.screen = pygame.display.set_mode((self.settings_data["resolution"]["width"],
                                               self.settings_data["resolution"]["height"]))
        self.clock = pygame.time.Clock()
        self.running = True

        # 글꼴 설정
        self.font = pygame.font.Font(game_view_controller.FONT_PATH, self.ui_size["font"][0])
        self.small_font = pygame.font.Font(game_view_controller.FONT_PATH, self.ui_size["font"][1])

        # 컴퓨터 추가 버튼
        self.buttons_computer = [ImageButton(self.screen.get_width() * 0.7,
                                             self.screen.get_height() * 0.2,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/big/computer1.png",
                                             on_click_function=self.event_join_ai_player),
                                 ImageButton(self.screen.get_width() * 0.7,
                                             self.screen.get_height() * 0.4,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/big/computer2.png",
                                             on_click_function=self.event_join_ai_player),
                                 ImageButton(self.screen.get_width() * 0.7,
                                             self.screen.get_height() * 0.6,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/big/computer3.png",
                                             on_click_function=self.event_join_ai_player),
                                 ImageButton(self.screen.get_width() * 0.7,
                                             self.screen.get_height() * 0.8,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/big/computer4.png",
                                             on_click_function=self.event_join_ai_player),
                                 ImageButton(self.screen.get_width() * 0.7,
                                             self.screen.get_height() * 1,
                                             self.screen.get_width() // 6,
                                             self.screen.get_height() // 6,
                                             self.screen,
                                             "./resources/Image/lobby_images/big/computer5.png",
                                             on_click_function=self.event_join_ai_player)]

        self.button_start = ImageButton(self.screen.get_width() // 2,
                                        self.screen.get_height() // 2,
                                        self.screen.get_width() // 4,
                                        self.screen.get_height() // 4,
                                        self.screen,
                                        "./resources/Image/lobby_images/big/computer5.png",
                                        on_click_function=self.event_start)

        self.computer1_attend = False
        self.computer2_attend = False
        self.computer3_attend = False
        self.computer4_attend = False
        self.computer5_attend = False

        # 이름 변경 버튼
        self.change_name_button = Button(self.display_size[0] // 2, self.display_size[1] // 4, self.button_size[0],
                                         self.button_size[1], 'User 이름 변경', self.change_name_event, self.ui_size["font"][1])
        self.name = "You"
        self.name_display = self.font.render("User name : " + self.name, True, (0, 0, 0))

    def change_name_event(self):
        self.name = ""
        popup = self.font.render("바꿀 이름을 입력하고 " + pygame.key.name(save.key_setting['enter']) + "키를 입력하시오.", True, (0, 0, 0))
        self.screen.fill((255, 255, 255))
        self.screen.blit(popup, (self.screen.get_width() // 2 - popup.get_size()[0] // 2,
                                 self.screen.get_height() // 2))
        pygame.display.flip()
        popup_running = True
        while popup_running:
            for popup_event in pygame.event.get():
                if popup_event.type == pygame.KEYDOWN:
                    if popup_event.key == self.key_setting['enter']:
                        popup_running = False
                        break
                    self.name = self.name + pygame.key.name(popup_event.key)

    def check_computer_click(self):
        mouse_x, mouse_y = Mouse.getMousePos()
        mouse_state = Mouse.getMouseState()

        computer_numbers = [1, 2, 3, 4, 5]
        for i in computer_numbers:
            computer_coordinate = getattr(self, f"computer{i}_coordinate")
            computer_size = getattr(self, f"computer{i}_size")

            if (computer_coordinate[0] <= mouse_x <= computer_coordinate[0] + computer_size[0]
                    and computer_coordinate[1] <= mouse_y <= computer_coordinate[1] + computer_size[1]):
                if mouse_state == MouseState.CLICK:
                    print(f"Computer {i} clicked")
                    current_attend_status = getattr(self, f"computer{i}_attend")
                    setattr(self, f"computer{i}_attend", not current_attend_status)
                    break

    def all_computers_unattended(self):
        computer_numbers = [1, 2, 3, 4, 5]
        for i in computer_numbers:
            if getattr(self, f"computer{i}_attend"):
                return False
        return True

    def check_start_click(self):
        mouse_x, mouse_y = Mouse.getMousePos()
        mouse_state = Mouse.getMouseState()

        if (self.start_coordinate[0] <= mouse_x <= self.start_coordinate[0] + self.start_img_size[0]
                and self.start_coordinate[1] <= mouse_y <= self.start_coordinate[1] + self.start_img_size[1]):
            if mouse_state == MouseState.CLICK and not self.all_computers_unattended():
                print("Start game")
                computer_attends = [self.computer1_attend, self.computer2_attend, self.computer3_attend,
                                    self.computer4_attend, self.computer5_attend]
<<<<<<< HEAD:scene/single_play_lobby.py
                single_game = SinglePlay(computer_attends, self.name)
=======
                single_game = SingleGameYhj(computer_attends, self.name)
>>>>>>> main:single_play_lobby.py
                single_game.run()
                self.running = False

    def draw(self):
        self.screen.fill((111, 111, 111))
        self.screen.blit(self.computer1_img, self.computer1_coordinate)
        self.screen.blit(self.computer2_img, self.computer2_coordinate)
        self.screen.blit(self.computer3_img, self.computer3_coordinate)
        self.screen.blit(self.computer4_img, self.computer4_coordinate)
        self.screen.blit(self.computer5_img, self.computer5_coordinate)

        if self.computer1_attend:
            self.screen.blit(self.enter_img, self.computer1_coordinate)
        if self.computer2_attend:
            self.screen.blit(self.enter_img, self.computer2_coordinate)
        if self.computer3_attend:
            self.screen.blit(self.enter_img, self.computer3_coordinate)
        if self.computer4_attend:
            self.screen.blit(self.enter_img, self.computer4_coordinate)
        if self.computer5_attend:
            self.screen.blit(self.enter_img, self.computer5_coordinate)

        if not self.all_computers_unattended():
            self.screen.blit(self.start_img, self.start_coordinate)

        self.change_name_button.process()
        self.screen.blit(self.change_name_button.surface, self.change_name_button.rect)

        self.name_display = self.font.render("User name : " + self.name, True, (0, 0, 0))
        self.screen.blit(self.name_display, (100, 100))

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            Mouse.updateMouseState()
            self.clock.tick(basic.fps)
            self.draw()
            self.check_computer_click()
            self.check_start_click()  # start_img 클릭 확인
