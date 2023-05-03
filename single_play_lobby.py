import pygame
import pickle

from single_game import SingleGame
from mouse import Mouse, MouseState
from ui.button import Button
from option import save_option as save
from option import basic_option as basic


class Lobby:
    def __init__(self):
        # 저장된 설정 불러오기, 만약 파일이 비어있다면 기본 설정으로 세팅
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
        self.screen = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption(basic.game_title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font("./resources/maplestory_font.ttf", self.font_size[0])
        self.small_font = pygame.font.Font("./resources/maplestory_font.ttf", self.font_size[1])

        if self.display_size[0] == 1920:
            # 컴퓨터 이미지 가져오기
            self.computer1_img = pygame.image.load("./resources/Image/lobby_images/big/computer1.png").convert_alpha()
            self.computer2_img = pygame.image.load("./resources/Image/lobby_images/big/computer2.png").convert_alpha()
            self.computer3_img = pygame.image.load("./resources/Image/lobby_images/big/computer3.png").convert_alpha()
            self.computer4_img = pygame.image.load("./resources/Image/lobby_images/big/computer4.png").convert_alpha()
            self.computer5_img = pygame.image.load("./resources/Image/lobby_images/big/computer5.png").convert_alpha()
            self.enter_img = pygame.image.load("./resources/Image/lobby_images/big/computer_enter.png").convert_alpha()
            self.start_img = pygame.image.load("./resources/Image/lobby_images/big/game_start.png").convert_alpha()
        elif self.display_size[0] == 1600:
            self.computer1_img = pygame.image.load("./resources/Image/lobby_images/middle/computer1.png").convert_alpha()
            self.computer2_img = pygame.image.load("./resources/Image/lobby_images/middle/computer2.png").convert_alpha()
            self.computer3_img = pygame.image.load("./resources/Image/lobby_images/middle/computer3.png").convert_alpha()
            self.computer4_img = pygame.image.load("./resources/Image/lobby_images/middle/computer4.png").convert_alpha()
            self.computer5_img = pygame.image.load("./resources/Image/lobby_images/middle/computer5.png").convert_alpha()
            self.enter_img = basic.scale_by(pygame.image.load("./resources/Image/lobby_images/middle/computer_enter.png").convert_alpha(), basic.change_size[1])
            self.start_img = basic.scale_by(pygame.image.load("./resources/Image/lobby_images/middle/game_start.png").convert_alpha(), basic.change_size[1])
        else:
            self.computer1_img = pygame.image.load("./resources/Image/lobby_images/small/computer1.png").convert_alpha()
            self.computer2_img = pygame.image.load("./resources/Image/lobby_images/small/computer2.png").convert_alpha()
            self.computer3_img = pygame.image.load("./resources/Image/lobby_images/small/computer3.png").convert_alpha()
            self.computer4_img = pygame.image.load("./resources/Image/lobby_images/small/computer4.png").convert_alpha()
            self.computer5_img = pygame.image.load("./resources/Image/lobby_images/small/computer5.png").convert_alpha()
            self.enter_img = basic.scale_by(pygame.image.load("./resources/Image/lobby_images/small/computer_enter.png").convert_alpha(), basic.change_size[2])
            self.start_img = basic.scale_by(pygame.image.load("./resources/Image/lobby_images/small/game_start.png").convert_alpha(), basic.change_size[2])

        # 이미지 크기 가져오기
        self.computer1_size = self.computer1_img.get_size()
        self.computer2_size = self.computer2_img.get_size()
        self.computer3_size = self.computer3_img.get_size()
        self.computer4_size = self.computer4_img.get_size()
        self.computer5_size = self.computer5_img.get_size()
        self.start_img_size = self.start_img.get_size()

        self.computer1_attend = False
        self.computer2_attend = False
        self.computer3_attend = False
        self.computer4_attend = False
        self.computer5_attend = False

        # 화면 크기 정보 가져옴
        self.screen = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption(basic.game_title)
        self.clock = pygame.time.Clock()
        self.running = True

        if self.display_size[0] == 1920:
            self.computer1_coordinate = (self.display_size[0]-500, 0)
            self.computer2_coordinate = (self.display_size[0]-500, 220)
            self.computer3_coordinate = (self.display_size[0]-500, 440)
            self.computer4_coordinate = (self.display_size[0]-500, 660)
            self.computer5_coordinate = (self.display_size[0]-500, 880)
            self.start_coordinate = (self.display_size[0]/2 - self.start_img_size[0]/2, self.display_size[1]/2- self.start_img_size[1]/2)
        elif self.display_size[0] == 1600:
            self.computer1_coordinate = (self.display_size[0]-300, 0)
            self.computer2_coordinate = (self.display_size[0]-300, 170)
            self.computer3_coordinate = (self.display_size[0]-300, 340)
            self.computer4_coordinate = (self.display_size[0]-300, 510)
            self.computer5_coordinate = (self.display_size[0]-300, 680)
            self.start_coordinate = (self.display_size[0]/2 - self.start_img_size[0]/2, self.display_size[1]/2- self.start_img_size[1]/2)
        else:
            self.computer1_coordinate = (self.display_size[0]-300, 0)
            self.computer2_coordinate = (self.display_size[0]-300, 130)
            self.computer3_coordinate = (self.display_size[0]-300, 260)
            self.computer4_coordinate = (self.display_size[0]-300, 390)
            self.computer5_coordinate = (self.display_size[0]-300, 520)
            self.start_coordinate = (self.display_size[0]/2 - self.start_img_size[0]/2, self.display_size[1]/2- self.start_img_size[1]/2)

        # 이름 변경 버튼
        self.change_name_button = Button(self.display_size[0] // 2, self.display_size[1] // 4, self.button_size[0],
                                         self.button_size[1], 'User 이름 변경', self.change_name_event, self.font_size[1])
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
                single_game = SingleGame(computer_attends, self.name)
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
