import pygame
import pickle
import random
import math
from mouse import Mouse, MouseState
from slider import Slider
from button import Button
from option import save_option as save
from card_gen import generate_cards, generate_for_change_cards
from card_shuffle import shuffle_cards, distribute_cards
from option import basic_option as basic
from game_utils import (
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
    check_uno,
    computer_playable_card,
    is_uno,
    user_submit_card,
    com_submit_card,
    apply_special_card_effects,
    card_reshuffle
)


class SingleGame():
    def __init__(self, computer_attends):
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
        self.font = pygame.font.Font("./resources/maplestory_font.ttf", self.font_size[0])
        self.small_font = pygame.font.Font("./resources/maplestory_font.ttf", self.font_size[1])

        self.screen = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption(basic.game_title)
        self.clock = pygame.time.Clock()
        self.running = True

        # single_game 변수
        self.player_count = 1  # 플레이어 수
        self.card_count = 7  # 처음 시작하는 카드 수
        self.winner_message = ""  # 승리 메세지

        # 로비에서 가져온 정보
        self.computer_attends = computer_attends
        for i in range(len(self.computer_attends)):
            if self.computer_attends[i]:
                self.player_count += 1

        self.computer_color = ["red", "blue", "green", "yellow"]

        # 컴퓨터 초기 좌표와 카드 색 선호도.
        self.user_coordinate = []
        self.computer_coordinate = []
        if self.display_size[0] == 1920:
            self.max_per_row = 15
            self.max_per_row_com = 20
            self.user_coordinate.append(30)
            self.user_coordinate.append(self.display_size[1] * 0.7)
            self.user_spacing = self.display_size[1] * 0.08
            if self.computer_attends[0]:
                self.computer_coordinate.append([self.display_size[0] * 0.65, self.display_size[1] * 0.03])
                self.computer1_color = self.computer_color[random.randint(0, 3)]
                print("computer1_color", self.computer1_color)
            if self.computer_attends[1]:
                self.computer_coordinate.append([self.display_size[0] * 0.65, (self.display_size[1] * 0.03) + self.display_size[1] * 0.2])
                self.computer2_color = self.computer_color[random.randint(0, 3)]
                print("computer2_color", self.computer2_color)
            if self.computer_attends[2]:
                self.computer_coordinate.append([self.display_size[0] * 0.65, (self.display_size[1] * 0.03) + (self.display_size[1] * 0.4)])
                self.computer3_color = self.computer_color[random.randint(0, 3)]
                print("computer3_color", self.computer3_color)
            if self.computer_attends[3]:
                self.computer_coordinate.append([self.display_size[0] * 0.65, (self.display_size[1] * 0.03) + (self.display_size[1] * 0.6)])
                self.computer4_color = self.computer_color[random.randint(0, 3)]
                print("computer4_color", self.computer4_color)
            if self.computer_attends[4]:
                self.computer_coordinate.append([self.display_size[0] * 0.65, (self.display_size[1] * 0.03) + (self.display_size[1] * 0.8)])
                self.computer5_color = self.computer_color[random.randint(0, 3)]
                print("computer5_color", self.computer5_color)
        if self.display_size[1] == 1600:
            self.max_per_row = 13
            self.max_per_row_com = 17
            self.user_coordinate.append(30)
            self.user_coordinate.append(self.display_size[1] * 0.7)
            self.user_spacing = self.display_size[1] * 0.08
            if self.computer_attends[0]:
                self.computer_coordinate.append([self.display_size[0] * 0.72, self.display_size[1] * 0.08])
                self.computer1_color = self.computer_color[random.randint(0, 3)]
                print("computer1_color", self.computer1_color)
            if self.computer_attends[1]:
                self.computer_coordinate.append([self.display_size[0] * 0.72, (self.display_size[1] * 0.08) + self.display_size[1] * 0.2])
                self.computer2_color = self.computer_color[random.randint(0, 3)]
                print("computer2_color", self.computer2_color)
            if self.computer_attends[2]:
                self.computer_coordinate.append([self.display_size[0] * 0.72, (self.display_size[1] * 0.08) + (self.display_size[1] * 0.4)])
                self.computer3_color = self.computer_color[random.randint(0, 3)]
                print("computer3_color", self.computer3_color)
            if self.computer_attends[3]:
                self.computer_coordinate.append([self.display_size[0] * 0.72, (self.display_size[1] * 0.08) + (self.display_size[1] * 0.6)])
                self.computer4_color = self.computer_color[random.randint(0, 3)]
                print("computer4_color", self.computer4_color)
            if self.computer_attends[4]:
                self.computer_coordinate.append([self.display_size[0] * 0.72, (self.display_size[1] * 0.08) + (self.display_size[1] * 0.8)])
                self.computer5_color = self.computer_color[random.randint(0, 3)]
                print("computer5_color", self.computer5_color)
        else :
            self.max_per_row = 11
            self.max_per_row_com = 15
            self.user_coordinate.append(30)
            self.user_coordinate.append(self.display_size[1] * 0.7)
            self.user_spacing = self.display_size[1] * 0.08
            if self.computer_attends[0]:
                self.computer_coordinate.append([self.display_size[0] * 0.67, self.display_size[1] * 0.01])
                self.computer1_color = self.computer_color[random.randint(0, 3)]
                print("computer1_color", self.computer1_color)
            if self.computer_attends[1]:
                self.computer_coordinate.append([self.display_size[0] * 0.67, (self.display_size[1] * 0.01) + self.display_size[1] * 0.2])
                self.computer2_color = self.computer_color[random.randint(0, 3)]
                print("computer2_color", self.computer2_color)
            if self.computer_attends[2]:
                self.computer_coordinate.append([self.display_size[0] * 0.67, (self.display_size[1] * 0.01) + (self.display_size[1] * 0.4)])
                self.computer3_color = self.computer_color[random.randint(0, 3)]
                print("computer3_color", self.computer3_color)
            if self.computer_attends[3]:
                self.computer_coordinate.append([self.display_size[0] * 0.67, (self.display_size[1] * 0.01) + (self.display_size[1] * 0.6)])
                self.computer4_color = self.computer_color[random.randint(0, 3)]
                print("computer4_color", self.computer4_color)
            if self.computer_attends[4]:
                self.computer_coordinate.append([self.display_size[0] * 0.67, (self.display_size[1] * 0.01) + (self.display_size[1] * 0.8)])
                self.computer5_color = self.computer_color[random.randint(0, 3)]
                print("computer5_color", self.computer5_color)


        # 게임 이미지를 로드
        self.pause_button_img = pygame.image.load("./resources/Image/button_images/pause.png").convert_alpha()
        self.resume_button_img = pygame.image.load("./resources/Image/button_images/resume.png").convert_alpha()
        self.direction_img = pygame.image.load("./resources/Image/direction_images/direction.png").convert_alpha()
        self.direction_reverse_img = pygame.image.load(
            "./resources/Image/direction_images/direction_reverse.png").convert_alpha()
        self.turn_arrow_img = pygame.image.load("./resources/Image/direction_images/turn_arrow.png").convert_alpha()
        self.next_turn_button_img = pygame.image.load("./resources/Image/button_images/next_turn.png").convert_alpha()
        self.uno_button_img = pygame.image.load("./resources/Image/button_images/uno_button.png").convert_alpha()
        self.uno_button_inactive_img = pygame.image.load(
            "./resources/Image/button_images/uno_button_inactive.png").convert_alpha()

        # 화면 중앙 좌표 계산
        self.image_width, self.image_height = self.direction_img.get_size()
        self.center_x = (self.display_size[0] - self.image_width) // 2
        self.center_y = (self.display_size[1] - self.image_height) // 2

        # 카드 생성 및 셔플
        self.cards = generate_cards(self.color_weakness)
        self.shuffled_cards = shuffle_cards(self.cards)

        # 카드 분배, 유저는 player_hands[0]이고, 나머지는 인공지능으로 설정한다. change는 카드 체인지를 위한 카드들.
        self.player_hands, self.remain_cards = distribute_cards(self.shuffled_cards, self.player_count, self.card_count)
        self.change_color_list = generate_for_change_cards(self.color_weakness)

        # 플레이어 순서 결정
        self.player_order = list(range(self.player_count))
        # 초기 플레이어 순서를 위한 설정 값.
        self.current_player = (random.randint(0, self.player_count - 1))
        # 게임 순서 방향 (1: 정방향, -1: 역방향)
        self.game_direction = 1

        # 보드에 뒤집힌 카드 설정 (카드 한 장을 뽑아서 남은 카드 덱 옆에 보이게 놓기)
        self.board_card = [self.remain_cards.pop()]

        # 선택한 카드 위로 띄우기 해야함
        # 카드 약간 띄우는 초기값 index는 플레이어, index2는 ai,
        self.hovered_card_index = None
        self.hovered_card_index2 = None
        self.hovered_change_index = None

        self.paused = False  # 일시정지 초기값
        self.game_over = False  # 게임 오버 초기값
        self.user_turn = None  # 유저 턴 여부 초기값

        self.top_card = None  # board카드 맨 위
        self.pop_card = None  # 뽑은 카드 초기값
        self.pop_card_index = None  # 뽑은 카드 인덱스 숫자 초기값
        self.draw_requested = False  # draw 했는지 확인하는 초기값
        self.new_drawn_card = None  # draw한 카드가 어떤 카드인가의 초기값

        self.clicked_card = None  # 클릭 카드 초기값
        self.clicked_remain_cards = False  # remain_cards 클릭 여부 초기값
        self.clicked_next_turn_button = False  # 다음턴 클릭여부 초기값

        # uno 초기값
        self.uno_check = False
        self.uno_current_time = None
        self.uno_delay_time = None
        self.uno_click_time = None
        self.user_uno_clicked = False
        self.one_flags = [False, False, False, False, False, False]
        self.change_card = False
        self.clicked_card_index = None
        self.clicked_change_index = None
        self.change_index = None
        self.playable = False
        self.clicked_change = False
        self.user_draw_time = None
        self.uno_drawn_card = None
        self.color_change = None
        self.change_uno_expire = False

        # 턴 시간
        self.time_limit = 10000  # 유저의 턴 시간 제한
        self.current_time = pygame.time.get_ticks()  # 현재 시간
        self.turn_start_time = pygame.time.get_ticks()  # 턴 시작 시간
        self.delay_time = random.randint(1000, 2000)  # 컴퓨터 딜레이 타임1
        self.delay_time2 = self.delay_time + random.randint(900, 2000)  # 컴퓨터 딜레이 타임2
        self.delay_time3 = self.delay_time2 + random.randint(900, 2000)  # 컴퓨터 딜레이 타임3
        self.computer_action_time = pygame.time.get_ticks() + self.delay_time  # 현재 시간에 랜덤한 지연 시간을 더함
        self.remaining_time = None  # 유저 턴 시간제한
        self.remaining_time_text = None  # 유저 턴 시간제한 텍스트
        self.after_draw_remaining_time = None  # 드로우 후 유저 턴 시간제한
        self.after_draw_remaining_time_text = None  # 드로우 후 유저 턴 시간제한 텍스트
        self.uno_remaining_time = None  # 유저턴 남은 우노 시간
        self.uno_remaining_time_text = None  # 유저턴 남은 우노 시간 텍스트
        self.com_uno_remaining_time = None  # 컴퓨터턴 남은 우노 시간
        self.com_uno_remaining_time_text = None  # 컴퓨터턴 남은 우노 시간 텍스트

        # change카드 좌표, spacing은 공백
        self.x5 = 100
        self.y5 = 100
        self.spacing5 = 200
        # 플레이어들이 카드를 뽑고 남은 카드들의 위치를 잡는데 사용
        self.remain_cards_x_position = (self.screen.get_rect().centerx - 100)
        self.remain_cards_y_position = (self.screen.get_rect().centery - 50)
        # remain카드
        self.remain_cards_rect = self.remain_cards[0].card_img_back.get_rect()
        self.remain_cards_rect.topleft = (self.remain_cards_x_position, self.remain_cards_y_position)
        # pause버튼
        self.pause_button_rect = self.pause_button_img.get_rect()
        self.pause_button_rect.topleft = (25, 25)
        # next_turn버튼
        self.next_turn_button_rect = self.next_turn_button_img.get_rect()
        self.next_turn_button_rect.topleft = (self.user_coordinate[0], self.user_coordinate[1] - 150)
        # uno_button
        self.uno_button_rect = self.uno_button_img.get_rect()
        self.uno_button_rect.topleft = (self.user_coordinate[0], self.user_coordinate[1] - 300)
        self.uno_button_inactive_rect = self.uno_button_inactive_img.get_rect()
        self.uno_button_inactive_rect.topleft = (150, self.display_size[1] * 0.5)
        self.play_drawn_card_button = pygame.Rect(0, 0, 430, 110)

    def reset(self):
        self.pop_card = None  # 뽑은 카드 초기값
        self.pop_card_index = None  # 뽑은 카드 인덱스 숫자 초기값
        self.draw_requested = False  # draw 했는지 확인하는 초기값
        self.new_drawn_card = None  # draw한 카드가 어떤 카드인가의 초기값

        self.clicked_card = None  # 클릭 카드 초기값
        self.clicked_remain_cards = False  # remain_cards 클릭 여부 초기값
        self.clicked_next_turn_button = False  # 다음턴 클릭여부 초기값

        # uno 초기값
        self.uno_check = False
        self.uno_current_time = None
        self.uno_delay_time = None
        self.uno_click_time = None
        self.user_uno_clicked = False
        self.one_flags = [False, False, False, False, False, False]
        self.change_card = False
        self.clicked_card_index = None
        self.clicked_change_index = None
        self.change_index = None
        self.playable = False
        self.clicked_change = False
        self.user_draw_time = None
        self.uno_drawn_card = None
        self.color_change = None
        self.change_uno_expire = False

        # 턴 시간
        self.time_limit = 10000  # 유저의 턴 시간 제한
        self.current_time = pygame.time.get_ticks()  # 현재 시간
        self.turn_start_time = pygame.time.get_ticks()  # 턴 시작 시간
        self.delay_time = random.randint(1000, 2000)  # 컴퓨터 딜레이 타임1
        self.delay_time2 = self.delay_time + random.randint(900, 2000)  # 컴퓨터 딜레이 타임2
        self.delay_time3 = self.delay_time2 + random.randint(900, 2000)  # 컴퓨터 딜레이 타임3
        self.computer_action_time = pygame.time.get_ticks() + self.delay_time  # 현재 시간에 랜덤한 지연 시간을 더함
        self.remaining_time = None  # 유저 턴 시간제한
        self.remaining_time_text = None  # 유저 턴 시간제한 텍스트
        self.after_draw_remaining_time = None  # 드로우 후 유저 턴 시간제한
        self.after_draw_remaining_time_text = None  # 드로우 후 유저 턴 시간제한 텍스트
        self.uno_remaining_time = None  # 유저턴 남은 우노 시간
        self.uno_remaining_time_text = None  # 유저턴 남은 우노 시간 텍스트
        self.com_uno_remaining_time = None  # 컴퓨터턴 남은 우노 시간
        self.com_uno_remaining_time_text = None  # 컴퓨터턴 남은 우노 시간 텍스트

    def game(self):
        # 마우스의 위치를 가져옴
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # 현재 플레이어 결정
        self.top_card = get_top_card(self.board_card)
        # 현재 시각 불러옴
        self.current_time = pygame.time.get_ticks()

        # 플레이어턴, 컴퓨터턴 결정
        if self.current_player == 0:
            self.user_turn = True
        else:
            self.user_turn = False

        if Mouse.getMouseState() == MouseState.CLICK:
            if self.uno_button_rect.collidepoint(mouse_x, mouse_y) and len(self.player_hands[self.current_player]) == 1:
                self.user_uno_clicked = True
        self.hovered_card_index = find_hovered_card(self.player_hands[0], self.user_coordinate[0],
                                                    self.user_coordinate[1], self.user_spacing, mouse_x, mouse_y, self.max_per_row)
        self.hovered_change_index = find_hovered_change(self.change_color_list, self.x5, self.y5, self.spacing5, mouse_x, mouse_y)

        # 현재 플레이어가 유저인지 확인
        if self.user_turn:
            if self.turn_start_time is None:
                self.turn_start_time = pygame.time.get_ticks()
            if Mouse.getMouseState() == MouseState.CLICK:
                self.clicked_card_index, self.clicked_card = get_clicked_card(self.player_hands[0],
                                                                              self.user_coordinate[0], self.user_coordinate[1], self.user_spacing, mouse_x, mouse_y, self.max_per_row)
                # remain_cards 클릭 확인
                self.clicked_remain_cards = self.remain_cards_rect.collidepoint(mouse_x, mouse_y)
                # next_turn_button 클릭 확인
                self.clicked_next_turn_button = self.next_turn_button_rect.collidepoint(mouse_x, mouse_y)
                # change 클릭 확인
                self.clicked_change_index, self.clicked_change = get_clicked_change(self.change_color_list, self.x5, self.y5, self.spacing5, mouse_x,
                                                                          mouse_y)
            if self.clicked_card is not None or self.clicked_remain_cards or self.clicked_next_turn_button or self.user_uno_clicked:
                # 카드를 드로우함
                if self.clicked_remain_cards and self.new_drawn_card is None and self.pop_card is None:
                    self.user_draw_time = pygame.time.get_ticks()
                    self.player_hands[0].append(self.remain_cards.pop())
                    self.new_drawn_card = self.player_hands[0][-1]
                # 카드를 드로우 하고 턴을 넘기는 함수.
                elif self.new_drawn_card is not None and self.clicked_next_turn_button:
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.new_drawn_card = None
                    self.clicked_card = None
                    self.clicked_remain_cards = False
                    self.clicked_next_turn_button = False
                # 카드를 드로우 하고, 드로우한 카드를 내는 함수.
                elif self.new_drawn_card is not None and self.pop_card is None:
                    # 유효성 검사 및 클릭카드가 new_drawn_card인지 확인
                    if self.new_drawn_card is not None and is_valid_move(self.new_drawn_card, self.top_card) and self.clicked_card == self.new_drawn_card and self.pop_card is None:
                        self.board_card, self.player_hands[self.current_player], self.pop_card = user_submit_card\
                            (self.clicked_card, self.clicked_card_index, self.board_card, self.player_hands[self.current_player])
                        self.uno_check = check_uno(self.player_hands[0])
                        if self.uno_check:
                            self.one_flags, self.uno_current_time, self.uno_delay_time = is_uno(self.one_flags,
                                                                                                self.current_player)
                # 카드를 드로우하지 않고, 카드를 냄
                elif self.new_drawn_card is None and self.pop_card is None:
                    # 유효성 검사
                    if self.clicked_card is not None and is_valid_move(self.clicked_card, self.top_card):
                        self.board_card, self.player_hands[self.current_player], self.pop_card = user_submit_card\
                            (self.clicked_card, self.clicked_card_index, self.board_card, self.player_hands[self.current_player])
                        self.uno_check = check_uno(self.player_hands[0])
                        if self.uno_check:
                            self.one_flags, self.uno_current_time, self.uno_delay_time = is_uno(self.one_flags,
                                                                                                self.current_player)
            # 카드를 냈을 때,
            if self.pop_card is not None:
                # 우노일 경우
                if self.uno_check:
                    if self.user_uno_clicked:
                        self.one_flags[0] = False
                        # 내는 카드가 special이고 change가 아닐 경우
                        if self.pop_card.is_special() and self.pop_card.value != "change":
                            self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                         self.current_player,
                                                                                         self.game_direction,
                                                                                         self.player_hands,
                                                                                         self.remain_cards,
                                                                                         self.player_count)
                            self.reset()
                        # 내는 카드가 special이고, change일 경우
                        elif self.pop_card.is_special() and self.pop_card.value == "change":
                            self.change_card = True
                            if self.clicked_change_index is not None:
                                self.color_change = self.change_color_list[self.clicked_change_index]
                                self.current_player, self.game_direction = apply_special_card_effects(
                                    self.pop_card, self.current_player, self.game_direction,
                                    self.player_hands, self.remain_cards, self.player_count)
                                self.board_card.append(self.color_change)
                                self.reset()
                        # 내는 카드가 special이 아닌 경우
                        elif not self.pop_card.is_special():
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.reset()
                elif not self.uno_check:
                    # 내는 카드가 special이고 change가 아닐 때,
                    if self.pop_card.is_special() and self.pop_card.value != "change":
                        self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                     self.current_player,
                                                                                     self.game_direction,
                                                                                     self.player_hands,
                                                                                     self.remain_cards,
                                                                                     self.player_count)
                        self.reset()
                    # 내는 카드가 change인 경우
                    elif self.pop_card.value == "change":
                        self.change_card = True
                        if self.clicked_change_index is not None:
                            self.color_change = self.change_color_list[self.clicked_change_index]
                            self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                         self.current_player,
                                                                                         self.game_direction,
                                                                                         self.player_hands,
                                                                                         self.remain_cards,
                                                                                         self.player_count)
                            self.board_card.append(self.color_change)
                            self.reset()
                    # 내는 카드가 special이 아닌 경우
                    else:
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()

            # 우노 시간 넘기면 발동
            if self.pop_card is not None and self.one_flags[0]:
                if self.current_time - self.uno_current_time >= self.uno_delay_time:
                    self.uno_drawn_card = self.remain_cards.pop()
                    self.player_hands[0].append(self.uno_drawn_card)
                    # 내는 카드가 special이고, change일 경우
                    if self.pop_card.is_special() and self.pop_card.value == "change":
                        self.one_flags[0] = False
                        self.uno_check = False
                        self.user_uno_clicked = False
                        self.change_uno_expire = True
                    # 내는 카드가 special이고, change가 아닐 경우
                    elif self.pop_card.is_special() and self.pop_card.value != "change":
                        self.current_player, self.game_direction = apply_special_card_effects(
                            self.pop_card, self.current_player, self.game_direction, self.player_hands,
                            self.remain_cards,
                            self.player_count)
                        self.reset()

                    # 내는 카드가 special이 아닌 경우
                    elif not self.pop_card.is_special():
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
            # 우노 마치고, change_card 제한시간 넘는 경우
            elif self.change_uno_expire:
                if self.user_turn and self.current_time - self.turn_start_time >= self.time_limit:
                    self.current_player, self.game_direction = apply_special_card_effects(
                        self.pop_card, self.current_player, self.game_direction, self.player_hands,
                        self.remain_cards,
                        self.player_count)
                    self.reset()
            # 유저의 턴일 때 시간이 초과되면 드로우하고 턴을 넘김
            elif self.new_drawn_card is None:
                if self.user_turn and self.current_time - self.turn_start_time >= self.time_limit:
                    self.new_drawn_card = self.remain_cards.pop()
                    self.player_hands[self.current_player].append(self.new_drawn_card)  # 카드를 드로우
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.reset()

            # 유저가 드로우를 하고 시간이 초과되면 턴을 그냥 넘김
            elif self.new_drawn_card is not None:
                if self.user_turn and self.current_time - self.user_draw_time >= self.time_limit:
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.reset()

        # 컴퓨터 턴 처리
        if not self.user_turn:
            if self.current_time >= self.computer_action_time:  # 설정한 시간이 되면 컴퓨터가 행동함
                # 처음 유효성 검사
                if self.new_drawn_card is None and self.pop_card is None:
                    self.playable, self.pop_card_index = computer_playable_card(self.player_hands[self.current_player], self.board_card)
                # 카드를 낼 수 있을 때 낸다.
                if self.playable and self.new_drawn_card is None and self.pop_card is None:
                    self.pop_card = self.player_hands[self.current_player][self.pop_card_index]
                    self.board_card, self.player_hands[self.current_player] = com_submit_card\
                        (self.pop_card, self.pop_card_index, self.board_card, self.player_hands[self.current_player])
                    self.uno_check = check_uno(self.player_hands[self.current_player])
                    if self.uno_check:
                        self.one_flags, self.uno_current_time, self.uno_delay_time = is_uno(self.one_flags, self.current_player)
                # 카드를 낼 수 없을 때 드로우 한다.
                elif not self.playable and self.new_drawn_card is None and self.pop_card is None:
                    self.new_drawn_card = self.remain_cards.pop()
                    self.player_hands[self.current_player].append(self.new_drawn_card)
                # 드로우한 카드가 낼 수 있는 경우
                elif self.new_drawn_card is not None and is_valid_move(self.new_drawn_card, self.top_card) and self.pop_card is None:
                    if self.current_time - self.turn_start_time >= self.delay_time2:
                        self.pop_card = self.new_drawn_card
                        self.pop_card_index = self.player_hands[self.current_player].index(self.pop_card)
                        self.board_card, self.player_hands[self.current_player] = com_submit_card \
                            (self.pop_card, self.pop_card_index, self.board_card, self.player_hands[self.current_player])
                        self.uno_check = check_uno(self.player_hands[self.current_player])
                        if self.uno_check:
                            self.one_flags, self.uno_current_time, self.uno_delay_time = is_uno(self.one_flags,
                                                                                                self.current_player)
                # 드로우한 카드를 낼 수 없는 경우
                elif self.new_drawn_card is not None and not is_valid_move(self.new_drawn_card, self.top_card) and self.pop_card is None:
                    if self.current_time - self.turn_start_time >= self.delay_time2:
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.new_drawn_card = None
                        self.computer_action_time = pygame.time.get_ticks() + self.delay_time
                        self.turn_start_time = pygame.time.get_ticks()
                # 컴퓨터가 우노이고, 유저가 우노를 클릭했을 경우
                elif self.uno_check:
                    if self.user_uno_clicked:
                        self.one_flags[self.current_player] = False
                        self.uno_drawn_card = self.remain_cards.pop()
                        self.player_hands[self.current_player].append(self.uno_drawn_card)
                        # 컴퓨터가 낸 카드가 special일 경우
                        if self.pop_card.is_special() and self.pop_card.value != "change":
                            self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                                  self.current_player,
                                                                                                  self.game_direction,
                                                                                                  self.player_hands,
                                                                                                  self.remain_cards,
                                                                                                  self.player_count)
                            self.reset()
                        # 컴퓨터가 낸 카드가 change일 경우
                        elif self.pop_card.value == "change":
                            self.change_index = random.randint(0, 3)
                            self.color_change = self.change_color_list[self.change_index]
                            self.board_card.append(self.color_change)
                            self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                                  self.current_player,
                                                                                                  self.game_direction,
                                                                                                  self.player_hands,
                                                                                                  self.remain_cards,
                                                                                                  self.player_count)
                            self.reset()
                        # 컴퓨터가 낸 카드가 special이 아닌 경우
                        elif not self.pop_card.is_special():
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.reset()
                # 컴퓨터가 우노가 아니고, 컴퓨터가 카드를 낸 경우
                elif not self.uno_check and self.pop_card is not None:
                    # 내는 카드가 special이고 change가 아닐 경우
                    if self.pop_card.is_special() and self.pop_card.value != "change":
                        self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                     self.current_player,
                                                                                     self.game_direction,
                                                                                     self.player_hands,
                                                                                     self.remain_cards,
                                                                                     self.player_count)
                        self.reset()
                    # 내는 카드가 special이고, change일 경우
                    elif self.pop_card.is_special() and self.pop_card.value == "change":
                        if self.current_time - self.turn_start_time >= self.delay_time3:
                            self.change_index = random.randint(0, 3)
                            self.color_change = self.change_color_list[self.change_index]
                            self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                         self.current_player,
                                                                                         self.game_direction,
                                                                                         self.player_hands,
                                                                                         self.remain_cards,
                                                                                         self.player_count)
                            self.board_card.append(self.color_change)
                            self.reset()
                    # 내는 카드가 special이 아닌 경우
                    elif not self.pop_card.is_special():
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()

            # 컴퓨터의 턴일 때 시간이 초과되면 우노를 넘긴다.
            if any(self.one_flags[1:]) and not self.user_turn:
                if self.current_time - self.uno_current_time >= self.uno_delay_time:
                    # 내는 카드가 special이고, change가 아닐 경우
                    if self.pop_card.is_special() and self.pop_card.value != "change":
                        self.current_player, self.game_direction = apply_special_card_effects(
                            self.pop_card, self.current_player, self.game_direction, self.player_hands,
                            self.remain_cards,
                            self.player_count)
                        self.reset()

                    # 내는 카드가 special이고 change인 경우
                    elif self.pop_card.is_special() and self.pop_card.value == "change":
                        self.change_index = random.randint(0, 3)
                        self.color_change = self.change_color_list[self.change_index]
                        if self.current_time - self.turn_start_time >= self.delay_time3:
                            self.current_player, self.game_direction = apply_special_card_effects(
                                self.pop_card, self.current_player, self.game_direction, self.player_hands,
                                self.remain_cards,
                                self.player_count)
                            self.board_card.append(self.color_change)
                            self.reset()
                    # 내는 카드가 special이 아닌 경우
                    elif not self.pop_card.is_special():
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()

        # 카드 섞기 발생
        if not self.remain_cards:
            self.board_card, self.remain_cards = card_reshuffle(self.board_card, self.remain_cards)


    def win(self):
        if self.game_over:
            # 마우스 클릭 또는 버튼 클릭시 넘어가야 함
            self.running = False

    def pause(self):
        print("Asdasds")
        self.draw()
        self.paused = False

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
            self.screen.blit(self.turn_arrow_img, (self.user_coordinate[0]-100, self.user_coordinate[1]-130))
        elif self.current_player == 1:
            self.screen.blit(self.turn_arrow_img, (self.computer_coordinate[0][0]-150, self.computer_coordinate[0][1]-80))
        elif self.current_player == 2:
            self.screen.blit(self.turn_arrow_img, (self.computer_coordinate[1][0]-150, self.computer_coordinate[1][1]-80))
        elif self.current_player == 3:
            self.screen.blit(self.turn_arrow_img, (self.computer_coordinate[2][0]-150, self.computer_coordinate[2][1]-80))
        elif self.current_player == 4:
            self.screen.blit(self.turn_arrow_img, (self.computer_coordinate[3][0]-150, self.computer_coordinate[3][1]-80))
        elif self.current_player == 5:
            self.screen.blit(self.turn_arrow_img, (self.computer_coordinate[4][0]-150, self.computer_coordinate[4][1]-80))

        # 남은 카드 더미 그리기
        self.screen.blit(self.remain_cards[0].card_img_back, (self.remain_cards_x_position, self.screen.get_rect().centery - 100))
        # 엎은 카드 그리기
        draw_board_card(self.screen, self.board_card[-1], self.screen.get_rect().centerx, self.screen.get_rect().centery - 100)
        # 유저 카드 그리기
        draw_cards_user(self.screen, self.player_hands[0], self.user_coordinate[0], self.user_coordinate[1], self.max_per_row,
                        self.user_spacing, self.hovered_card_index)
        # ai의 카드를 그린다.
        # ai의 카드를 그린다.
        for i in range(len(self.player_hands) - 1):
            draw_cards_ai(self.screen, self.player_hands[i + 1], self.computer_coordinate[i][0],
                          self.computer_coordinate[i][1],
                          self.max_per_row_com, 20,
                          self.hovered_card_index2,
                          show_back=True)  # 추후 True로 바꾼다.

        # 유저턴이고, 체인지 카드면 체인지카드를 그린다.
        if self.user_turn and self.change_card:
            draw_change_card(self.screen, self.change_color_list, self.x5, self.y5, self.spacing5, self.hovered_change_index)  # 체인지 카드 그림

        # 우노 버튼 표시
        if any(self.one_flags):
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
        if self.user_turn and self.new_drawn_card is None and not self.one_flags[0]:
            self.remaining_time = self.time_limit - (self.current_time - self.turn_start_time)
            self.remaining_time_text = f"턴 남은 시간: {self.remaining_time // 1000}초"
            draw_text(self.screen, self.remaining_time_text, self.font, (255, 255, 255), self.screen.get_rect().centerx/2, 30)
        # draw후 시간제한,턴 넘기기는 draw를 해야지 나옴.
        elif self.user_turn and self.new_drawn_card is not None and not self.one_flags[0]:
            self.after_draw_remaining_time = self.time_limit - (self.current_time - self.user_draw_time)
            self.after_draw_remaining_time_text = f"턴 남은 시간: {self.after_draw_remaining_time // 1000}초"
            draw_text(self.screen, self.after_draw_remaining_time_text, self.font, (255, 255, 255), self.screen.get_rect().centerx/2, 30)
        '''
        # 유저 턴일때, uno버튼 시간
        elif self.user_turn and self.one_flags[0]:
            self.uno_remaining_time = self.uno_delay_time - (self.current_time - self.uno_current_time)
            self.uno_remaining_time_text = f"우노버튼 남은 시간: {self.uno_remaining_time // 1000}초"
            draw_text(self.screen, self.uno_remaining_time_text, self.font, (255, 255, 255), self.screen.get_rect().centerx, 30)
        # 컴퓨터 턴일때, uno버튼 시간
        elif not self.user_turn and any(self.one_flags[1:]):
            self.com_uno_remaining_time = self.uno_delay_time - (self.current_time - self.uno_current_time)
            self.com_uno_remaining_time_text = f"우노버튼 남은 시간: {self.com_uno_remaining_time // 1000}초"
            draw_text(self.screen, self.com_uno_remaining_time_text, self.font, (255, 255, 255), self.screen.get_rect().centerx, 30)
        '''

        if len(self.player_hands[0]) == 0:
            self.winner_message = "User Wins!"
            self.game_over = True
        elif any(len(player_hand) == 0 for player_hand in self.player_hands[1:]):
            self.winner_message = "Computer wins!"
            self.game_over = True

        # 매 프레임마다 화면 업데이트
        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = True
                    self.pause()

    def run(self):
        while self.running:
            self.win()
            Mouse.updateMouseState()
            self.clock.tick(basic.fps)
            self.game()
            self.draw()
            self.event()
