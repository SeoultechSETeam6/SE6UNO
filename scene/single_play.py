import pygame
import random
import time

from ui.button import Button

from scene.settings import Settings

from controller.mouse import Mouse, MouseState
from controller.card_gen import generate_cards, generate_for_change_cards
from controller.card_shuffle import shuffle_cards, distribute_cards
from controller.game_utils import (
    draw_cards_user,
    draw_cards_ai,
    draw_change_card,
    find_hovered_card,
    find_hovered_change,
    draw_text,
    get_clicked_card,
    get_clicked_change,
    draw_button,
    get_top_card,
    draw_board_card,
    is_valid_move,
    computer_playable_card,
    user_submit_card,
    com_submit_card,
    apply_special_card_effects,
    decide_computer_play,
    card_reshuffle
)

from controller import game_view, game_data


class SinglePlay:
    def __init__(self, computer_attends, username, computer_logic):
        # 게임 설정 불러오기
        self.settings_data = game_data.load_settings()

        # pygame 초기화
        pygame.init()
        pygame.display.set_caption(game_view.GAME_TITLE + ": Single Play")
        self.ui_size = game_view.set_size(self.settings_data["resolution"]["width"])
        self.screen = pygame.display.set_mode((self.settings_data["resolution"]["width"],
                                               self.settings_data["resolution"]["height"]))
        self.clock = pygame.time.Clock()
        self.running = True

        # 글꼴 설정
        self.font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][0])
        self.small_font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][1])

        # single_game 변수
        self.player_count = 1  # 플레이어 수
        self.card_count = 7  # 처음 시작하는 카드 수

        # 텍스트 설정
        # 플레이어 이름
        self.text_player_name = self.font.render(username, True, (0, 0, 0))
        self.text_computer_name = [self.small_font.render("Computer1", True, (0, 0, 0)),
                                   self.small_font.render("Computer2", True, (0, 0, 0)),
                                   self.small_font.render("Computer3", True, (0, 0, 0)),
                                   self.small_font.render("Computer4", True, (0, 0, 0)),
                                   self.small_font.render("Computer5", True, (0, 0, 0))]

        # 컴퓨터 플레이어 참여 정보
        self.computer_attends = computer_attends
        self.computer_logic = computer_logic
        for attend in self.computer_attends:
            if attend:
                self.player_count += 1

        # 게임 이미지
        self.pause_button_img = game_view.scale_by(pygame.image.load("./resources/Image/button_images/pause.png").convert_alpha(), self.ui_size["change"])
        self.resume_button_img = game_view.scale_by(pygame.image.load("./resources/Image/button_images/resume.png").convert_alpha(), self.ui_size["change"])
        self.direction_img = game_view.scale_by(pygame.image.load("./resources/Image/direction_images/direction.png").convert_alpha(), self.ui_size["change"])
        self.direction_reverse_img = game_view.scale_by(pygame.image.load(
            "./resources/Image/direction_images/direction_reverse.png").convert_alpha(), self.ui_size["change"])
        self.turn_arrow_img = game_view.scale_by(pygame.image.load("./resources/Image/direction_images/turn_arrow.png").convert_alpha(), self.ui_size["change"])
        self.next_turn_button_img = game_view.scale_by(pygame.image.load("./resources/Image/button_images/next_turn.png").convert_alpha(), self.ui_size["change"])
        self.uno_button_img = game_view.scale_by(pygame.image.load("./resources/Image/button_images/uno_button.png").convert_alpha(), self.ui_size["change"])
        self.uno_button_inactive_img = game_view.scale_by(pygame.image.load(
            "./resources/Image/button_images/uno_button_inactive.png").convert_alpha(), self.ui_size["change"])
        self.card_back_image = game_view.scale_by(pygame.image.load("resources/Image/card_images/card_back.png"), self.ui_size["change"])
        self.selected_image = game_view.scale_by(pygame.image.load("./resources/Image/selected_check.png"), self.ui_size["change"] * 0.2)

        # 배경 음악
        self.background_music = pygame.mixer.Sound("./resources/Music/single_mode_play.ogg")

        # 효과음
        self.sound_card_distribution = pygame.mixer.Sound("./resources/SoundEffect/carddistribution_sound.ogg")
        self.sound_card_place = pygame.mixer.Sound("./resources/SoundEffect/cardplace_sound.ogg")
        self.sound_shuffle = pygame.mixer.Sound("./resources/SoundEffect/cardshuffle_sound.ogg")
        self.sound_uno_button = pygame.mixer.Sound("./resources/SoundEffect/Unobutton_sound.ogg")

        # 카드 생성 및 셔플
        self.cards = generate_cards(self.settings_data["color_weakness"], self.ui_size["change"])
        self.shuffled_cards = shuffle_cards(self.cards)

        # 카드 분배, 유저는 player_hands[0]이고, 나머지는 인공지능으로 설정한다. change는 카드 체인지를 위한 카드들.
        self.player_hands, self.remain_cards = distribute_cards(self.shuffled_cards, self.player_count, self.card_count)
        self.change_color_list = generate_for_change_cards(self.settings_data["color_weakness"], self.ui_size["change"])

        # 초기 플레이어 순서를 위한 설정 값.
        self.current_player = (random.randint(0, self.player_count - 1))
        # 게임 순서 방향 (1: 정방향, -1: 역방향)
        self.game_direction = 1

        # 보드에 뒤집힌 카드 설정 (카드 한 장을 뽑아서 남은 카드 덱 옆에 보이게 놓기)
        self.board_card = [self.remain_cards.pop()]

        # 기타 정보
        self.paused = False  # 일시정지 초기값
        self.game_over = False  # 게임 오버 초기값
        self.top_card = None  # board 카드 맨 위
        self.user_turn = False

        # 턴 시간
        self.time_limit = 10000  # 유저의 턴 시간 제한
        self.current_time = pygame.time.get_ticks()  # 현재 시간
        self.turn_start_time = None  # 턴 시작 시간
        self.is_draw = False # 드로우한 시간인지 아닌지 구분
        self.delay_time = random.randint(1000, 2000)  # 컴퓨터 딜레이 타임1
        self.delay_time2 = random.randint(900, 2000)  # 컴퓨터 딜레이 타임2
        self.delay_time3 = random.randint(900, 2000)  # 컴퓨터 딜레이 타임3

        # 화면 중앙 좌표 계산
        self.image_width, self.image_height = self.direction_img.get_size()
        self.center_x = (self.settings_data["resolution"]["width"] - self.image_width) // 2
        self.center_y = (self.settings_data["resolution"]["height"] - self.image_height) // 2

        self.select_color = ["red", "blue", "green", "yellow"]

        # 컴퓨터 초기 좌표와 카드 색 선호도.
        self.user_coordinate = []
        self.computer_coordinate = []
        self.computer_color = [None]
        self.max_per_row = 15 * self.ui_size["change"]
        self.max_per_row_com = 20 * self.ui_size["change"]
        self.user_coordinate.append(30)
        self.user_coordinate.append(self.settings_data["resolution"]["height"] * 0.7)
        self.user_spacing = self.settings_data["resolution"]["height"] * 0.08
        self.turn_coordinate = [70, 150 * self.ui_size["change"], 150 * self.ui_size["change"], 80]
        self.next_turn_co = [0, 150 * self.ui_size["change"]]
        if self.computer_attends[0]:
            self.computer_coordinate.append([self.settings_data["resolution"]["width"] * 0.65, self.settings_data["resolution"]["height"] * 0.03])
            self.computer1_color = self.select_color[random.randint(0, 3)]
            self.computer_color.append(self.computer1_color)
        if self.computer_attends[1]:
            self.computer_coordinate.append([self.settings_data["resolution"]["width"] * 0.65, (self.settings_data["resolution"]["height"] * 0.03) + self.settings_data["resolution"]["height"] * 0.2])
            self.computer2_color = self.select_color[random.randint(0, 3)]
            self.computer_color.append(self.computer2_color)
        if self.computer_attends[2]:
            self.computer_coordinate.append([self.settings_data["resolution"]["width"] * 0.65, (self.settings_data["resolution"]["height"] * 0.03) + (self.settings_data["resolution"]["height"] * 0.4)])
            self.computer3_color = self.select_color[random.randint(0, 3)]
            self.computer_color.append(self.computer3_color)
        if self.computer_attends[3]:
            self.computer_coordinate.append([self.settings_data["resolution"]["width"] * 0.65, (self.settings_data["resolution"]["height"] * 0.03) + (self.settings_data["resolution"]["height"] * 0.6)])
            self.computer4_color = self.select_color[random.randint(0, 3)]
            self.computer_color.append(self.computer4_color)
        if self.computer_attends[4]:
            self.computer_coordinate.append([self.settings_data["resolution"]["width"] * 0.65, (self.settings_data["resolution"]["height"] * 0.03) + (self.settings_data["resolution"]["height"] * 0.8)])
            self.computer5_color = self.select_color[random.randint(0, 3)]
            self.computer_color.append(self.computer5_color)
        print("computer color list", self.computer_color)

        # change카드 좌표, spacing은 공백
        self.x5 = 100
        self.y5 = 100
        self.spacing5 = 200
        # 플레이어들이 카드를 뽑고 남은 카드들의 위치를 잡는데 사용
        self.remain_cards_x_position = (self.screen.get_rect().centerx - 151 * self.ui_size["change"])
        self.remain_cards_y_position = (self.screen.get_rect().centery - 75 * self.ui_size["change"])
        self.remain_pos = pygame.Vector2(self.screen.get_rect().centerx, self.screen.get_rect().centery - 151 * self.ui_size["change"])
        # remain카드
        self.remain_cards_rect = self.remain_cards[0].card_img_back.get_rect()
        self.remain_cards_rect.topleft = (self.remain_cards_x_position, self.remain_cards_y_position)
        # pause버튼
        self.pause_button_rect = self.pause_button_img.get_rect()
        self.pause_button_rect.topleft = (25, 25)
        # next_turn버튼
        self.next_turn_button_rect = self.next_turn_button_img.get_rect()
        self.next_turn_button_rect.topleft = (self.user_coordinate[0] - self.next_turn_co[0], self.user_coordinate[1] - self.next_turn_co[1])
        # uno_button
        self.uno_button_rect = self.uno_button_img.get_rect()
        self.uno_button_rect.topleft = (150, self.settings_data["resolution"]["height"] * 0.5)
        self.uno_button_inactive_rect = self.uno_button_inactive_img.get_rect()
        self.uno_button_inactive_rect.topleft = (150, self.settings_data["resolution"]["height"] * 0.5)
        self.play_drawn_card_button = pygame.Rect(0, 0, 430, 110)
        # animation 메소드 모음
        self.animation_method = {"reverse": self.reverse_animation, "skip": self.skip_animation,
                                 "draw_2": self.draw_2_animation, "bomb": self.bomb_animation,
                                 "shield": self.shield_animation, "change": self.change_animation,
                                 "one_more": self.one_more_animation}

        # Pause Button Check
        self.alreadyPressed = False
        self.hovered_card_index = 0
        self.hovered_change_index = 0

        # 어떤 스테이지에서 게임을 진행하는지?
        self.stage = "single"

        # uno 초기값
        self.uno_check = False
        self.uno_delay_time = None
        self.uno_current_time = None
        self.uno_flags = [False, False, False, False, False, False]

        self.remaining_time = None
        self.remaining_time_text = None
        self.after_draw_remaining_time = None
        self.after_draw_remaining_time_text = None
        self.pause_start_time = None

        self.change_card = False
        self.clicked_card_index = None
        self.clicked_change_index = None
        self.change_index = None
        self.playable = False
        self.playable_special_check = False
        self.clicked_change = False
        self.color_change = None

        self.pop_card = None  # 뽑은 카드 초기값
        self.pop_card_index = None  # 뽑은 카드 인덱스 숫자 초기값
        self.new_drawn_card = None  # draw한 카드가 어떤 카드인가의 초기값

        self.clicked_card = None  # 클릭 카드 초기값
        self.clicked_remain_cards = False  # remain_cards 클릭 여부 초기값
        self.clicked_next_turn_button = False  # 다음턴 클릭여부 초기값

        self.turn_count = 1

        # 0: 드로우, 1: 우노버튼, 2: 턴 넘기기, 3. 덱
        self.key_select_option = 3

    def reload_card(self, deck):
        for card in deck:
            if self.settings_data["color_weakness"]:
                card.card_img = game_view.scale_by(card.image_cw, self.ui_size["change"])
            else:
                card.card_img = game_view.scale_by(card.image, self.ui_size["change"])
            card.card_img_back = game_view.scale_by(card.image_back, self.ui_size["change"])

    def setting(self):
        self.settings_data = game_data.load_settings()
        self.ui_size = game_view.set_size(self.settings_data["resolution"]["width"])

        self.font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][0])
        self.small_font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][1])

        self.screen = pygame.display.set_mode((self.settings_data["resolution"]["width"],
                                               self.settings_data["resolution"]["height"]))

        # 게임 이미지를 로드
        self.pause_button_img = game_view.scale_by(
            pygame.image.load("./resources/Image/button_images/pause.png").convert_alpha(), self.ui_size["change"])
        self.resume_button_img = game_view.scale_by(
            pygame.image.load("./resources/Image/button_images/resume.png").convert_alpha(), self.ui_size["change"])
        self.direction_img = game_view.scale_by(
            pygame.image.load("./resources/Image/direction_images/direction.png").convert_alpha(), self.ui_size["change"])
        self.direction_reverse_img = game_view.scale_by(pygame.image.load(
            "./resources/Image/direction_images/direction_reverse.png").convert_alpha(), self.ui_size["change"])
        self.turn_arrow_img = game_view.scale_by(
            pygame.image.load("./resources/Image/direction_images/turn_arrow.png").convert_alpha(), self.ui_size["change"])
        self.next_turn_button_img = game_view.scale_by(
            pygame.image.load("./resources/Image/button_images/next_turn.png").convert_alpha(), self.ui_size["change"])
        self.uno_button_img = game_view.scale_by(
            pygame.image.load("./resources/Image/button_images/uno_button.png").convert_alpha(), self.ui_size["change"])
        self.uno_button_inactive_img = game_view.scale_by(pygame.image.load(
            "./resources/Image/button_images/uno_button_inactive.png").convert_alpha(), self.ui_size["change"])
        self.card_back_image = game_view.scale_by(pygame.image.load("./resources/Image/card_images/card_back.png"),
                                                  self.ui_size["change"])
        self.selected_image = game_view.scale_by(pygame.image.load("./resources/Image/selected_check.png"),
                                                 self.ui_size["change"] * 0.2)

        # 색변경 카드 사용시 None 나오는거 경로가 다름
        # 카드 크기 줄이기
        self.reload_card(self.change_color_list)
        self.reload_card(self.remain_cards)
        self.reload_card(self.board_card)
        for i in range(self.player_count):
            self.reload_card(self.player_hands[i])

        # 화면 중앙 좌표 계산
        self.image_width, self.image_height = self.direction_img.get_size()
        self.center_x = (self.settings_data["resolution"]["width"] - self.image_width) // 2
        self.center_y = (self.settings_data["resolution"]["height"] - self.image_height) // 2

        # 컴퓨터 초기 좌표와 카드 색 선호도.
        self.user_coordinate = []
        self.computer_coordinate = []
        self.max_per_row = 15 * self.ui_size["change"]
        self.max_per_row_com = 20 * self.ui_size["change"]
        self.user_coordinate.append(30)
        self.user_coordinate.append(self.settings_data["resolution"]["height"] * 0.7)
        self.user_spacing = self.settings_data["resolution"]["height"] * 0.08
        self.turn_coordinate = [70, 150 * self.ui_size["change"], 150 * self.ui_size["change"], 80]
        self.next_turn_co = [0, 150 * self.ui_size["change"]]
        if self.computer_attends[0]:
            self.computer_coordinate.append([self.settings_data["resolution"]["width"] * 0.65, self.settings_data["resolution"]["height"] * 0.03])
        if self.computer_attends[1]:
            self.computer_coordinate.append([self.settings_data["resolution"]["width"] * 0.65, (self.settings_data["resolution"]["height"] * 0.03) + self.settings_data["resolution"]["height"] * 0.2])
        if self.computer_attends[2]:
            self.computer_coordinate.append([self.settings_data["resolution"]["width"] * 0.65, (self.settings_data["resolution"]["height"] * 0.03) + (self.settings_data["resolution"]["height"] * 0.4)])
        if self.computer_attends[3]:
            self.computer_coordinate.append([self.settings_data["resolution"]["width"] * 0.65, (self.settings_data["resolution"]["height"] * 0.03) + (self.settings_data["resolution"]["height"] * 0.6)])
        if self.computer_attends[4]:
            self.computer_coordinate.append([self.settings_data["resolution"]["width"] * 0.65, (self.settings_data["resolution"]["height"] * 0.03) + (self.settings_data["resolution"]["height"] * 0.8)])

        # change카드 좌표, spacing은 공백
        self.x5 = 100
        self.y5 = 100
        self.spacing5 = 200
        # 플레이어들이 카드를 뽑고 남은 카드들의 위치를 잡는데 사용
        self.remain_cards_x_position = (self.screen.get_rect().centerx - 151 * self.ui_size["change"])
        self.remain_cards_y_position = (self.screen.get_rect().centery - 75 * self.ui_size["change"])
        self.remain_pos = pygame.Vector2(self.screen.get_rect().centerx, self.screen.get_rect().centery - 151 * self.ui_size["change"])
        # remain카드
        self.remain_cards_rect = self.remain_cards[0].card_img_back.get_rect()
        self.remain_cards_rect.topleft = (self.remain_cards_x_position, self.remain_cards_y_position)
        # pause버튼
        self.pause_button_rect = self.pause_button_img.get_rect()
        self.pause_button_rect.topleft = (25, 25)
        # next_turn버튼
        self.next_turn_button_rect = self.next_turn_button_img.get_rect()
        self.next_turn_button_rect.topleft = (
        self.user_coordinate[0] - self.next_turn_co[0], self.user_coordinate[1] - self.next_turn_co[1])
        # uno_button
        self.uno_button_rect = self.uno_button_img.get_rect()
        self.uno_button_rect.topleft = (150, self.settings_data["resolution"]["height"] * 0.5)
        self.uno_button_inactive_rect = self.uno_button_inactive_img.get_rect()
        self.uno_button_inactive_rect.topleft = (150, self.settings_data["resolution"]["height"] * 0.5)
        self.play_drawn_card_button = pygame.Rect(0, 0, 430, 110)

    def reset(self):
        self.is_draw = False

        self.turn_start_time = None

        self.change_card = False
        self.clicked_card_index = None
        self.clicked_change_index = None
        self.change_index = None
        self.playable = False
        self.playable_special_check = False
        self.clicked_change = False
        self.color_change = None

        self.pop_card = None  # 뽑은 카드 초기값
        self.pop_card_index = None  # 뽑은 카드 인덱스 숫자 초기값
        self.new_drawn_card = None  # draw한 카드가 어떤 카드인가의 초기값

        self.clicked_card = None  # 클릭 카드 초기값
        self.clicked_remain_cards = False  # remain_cards 클릭 여부 초기값
        self.clicked_next_turn_button = False  # 다음턴 클릭여부 초기값

    def check_reshuffle_method(self):
        self.turn_count = self.turn_count + 1
        if self.turn_count % 10 == 0:
            self.sound_shuffle.set_volume(
                self.settings_data["volume"]["sound"] * self.settings_data["volume"]["background"])
            self.sound_shuffle.play(1)
            self.board_card, self.remain_cards = card_reshuffle(self.board_card, self.remain_cards)

    def turn_end_method(self):
        self.reset()
        self.check_reshuffle_method()

    def game(self):
        # 마우스의 위치를 가져옴
        mouse_x, mouse_y = Mouse.getMousePos()
        # 현재 플레이어 결정
        self.top_card = get_top_card(self.board_card)

        # 플레이어턴, 컴퓨터턴 결정
        if self.current_player == 0:
            self.user_turn = True
        else:
            self.user_turn = False

        # 플레이어, 컴퓨터 메소드 호출
        if self.user_turn:
            self.user_turn_method()  # 여기서 user_turn_method 메소드를 호출
        else:
            self.computer_turn_method()

        if Mouse.getMouseState() == MouseState.CLICK:
            if self.uno_button_rect.collidepoint(mouse_x, mouse_y) and self.uno_check:
                self.sound_uno_button.set_volume(self.settings_data["volume"]["sound"] * self.settings_data["volume"]["effect"])
                self.sound_uno_button.play(1)
                self.uno_flags[self.current_player] = True

        if self.uno_check:
            return

        self.hovered_card_index = find_hovered_card(self.player_hands[0], self.user_coordinate[0],
                                                    self.user_coordinate[1], self.user_spacing, mouse_x, mouse_y,
                                                    self.max_per_row, self.hovered_card_index)
        self.hovered_change_index = find_hovered_change(self.change_color_list, self.x5, self.y5, self.spacing5,
                                                        mouse_x, mouse_y, self.hovered_card_index)

    def user_turn_method(self):
        # 마우스의 위치를 가져옴
        mouse_x, mouse_y = Mouse.getMousePos()
        # 현재 시각 불러옴
        self.current_time = pygame.time.get_ticks()

        if Mouse.getMouseState() == MouseState.CLICK:
            if self.uno_button_rect.collidepoint(mouse_x, mouse_y) and self.uno_check:
                self.sound_uno_button.set_volume(
                    self.settings_data["volume"]["sound"] * self.settings_data["volume"]["effect"])
                self.sound_uno_button.play(1)
                self.uno_flags[self.current_player] = True

        if self.uno_check:
            return

        # 플레이어턴, 컴퓨터턴 결정
        if self.current_player == 0:
            self.user_turn = True
        else:
            self.user_turn = False
        if self.user_turn:
            if self.turn_start_time is None:
                self.turn_start_time = pygame.time.get_ticks()
            if self.current_time - self.turn_start_time >= self.time_limit:
                if self.is_draw:
                    self.is_draw = False
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.turn_end_method()
                elif self.change_card:
                    self.user_turn = False
                    self.card_playing()
                else:
                    self.draw_animation(self.current_player)
                    self.player_hands[0].append(self.remain_cards.pop())
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.turn_end_method()

            if Mouse.getMouseState() == MouseState.CLICK:
                self.clicked_card_index, self.clicked_card = get_clicked_card(self.player_hands[0],
                                                                              self.user_coordinate[0], self.user_coordinate[1], self.user_spacing, mouse_x, mouse_y, self.max_per_row)
                # remain_cards 클릭 확인
                self.clicked_remain_cards = self.remain_cards_rect.collidepoint(mouse_x, mouse_y)
                # next_turn_button 클릭 확인
                self.clicked_next_turn_button = self.next_turn_button_rect.collidepoint(mouse_x, mouse_y)
                # change 클릭 확인
                self.clicked_change_index, self.clicked_change = get_clicked_change(self.change_color_list, self.x5, self.y5, self.spacing5, mouse_x, mouse_y)

            # 카드를 드로우함
            if self.clicked_remain_cards and self.new_drawn_card is None and self.pop_card is None:
                if len(self.remain_cards) > 1:
                    self.is_draw = True
                    self.draw_animation(self.current_player)
                    self.turn_start_time = pygame.time.get_ticks()
                    self.player_hands[0].append(self.remain_cards.pop())
                    self.new_drawn_card = self.player_hands[0][-1]
                elif len(self.remain_cards) == 1:
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.turn_end_method()
            # 카드를 드로우 하고 턴을 넘기는 함수.
            elif self.new_drawn_card is not None and self.clicked_next_turn_button:
                self.current_player = (self.current_player + self.game_direction) % self.player_count
                self.turn_end_method()
            # 카드를 드로우 하고, 드로우한 카드를 내는 함수.
            elif self.new_drawn_card is not None and self.pop_card is None:
                # 유효성 검사 및 클릭카드가 new_drawn_card인지 확인
                if self.new_drawn_card is not None and is_valid_move(self.new_drawn_card, self.top_card) and self.clicked_card == self.new_drawn_card and self.pop_card is None:
                    self.place_animation(self.current_player)
                    self.board_card, self.player_hands[self.current_player], self.pop_card = user_submit_card(self.clicked_card, self.clicked_card_index, self.board_card, self.player_hands[self.current_player])
                    self.turn_start_time = pygame.time.get_ticks()
            # 카드를 드로우하지 않고, 카드를 냄
            elif self.pop_card is None and self.clicked_card is not None and is_valid_move(self.clicked_card, self.top_card):
                self.place_animation(self.current_player)
                self.board_card, self.player_hands[self.current_player], self.pop_card = user_submit_card(self.clicked_card, self.clicked_card_index, self.board_card, self.player_hands[self.current_player])
                self.turn_start_time = pygame.time.get_ticks()

    def computer_turn_method(self):
        # 현재 시각 불러옴
        self.current_time = pygame.time.get_ticks()

        if self.uno_check:
            return

        # 컴퓨터 턴 처리
        if not self.user_turn:
            if self.turn_start_time is None:
                self.turn_start_time = pygame.time.get_ticks()
            if self.current_time - self.turn_start_time >= self.delay_time:  # 설정한 시간이 되면 컴퓨터가 행동함
                # 컴퓨터 로직을 입력받고, 행동을 결정함.
                if self.new_drawn_card is None and self.pop_card is None and self.playable_special_check is False:
                    self.playable, self.pop_card_index, self.playable_special_check = decide_computer_play(
                        self.player_hands[self.current_player], self.board_card,
                        self.computer_color[self.current_player], self.computer_logic[self.current_player - 1])
                # 처음 유효성 검사
                if self.new_drawn_card is None and self.pop_card is None and self.playable_special_check is False:
                    self.playable, self.pop_card_index = computer_playable_card(self.player_hands[self.current_player], self.board_card)
                # 카드를 낼 수 있을 때 낸다.
                if self.playable and self.new_drawn_card is None and self.pop_card is None:
                    self.place_animation(self.current_player)
                    self.pop_card = self.player_hands[self.current_player][self.pop_card_index]
                    self.board_card, self.player_hands[self.current_player] = com_submit_card(
                        self.pop_card, self.pop_card_index, self.board_card, self.player_hands[self.current_player])
                # 카드를 낼 수 없을 때 드로우 한다. (remain_cards가 2장 이상이면 카드를 가져오고, 한장만 존재하면 턴만 넘긴다.)
                elif not self.playable and self.new_drawn_card is None and self.pop_card is None:
                    if len(self.remain_cards) > 2:
                        self.draw_animation(self.current_player)
                        self.new_drawn_card = self.remain_cards.pop()
                        self.player_hands[self.current_player].append(self.new_drawn_card)
                        self.turn_start_time = pygame.time.get_ticks()
                    elif len(self.remain_cards) == 1:
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.turn_end_method()
                # 드로우한 카드가 낼 수 있는 경우
                elif self.new_drawn_card is not None and is_valid_move(self.new_drawn_card, self.top_card) and self.pop_card is None:
                    if self.current_time - self.turn_start_time >= self.delay_time2:
                        self.place_animation(self.current_player)
                        self.pop_card = self.new_drawn_card
                        self.pop_card_index = self.player_hands[self.current_player].index(self.pop_card)
                        self.board_card, self.player_hands[self.current_player] = com_submit_card(self.pop_card, self.pop_card_index, self.board_card, self.player_hands[self.current_player])
                # 드로우한 카드를 낼 수 없는 경우
                elif self.new_drawn_card is not None and not is_valid_move(self.new_drawn_card, self.top_card) and self.pop_card is None:
                    if self.current_time - self.turn_start_time >= self.delay_time2:
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.turn_end_method()

    def is_uno(self):
        if len(self.player_hands[self.current_player]) == 1:
            if not self.uno_check and not self.uno_flags[self.current_player]:
                self.uno_check = True
                self.uno_current_time = pygame.time.get_ticks()
                self.uno_delay_time = random.randint(500, 3000)
        else:
            self.uno_flags[self.current_player] = False
            self.uno_check = False
            self.uno_current_time = None
            self.uno_delay_time = None

    def uno_time_check(self):
        if self.uno_check:
            if self.user_turn:
                if self.current_time - self.uno_current_time >= self.uno_delay_time:
                    self.sound_uno_button.set_volume(self.settings_data["volume"]["sound"] * self.settings_data["volume"]["effect"])
                    self.sound_uno_button.play(1)
                    self.draw_animation(self.current_player)
                    self.player_hands[self.current_player].append(self.remain_cards.pop())
                else:
                    if self.uno_flags[self.current_player]:
                        self.uno_check = False

            else:
                if self.current_time - self.uno_current_time >= self.uno_delay_time:
                    self.sound_uno_button.set_volume(self.settings_data["volume"]["sound"] * self.settings_data["volume"]["effect"])
                    self.sound_uno_button.play(1)
                    self.uno_check = False
                    self.uno_flags[self.current_player] = True
                else:
                    if self.uno_flags[self.current_player]:
                        self.draw_animation(self.current_player)
                        self.player_hands[self.current_player].append(self.remain_cards.pop())

    def card_playing(self):
        if self.pop_card is not None and not self.uno_check:
            if self.user_turn:
                self.hovered_card_index -= 1
            # remain_cards가 5장 미만이면 특수카드 발동 안함
            if len(self.remain_cards) > 5 and self.pop_card.is_special() and self.pop_card.value != "change":
                self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                      self.current_player,
                                                                                      self.game_direction,
                                                                                      self.player_hands,
                                                                                      self.remain_cards,
                                                                                      self.player_count,
                                                                                      self.stage)
                self.animation_method[self.pop_card.value](self.current_player)
                self.turn_end_method()
            # 내는 카드가 special이고, change일 경우, remain_cards가 5장 미만이면 발동 안함
            elif len(self.remain_cards) > 5 and self.pop_card.is_special() and self.pop_card.value == "change":
                if self.user_turn:
                    self.change_card = True
                    if self.clicked_change_index is not None:
                        self.color_change = self.change_color_list[self.clicked_change_index]
                        self.current_player, self.game_direction = apply_special_card_effects(
                            self.pop_card, self.current_player, self.game_direction,
                            self.player_hands, self.remain_cards, self.player_count, self.stage)
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.board_card.append(self.color_change)
                        self.turn_end_method()
                else:
                    self.change_index = random.randint(0, 3)
                    self.color_change = self.change_color_list[self.change_index]
                    if self.current_time - self.turn_start_time >= self.delay_time3:
                        self.current_player, self.game_direction = apply_special_card_effects(
                            self.pop_card, self.current_player, self.game_direction, self.player_hands,
                            self.remain_cards, self.player_count, self.stage)
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.board_card.append(self.color_change)
                        self.turn_end_method()
            # 내는 카드가 special이 아닌 경우
            elif len(self.remain_cards) > 5 and not self.pop_card.is_special():
                self.current_player = (self.current_player + self.game_direction) % self.player_count
                self.turn_end_method()
            # 5장 이하인 경우에는 특수카드 발동x, 그냥 넘어감.
            elif len(self.remain_cards) <= 5:
                print('5장 미만 발동')
                self.current_player = (self.current_player + self.game_direction) % self.player_count
                self.turn_end_method()

    def win(self):
        popup = None
        if len(self.player_hands[0]) == 0:
            popup = game_view.scale_by(pygame.image.load("./resources/Image/win.png"), self.ui_size["change"])
            self.game_over = True
        elif any(len(player_hand) == 0 for player_hand in self.player_hands[1:]):
            popup = game_view.scale_by(pygame.image.load("./resources/Image/lose.png"), self.ui_size["change"])
            self.game_over = True
        if self.game_over:
            self.background_music.stop()
            self.sound_shuffle.stop()
            self.screen.fill((0, 0, 0))
            self.screen.blit(popup, (self.screen.get_width() // 2 - popup.get_size()[0] // 2,
                                     self.screen.get_height() // 2 - popup.get_size()[1] // 2))
            pygame.display.flip()
            popup_running = True
            while popup_running:
                for popup_event in pygame.event.get():
                    if popup_event.type == pygame.KEYDOWN:
                        self.running = False
                        popup_running = False
                    if popup_event.type == pygame.MOUSEBUTTONDOWN:
                        self.running = False
                        popup_running = False

    # 일시정지 버튼 관련 매서드
    def pause_popup(self):
        self.pause_popup_draw()
        self.settings_button.detect_event()
        self.close_button.detect_event()
        self.exit_button.detect_event()
        self.screen.blit(self.pause_popup_surface, self.pause_popup_rect)
        self.settings_button.draw()
        self.close_button.draw()
        self.exit_button.draw()

    def pause_popup_draw(self):
        width = self.settings_data["resolution"]["width"] * 0.4
        height = self.settings_data["resolution"]["height"] * 0.4
        x = self.settings_data["resolution"]["width"] // 2 - width // 2
        y = self.settings_data["resolution"]["height"] // 2 - height // 2
        self.pause_popup_rect = pygame.Rect(x, y, width, height)
        self.pause_popup_surface = pygame.Surface((width, height))
        self.pause_popup_surface.fill((0, 0, 0))

        self.settings_button = Button(self.settings_data["resolution"]["width"] // 2,
                                      self.settings_data["resolution"]["height"] // 2 * 0.85,
                                      width // 2.5,
                                      height // 5,
                                      self.screen,
                                      0xffffff,
                                      '설정',
                                      self.ui_size["font"][0],
                                      on_click_function=self.pause_popup_settings_button_event)
        self.exit_button = Button(self.settings_data["resolution"]["width"] // 2,
                                  self.settings_data["resolution"]["height"] // 2 * 1.15,
                                  width // 2.5,
                                  height // 5,
                                  self.screen,
                                  0xffffff,
                                  '게임 나가기',
                                  self.ui_size["font"][0],
                                  on_click_function=self.pause_popup_exit_button_event,)
        self.close_button = Button(self.settings_data["resolution"]["width"] // 2 * 1.3,
                                   self.settings_data["resolution"]["height"] // 2 * 0.7,
                                   width // 7,
                                   height // 7,
                                   self.screen,
                                   0xffffff,
                                   'X',
                                   self.ui_size["font"][0],
                                   on_click_function=self.pause_popup_close)

    def pause_popup_close(self):
        self.background_music.set_volume(self.settings_data["volume"]["sound"] * self.settings_data["volume"]["background"])
        self.background_music.play(-1)
        print('일시정지 해제')
        if self.turn_start_time is None:
            pass
        else:
            self.turn_start_time += pygame.time.get_ticks() - self.pause_start_time
        self.paused = False

    def pause_popup_exit_button_event(self):
        self.background_music.stop()
        self.sound_shuffle.stop()
        print('게임 종료 버튼 클릭')
        self.running = False

    def pause_popup_settings_button_event(self):
        self.background_music.stop()
        self.sound_shuffle.stop()
        print('설정 버튼 클릭됨')
        Settings().run()
        self.setting()

    def pause_button_process(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.pause_button_rect.collidepoint(mouse_pos):
            # 버튼 누를 때
            if self.pause_button_rect.collidepoint(mouse_pos) and Mouse.getMouseState() == MouseState.CLICK:
                Mouse.updateMouseState()
                # 클릭 판정을 위해 클릭 된 상태라면 더 이상 이벤트를 발생시키지 않음
                if not self.alreadyPressed and Mouse.getMouseState() == MouseState.DRAG:
                    self.background_music.stop()
                    self.sound_shuffle.stop()
                    self.pause_start_time = pygame.time.get_ticks()
                    self.paused = True
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

    # 일시정지 버튼 관련 메서드 끝

    # 애니메이션 관련 매서드
    def place_animation(self, index):
        self.sound_card_place.set_volume(self.settings_data["volume"]["sound"] * self.settings_data["volume"]["effect"])
        self.sound_card_place.play(1)
        if index == 0:
            pos = pygame.Vector2(self.user_coordinate[0] - self.turn_coordinate[0],
                                 self.user_coordinate[1] - self.turn_coordinate[1])
        elif index == 1:
            pos = pygame.Vector2(self.computer_coordinate[0][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[0][1] - self.turn_coordinate[3])
        elif index == 2:
            pos = pygame.Vector2(self.computer_coordinate[1][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[1][1] - self.turn_coordinate[3])
        elif index == 3:
            pos = pygame.Vector2(self.computer_coordinate[2][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[2][1] - self.turn_coordinate[3])
        elif index == 4:
            pos = pygame.Vector2(self.computer_coordinate[3][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[3][1] - self.turn_coordinate[3])
        else:
            pos = pygame.Vector2(self.computer_coordinate[4][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[4][1] - self.turn_coordinate[3])
        while True:
            self.clock.tick(game_view.FPS)
            if pos.distance_to(self.remain_pos) < 1:
                break
            pos = pos.lerp(self.remain_pos, 0.1)
            self.draw()
            self.screen.blit(self.card_back_image, pos)
            pygame.display.flip()

    def draw_animation(self, index):
        remain_pos = pygame.Vector2(self.remain_cards_x_position, self.screen.get_rect().centery - 151 * self.ui_size["change"])
        self.sound_card_place.set_volume(self.settings_data["volume"]["sound"] * self.settings_data["volume"]["effect"])
        self.sound_card_place.play(1)
        if index == 0:
            pos = pygame.Vector2(self.user_coordinate[0] - self.turn_coordinate[0],
                                 self.user_coordinate[1] - self.turn_coordinate[1])
        elif index == 1:
            pos = pygame.Vector2(self.computer_coordinate[0][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[0][1] - self.turn_coordinate[3])
        elif index == 2:
            pos = pygame.Vector2(self.computer_coordinate[1][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[1][1] - self.turn_coordinate[3])
        elif index == 3:
            pos = pygame.Vector2(self.computer_coordinate[2][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[2][1] - self.turn_coordinate[3])
        elif index == 4:
            pos = pygame.Vector2(self.computer_coordinate[3][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[3][1] - self.turn_coordinate[3])
        else:
            pos = pygame.Vector2(self.computer_coordinate[4][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[4][1] - self.turn_coordinate[3])
        while True:
            self.clock.tick(game_view.FPS)
            if remain_pos.distance_to(pos) < 1:
                break
            remain_pos = remain_pos.lerp(pos, 0.1)
            self.draw()
            self.screen.blit(self.card_back_image, remain_pos)
            pygame.display.flip()

    def draw_2_animation(self, index):
        self.draw()
        self.screen.blit(game_view.scale_by(pygame.image.load("./resources/Image/animation/+2.png"), self.ui_size["change"]),
                         (self.center_x, self.center_y))
        pygame.display.flip()
        time.sleep(0.7)
        self.draw_animation((index - self.game_direction) % self.player_count)
        self.draw_animation((index - self.game_direction) % self.player_count)

    def bomb_animation(self, index):
        self.draw()
        self.screen.blit(
            game_view.scale_by(pygame.image.load("./resources/Image/animation/bomb.png"), self.ui_size["change"]),
            (self.center_x, self.center_y))
        pygame.display.flip()
        time.sleep(0.7)
        remain_pos = [pygame.Vector2(self.remain_cards_x_position, self.screen.get_rect().centery - 100)]
        self.sound_card_place.set_volume(self.settings_data["volume"]["sound"] * self.settings_data["volume"]["effect"])
        self.sound_card_place.play(1)
        pos = [pygame.Vector2(self.user_coordinate[0] - self.turn_coordinate[0],
                              self.user_coordinate[1] - self.turn_coordinate[1])]
        j = 0
        for i in range(0, 5):
            if self.computer_attends[i]:
                pos.append(pygame.Vector2(self.computer_coordinate[j][0] - self.turn_coordinate[2],
                                          self.computer_coordinate[j][1] - self.turn_coordinate[3]))
                remain_pos.append(
                    pygame.Vector2(self.remain_cards_x_position, self.screen.get_rect().centery - 100))
                j = j + 1
        while True:
            self.clock.tick(game_view.FPS)
            if remain_pos[0].distance_to(pos[0]) < 1:
                break
            for i in range(len(remain_pos)):
                remain_pos[i] = remain_pos[i].lerp(pos[i], 0.1)
            self.draw()
            if self.game_direction > 0:
                for i in range(self.player_count - 1):
                    self.screen.blit(self.card_back_image, remain_pos[(index + i) % self.player_count])
            else:
                for i in range(self.player_count - 1):
                    self.screen.blit(self.card_back_image, remain_pos[(index - i) % self.player_count])
            pygame.display.flip()

    def reverse_animation(self, index):
        self.draw()
        self.screen.blit(
            game_view.scale_by(pygame.image.load("./resources/Image/animation/reverse.png"), self.ui_size["change"]),
            (self.center_x, self.center_y))
        pygame.display.flip()
        time.sleep(0.7)

    def skip_animation(self, index):
        if self.game_direction > 0:
            index = (index - 1) % self.player_count
        else:
            index = (index + 1) % self.player_count
        if index == 0:
            pos = pygame.Vector2(self.user_coordinate[0] - self.turn_coordinate[0],
                                 self.user_coordinate[1] - self.turn_coordinate[1])
        elif index == 1:
            pos = pygame.Vector2(self.computer_coordinate[0][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[0][1] - self.turn_coordinate[3])
        elif index == 2:
            pos = pygame.Vector2(self.computer_coordinate[1][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[1][1] - self.turn_coordinate[3])
        elif index == 3:
            pos = pygame.Vector2(self.computer_coordinate[2][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[2][1] - self.turn_coordinate[3])
        elif index == 4:
            pos = pygame.Vector2(self.computer_coordinate[3][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[3][1] - self.turn_coordinate[3])
        else:
            pos = pygame.Vector2(self.computer_coordinate[4][0] - self.turn_coordinate[2],
                                 self.computer_coordinate[4][1] - self.turn_coordinate[3])
        self.draw()
        self.screen.blit(
            game_view.scale_by(pygame.image.load("./resources/Image/animation/skip.png"), self.ui_size["change"]), pos)
        pygame.display.flip()
        time.sleep(0.7)

    def one_more_animation(self, index):
        self.draw()
        self.screen.blit(game_view.scale_by(pygame.image.load("./resources/Image/animation/_1.png"), self.ui_size["change"]),
                         (self.center_x, self.center_y))
        pygame.display.flip()
        time.sleep(0.7)

    def change_animation(self, index):
        self.draw()
        self.screen.blit(
            game_view.scale_by(pygame.image.load("./resources/Image/animation/change.png"), self.ui_size["change"]),
            (self.center_x, self.center_y))
        pygame.display.flip()
        time.sleep(0.7)

    def shield_animation(self, index):
        self.draw()
        self.screen.blit(
            game_view.scale_by(pygame.image.load("./resources/Image/animation/shield.png"), self.ui_size["change"]),
            (self.center_x, self.center_y))
        pygame.display.flip()
        time.sleep(0.7)

    # 애니메이션 관련 매서드 끝

    def draw(self):
        self.screen.fill((111, 111, 111))

        # 퍼즈버튼 그리기(그리는 이미지, 작동되는 함수)
        if self.paused:
            self.screen.blit(self.resume_button_img, (25, 25))
        else:
            self.screen.blit(self.pause_button_img, (25, 25))

        # game_direction 그리기
        if self.game_direction == 1:
            self.screen.blit(self.direction_img, (self.center_x, self.center_y))
        elif self.game_direction == -1:
            self.screen.blit(self.direction_reverse_img, (self.center_x, self.center_y))

        # 누구 턴인지 표시하는 화살표 그리기
        if self.user_turn:
            self.screen.blit(self.turn_arrow_img, (self.user_coordinate[0]-self.turn_coordinate[0], self.user_coordinate[1]-self.turn_coordinate[1]))
        elif self.current_player == 1:
            self.screen.blit(self.turn_arrow_img, (self.computer_coordinate[0][0]-self.turn_coordinate[2], self.computer_coordinate[0][1]-self.turn_coordinate[3]))
        elif self.current_player == 2:
            self.screen.blit(self.turn_arrow_img, (self.computer_coordinate[1][0]-self.turn_coordinate[2], self.computer_coordinate[1][1]-self.turn_coordinate[3]))
        elif self.current_player == 3:
            self.screen.blit(self.turn_arrow_img, (self.computer_coordinate[2][0]-self.turn_coordinate[2], self.computer_coordinate[2][1]-self.turn_coordinate[3]))
        elif self.current_player == 4:
            self.screen.blit(self.turn_arrow_img, (self.computer_coordinate[3][0]-self.turn_coordinate[2], self.computer_coordinate[3][1]-self.turn_coordinate[3]))
        elif self.current_player == 5:
            self.screen.blit(self.turn_arrow_img, (self.computer_coordinate[4][0]-self.turn_coordinate[2], self.computer_coordinate[4][1]-self.turn_coordinate[3]))

        # 남은 카드 더미 그리기
        self.screen.blit(self.remain_cards[0].card_img_back, (self.remain_cards_x_position, self.screen.get_rect().centery - 151 * self.ui_size["change"]))
        # 엎은 카드 그리기
        draw_board_card(self.screen, self.board_card[-1], self.screen.get_rect().centerx, self.screen.get_rect().centery - 151 * self.ui_size["change"])
        # 유저 카드 그리기
        draw_cards_user(self.screen, self.player_hands[0], self.user_coordinate[0], self.user_coordinate[1], self.max_per_row,
                        self.user_spacing, self.hovered_card_index)
        # 현재 색 그리기
        card_folder = "./resources/Image/select_color_cw" if self.settings_data["color_weakness"] else "./resources/Image/select_color"
        card_color = game_view.scale_by(pygame.image.load(f"{card_folder}/{self.top_card.color}.png"), self.ui_size["change"])
        self.screen.blit(card_color, (self.remain_cards_x_position, self.screen.get_rect().centery - 350 * self.ui_size["change"]))
        # ai의 카드를 그린다.
        for i in range(len(self.player_hands) - 1):
            draw_cards_ai(self.screen, self.player_hands[i + 1], self.computer_coordinate[i][0],
                          self.computer_coordinate[i][1],
                          self.max_per_row_com, 20,
                          None,
                          show_back=False)  # 추후 True로 바꾼다.

        # 유저턴이고, 체인지 카드면 체인지카드를 그린다.
        if self.user_turn and self.change_card:
            draw_change_card(self.screen, self.change_color_list, self.x5, self.y5, self.spacing5, self.hovered_change_index)  # 체인지 카드 그림

        # 우노 버튼 표시
        if self.uno_check and not self.uno_flags[self.current_player]:
            self.screen.blit(self.uno_button_img, self.uno_button_rect)
        else:
            self.screen.blit(self.uno_button_inactive_img, self.uno_button_inactive_rect)

        # 유저가 카드를 뽑았을 경우, next_turn 버튼 표시
        if self.user_turn and self.new_drawn_card is not None:
            if is_valid_move(self.new_drawn_card, self.top_card):
                self.play_drawn_card_button.topleft = (self.screen.get_rect().centerx + 100, self.screen.get_rect().centery)
                draw_button(self.screen, "Click NEXT TURN button to turn.\n Or If you want to submit a drawn card,"
                                "\nclick on the drawn card.", self.small_font, (255, 255, 255), self.play_drawn_card_button)
            elif not is_valid_move(self.new_drawn_card, self.top_card):
                self.play_drawn_card_button.topleft = (self.screen.get_rect().centerx + 100, self.screen.get_rect().centery)
                draw_button(self.screen, "Click NEXT TURN button to turn.", self.small_font, (255, 255, 255),
                            self.play_drawn_card_button)
            # 턴 넘기기는 버튼
            self.screen.blit(self.next_turn_button_img, self.next_turn_button_rect)

        # 유저턴일때 표시될 사항. (시간제한, 턴 넘기기 버튼)
        if self.user_turn and not self.uno_check and self.turn_start_time is not None:
            self.remaining_time = self.time_limit - (self.current_time - self.turn_start_time)
            self.remaining_time_text = f"턴 남은 시간: {self.remaining_time // 1000}초"
            draw_text(self.screen, self.remaining_time_text, self.font, (255, 255, 255), self.screen.get_rect().centerx/2, 30)

        # 유저 이름 그리기
        self.screen.blit(self.text_player_name,
                         (self.user_coordinate[0] - self.turn_coordinate[0] + self.ui_size["font"][0] * 3,
                          self.user_coordinate[1] - self.turn_coordinate[1] + self.ui_size["font"][0]))
        j = 0
        for i in range(5):
            if self.computer_attends[i]:
                self.screen.blit(self.text_computer_name[i],
                                 (self.computer_coordinate[j][0] - self.turn_coordinate[2] - self.ui_size["font"][0] // 2,
                                  self.computer_coordinate[j][1] - self.turn_coordinate[3] + self.ui_size["font"][0] * 2))
                j = j + 1
        # 키보드로 선택된 경우 체크 표시
        # 드로우
        if self.key_select_option == 0:
            self.screen.blit(self.selected_image, (self.screen.get_rect().centerx - 100, self.screen.get_rect().centery))
        # 우노 버튼
        elif self.key_select_option == 1:
            self.screen.blit(self.selected_image, self.uno_button_rect)
        # 다음 턴 버튼
        elif self.key_select_option == 2:
            self.screen.blit(self.selected_image, self.next_turn_button_rect)

        # 일시정지 팝업 띄우기
        if self.paused:
            self.pause_popup()

        # 매 프레임마다 화면 업데이트
        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.background_music.stop()
                self.sound_shuffle.stop()
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not self.paused:
                        self.pause_start_time = pygame.time.get_ticks()
                        self.paused = True
                        print('일시정지 시작')
                        self.background_music.stop()
                        self.sound_shuffle.stop()
                    else:
                        self.pause_popup_close()
                if event.type == pygame.KEYDOWN:
                    if event.key == self.settings_data["key"]['left']:
                        if self.key_select_option == 3:
                            self.hovered_card_index = (self.hovered_card_index - 1) % len(self.player_hands[0])
                    elif event.key == self.settings_data["key"]['right']:
                        if self.key_select_option == 3:
                            self.hovered_card_index = (self.hovered_card_index + 1) % len(self.player_hands[0])
                    elif event.key == self.settings_data["key"]['up']:
                        if self.key_select_option == 0:
                            self.key_select_option = 3
                        elif self.key_select_option == 1:
                            self.key_select_option = 0
                        elif self.key_select_option == 2:
                            if any(self.uno_flags):
                                self.key_select_option = 1
                            else:
                                self.key_select_option = 0
                        else:
                            if self.user_turn and self.new_drawn_card is not None:
                                self.key_select_option = 2
                            elif any(self.uno_flags):
                                self.key_select_option = 1
                            else:
                                self.key_select_option = 0
                    elif event.key == self.settings_data["key"]['down']:
                        if self.key_select_option == 0:
                            if any(self.uno_flags):
                                self.key_select_option = 1
                            elif self.user_turn and self.new_drawn_card is not None:
                                self.key_select_option = 2
                            else:
                                self.key_select_option = 3
                        elif self.key_select_option == 1:
                            if self.user_turn and self.new_drawn_card is not None:
                                self.key_select_option = 2
                            else:
                                self.key_select_option = 3
                        elif self.key_select_option == 2:
                            self.key_select_option = 3
                        else:
                            self.key_select_option = 0
                    elif event.key == self.settings_data["key"]['enter']:
                        if self.key_select_option == 0:
                            pass
                        elif self.key_select_option == 1:
                            pass
                        elif self.key_select_option == 2:
                            pass
                        else:
                            self.clicked_card_index, self.clicked_card \
                                = self.hovered_card_index, self.player_hands[0][self.hovered_card_index]

    def run(self):
        self.setting()
        self.background_music.set_volume(self.settings_data["volume"]["sound"] * self.settings_data["volume"]["background"])
        self.background_music.play(-1)
        self.sound_shuffle.set_volume(self.settings_data["volume"]["sound"] * self.settings_data["volume"]["background"])
        self.sound_shuffle.play(1)
        while self.running:
            self.win()
            Mouse.updateMouseState()
            self.clock.tick(game_view.FPS)
            if not self.paused:
                self.game()
                self.is_uno()
                self.uno_time_check()
                self.card_playing()
            self.draw()
            self.event()
            self.pause_button_process()
