import pygame
import pickle
import random
import time
from mouse import Mouse, MouseState
from slider import Slider
from button import Button
from option.setting_option import Option
from option import save_option as save
from card_gen import generate_cards, generate_for_change_cards, generate_c_stage_cards, generate_c_for_change_cards
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
    random_top_card_color,
    card_reshuffle
)


class SingleGameYhj:
    def __init__(self, computer_attends, username):
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
            self.size_change = basic.change_size[0]
            self.font_size = basic.font_size[0]
            self.button_size = basic.button_size[0]
        elif self.display_size[0] == 1600:
            self.size_change = basic.change_size[1]
            self.font_size = basic.font_size[1]
            self.button_size = basic.button_size[1]
        else:
            self.size_change = basic.change_size[2]
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

        # 플레이어 이름
        self.player_name = self.font.render(username, True, (0, 0, 0))
        self.computer_name = [self.small_font.render("computer1", True, (0, 0, 0)),
                              self.small_font.render("computer2", True, (0, 0, 0)),
                              self.small_font.render("computer3", True, (0, 0, 0)),
                              self.small_font.render("computer4", True, (0, 0, 0)),
                              self.small_font.render("computer5", True, (0, 0, 0))]

        self.computer_attends = computer_attends
        # 로비에서 가져온 정보
        for attend in self.computer_attends:
            if attend:
                self.player_count += 1

        # 게임 이미지를 로드
        self.pause_button_img = basic.scale_by(pygame.image.load("./resources/Image/button_images/pause.png").convert_alpha(), self.size_change)
        self.resume_button_img = basic.scale_by(pygame.image.load("./resources/Image/button_images/resume.png").convert_alpha(), self.size_change)
        self.direction_img = basic.scale_by(pygame.image.load("./resources/Image/direction_images/direction.png").convert_alpha(), self.size_change)
        self.direction_reverse_img = basic.scale_by(pygame.image.load(
            "./resources/Image/direction_images/direction_reverse.png").convert_alpha(), self.size_change)
        self.turn_arrow_img = basic.scale_by(pygame.image.load("./resources/Image/direction_images/turn_arrow.png").convert_alpha(), self.size_change)
        self.next_turn_button_img = basic.scale_by(pygame.image.load("./resources/Image/button_images/next_turn.png").convert_alpha(), self.size_change)
        self.uno_button_img = basic.scale_by(pygame.image.load("./resources/Image/button_images/uno_button.png").convert_alpha(), self.size_change)
        self.uno_button_inactive_img = basic.scale_by(pygame.image.load(
            "./resources/Image/button_images/uno_button_inactive.png").convert_alpha(), self.size_change)
        self.card_back_image = basic.scale_by(pygame.image.load("resources/Image/card_images/card_back.png"), self.size_change)
        self.selected_image = basic.scale_by(pygame.image.load("./resources/Image/selected_check.png"), self.size_change * 0.2)

        # 게임 음악 로드
        self.background_music = pygame.mixer.Sound("./resources/Music/single_mode_play.ogg")
        self.card_distribution_music = pygame.mixer.Sound("./resources/SoundEffect/carddistribution_sound.ogg")
        self.card_place_music = pygame.mixer.Sound("./resources/SoundEffect/cardplace_sound.ogg")
        self.card_shuffle_music = pygame.mixer.Sound("./resources/SoundEffect/cardshuffle_sound.ogg")
        self.Uno_button_music = pygame.mixer.Sound("./resources/SoundEffect/Unobutton_sound.ogg")

        # 카드 생성 및 셔플
        self.cards = generate_cards(self.color_weakness, self.size_change)
        self.shuffled_cards = shuffle_cards(self.cards)

        # 카드 분배, 유저는 player_hands[0]이고, 나머지는 인공지능으로 설정한다. change는 카드 체인지를 위한 카드들.
        self.player_hands, self.remain_cards = distribute_cards(self.shuffled_cards, self.player_count, self.card_count)
        self.change_color_list = generate_for_change_cards(self.color_weakness, self.size_change)

        # 초기 플레이어 순서를 위한 설정 값.
        self.current_player = (random.randint(0, self.player_count - 1))
        # 게임 순서 방향 (1: 정방향, -1: 역방향)
        self.game_direction = 1

        # 보드에 뒤집힌 카드 설정 (카드 한 장을 뽑아서 남은 카드 덱 옆에 보이게 놓기)
        self.board_card = [self.remain_cards.pop()]

        # 기타 정보
        self.paused = False  # 일시정지 초기값
        self.game_over = False  # 게임 오버 초기값
        self.top_card = None  # board카드 맨 위
        self.user_turn = False

        # 턴 시간
        self.time_limit = 10000  # 유저의 턴 시간 제한
        self.current_time = pygame.time.get_ticks()  # 현재 시간
        self.turn_start_time = None  # 턴 시작 시간
        self.delay_time = random.randint(1000, 2000)  # 컴퓨터 딜레이 타임1
        self.delay_time2 = self.delay_time + random.randint(900, 2000)  # 컴퓨터 딜레이 타임2
        self.delay_time3 = self.delay_time2 + random.randint(900, 2000)  # 컴퓨터 딜레이 타임3
        self.computer_action_time = pygame.time.get_ticks() + self.delay_time  # 현재 시간에 랜덤한 지연 시간을 더함

        # 화면 중앙 좌표 계산
        self.image_width, self.image_height = self.direction_img.get_size()
        self.center_x = (self.display_size[0] - self.image_width) // 2
        self.center_y = (self.display_size[1] - self.image_height) // 2

        self.computer_color = ["red", "blue", "green", "yellow"]

        # 컴퓨터 초기 좌표와 카드 색 선호도.
        self.user_coordinate = []
        self.computer_coordinate = []
        self.max_per_row = 15 * self.size_change
        self.max_per_row_com = 20 * self.size_change
        self.user_coordinate.append(30)
        self.user_coordinate.append(self.display_size[1] * 0.7)
        self.user_spacing = self.display_size[1] * 0.08
        self.turn_coordinate = [70, 150 * self.size_change, 150 * self.size_change, 80]
        self.next_turn_co = [0, 150 * self.size_change]
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

            # change카드 좌표, spacing은 공백
            self.x5 = 100
            self.y5 = 100
            self.spacing5 = 200
            # 플레이어들이 카드를 뽑고 남은 카드들의 위치를 잡는데 사용
            self.remain_cards_x_position = (self.screen.get_rect().centerx - 100)
            self.remain_cards_y_position = (self.screen.get_rect().centery - 50)
            self.remain_pos = pygame.Vector2(self.screen.get_rect().centerx, self.screen.get_rect().centery - 100)
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
            self.uno_button_rect.topleft = (150, self.display_size[1] * 0.5)
            self.uno_button_inactive_rect = self.uno_button_inactive_img.get_rect()
            self.uno_button_inactive_rect.topleft = (150, self.display_size[1] * 0.5)
            self.play_drawn_card_button = pygame.Rect(0, 0, 430, 110)
            # animation 메소드 모음
            self.animation_method = {"reverse": self.reverse_animation, "skip": self.skip_animation,
                                     "draw_2": self.draw_2_animation, "bomb": self.bomb_animation,
                                     "shield": self.shield_animation, "change": self.change_animation,
                                     "one_more": self.one_more_animation}

            # Pause Button Check
            self.alreadyPressed = False

    def setting(self):
        pass

    def game(self):
        # 마우스의 위치를 가져옴
        mouse_x, mouse_y = Mouse.getMousePos()
        # 현재 플레이어 결정
        self.top_card = get_top_card(self.board_card)
        # 현재 시각 불러옴
        self.current_time = pygame.time.get_ticks()

        # 플레이어턴, 컴퓨터턴 결정
        if self.current_player == 0:
            self.user_turn = True
        else:
            self.user_turn = False

        if self.user_turn:
            if self.turn_start_time is None:
                self.turn_start_time = pygame.time.get_ticks()
            if self.time_over():
                self.current_player = self.current_player + 1

    def is_uno(self, hand_deck):
        if len(hand_deck) == 1:
            pass

    def time_over(self):
        return True if self.current_time - self.turn_start_time <= self.time_limit else False

    def win(self):
        popup = None
        if len(self.player_hands[0]) == 0:
            popup = basic.scale_by(pygame.image.load("./resources/Image/win.png"), self.size_change)
            self.game_over = True
        elif any(len(player_hand) == 0 for player_hand in self.player_hands[1:]):
            popup = basic.scale_by(pygame.image.load("./resources/Image/lose.png"), self.size_change)
            self.game_over = True
        if self.game_over:
            self.background_music.stop()
            self.card_shuffle_music.stop()
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

    ### 일시정지 버튼 관련 매서드 ###
    def pause_popup(self):
        self.pause_popup_draw()
        self.settings_button.process()
        self.close_button.process()
        self.exit_button.process()
        self.screen.blit(self.pause_popup_surface, self.pause_popup_rect)
        self.screen.blit(self.settings_button.surface, self.settings_button.rect)
        self.screen.blit(self.close_button.surface, self.close_button.rect)
        self.screen.blit(self.exit_button.surface, self.exit_button.rect)

    def pause_popup_draw(self):
        width = self.display_size[0] * 0.4
        height = self.display_size[1] * 0.4
        x = self.display_size[0] // 2 - width // 2
        y = self.display_size[1] // 2 - height // 2
        self.pause_popup_rect = pygame.Rect(x, y, width, height)
        self.pause_popup_surface = pygame.Surface((width, height))
        self.pause_popup_surface.fill((0, 0, 0))

        self.settings_button = Button(self.display_size[0] // 2, self.display_size[1] // 2 * 0.85, width // 2.5,
                                      height // 5, '설정', self.pause_popup_settings_button_event, self.font_size[0])
        self.exit_button = Button(self.display_size[0] // 2, self.display_size[1] // 2 * 1.15, width // 2.5,
                                  height // 5, '게임 나가기', self.pause_popup_exit_button_event, self.font_size[0])
        self.close_button = Button(self.display_size[0] // 2 * 1.3, self.display_size[1] // 2 * 0.7, width // 7,
                                   height // 7, 'X', self.pause_popup_close, self.font_size[0])

    def pause_popup_close(self):
        self.background_music.set_volume(self.sound_volume * self.background_volume)
        self.background_music.play(-1)
        print('일시정지 해제')
        self.turn_start_time += pygame.time.get_ticks() - self.pause_start_time
        self.paused = False

    def pause_popup_exit_button_event(self):
        self.background_music.stop()
        self.card_shuffle_music.stop()
        print('게임 종료 버튼 클릭')
        self.running = False

    def pause_popup_settings_button_event(self):
        self.background_music.stop()
        self.card_shuffle_music.stop()
        print('설정 버튼 클릭됨')
        option = Option()
        option.run()
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
                    self.card_shuffle_music.stop()
                    self.pause_start_time = pygame.time.get_ticks()
                    self.paused = True
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

    ### 일시정지 버튼 관련 메서드 끝 ###

    def place_animation(self, index):
        self.card_place_music.set_volume(self.sound_volume * self.effect_volume)
        self.card_place_music.play(1)
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
            self.clock.tick(basic.fps)
            if pos.distance_to(self.remain_pos) < 1:
                break
            pos = pos.lerp(self.remain_pos, 0.1)
            self.draw()
            self.screen.blit(self.card_back_image, pos)
            pygame.display.flip()

    def draw_animation(self, index):
        remain_pos = pygame.Vector2(self.remain_cards_x_position, self.screen.get_rect().centery - 100)
        self.card_place_music.set_volume(self.sound_volume * self.effect_volume)
        self.card_place_music.play(1)
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
            self.clock.tick(basic.fps)
            if remain_pos.distance_to(pos) < 1:
                break
            remain_pos = remain_pos.lerp(pos, 0.1)
            self.draw()
            self.screen.blit(self.card_back_image, remain_pos)
            pygame.display.flip()

    def draw_2_animation(self, index):
        self.draw()
        self.screen.blit(basic.scale_by(pygame.image.load("./resources/Image/animation/+2.png"), self.size_change),
                         (self.center_x, self.center_y))
        pygame.display.flip()
        time.sleep(0.7)
        self.draw_animation((index - self.game_direction) % self.player_count)
        self.draw_animation((index - self.game_direction) % self.player_count)

    def bomb_animation(self, index):
        self.draw()
        self.screen.blit(
            basic.scale_by(pygame.image.load("./resources/Image/animation/bomb.png"), self.size_change),
            (self.center_x, self.center_y))
        pygame.display.flip()
        time.sleep(0.7)
        remain_pos = [pygame.Vector2(self.remain_cards_x_position, self.screen.get_rect().centery - 100)]
        self.card_place_music.set_volume(self.sound_volume * self.effect_volume)
        self.card_place_music.play(1)
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
            self.clock.tick(basic.fps)
            if remain_pos[0].distance_to(pos[0]) < 1:
                break
            for i in range(len(remain_pos)):
                remain_pos[i] = remain_pos[i].lerp(pos[i], 0.1)
            self.draw()
            if self.game_direction > 0:
                for i in range(self.player_count - 1):
                    self.screen.blit(self.card_back_image, remain_pos[(index + i) % self.player_count])
                print()
            else:
                for i in range(self.player_count - 1):
                    self.screen.blit(self.card_back_image, remain_pos[(index - i) % self.player_count])
            pygame.display.flip()

    def reverse_animation(self, index):
        self.draw()
        self.screen.blit(
            basic.scale_by(pygame.image.load("./resources/Image/animation/reverse.png"), self.size_change),
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
            basic.scale_by(pygame.image.load("./resources/Image/animation/skip.png"), self.size_change), pos)
        pygame.display.flip()
        time.sleep(0.7)

    def one_more_animation(self, index):
        self.draw()
        self.screen.blit(basic.scale_by(pygame.image.load("./resources/Image/animation/-1.png"), self.size_change),
                         (self.center_x, self.center_y))
        pygame.display.flip()
        time.sleep(0.7)

    def change_animation(self, index):
        self.draw()
        self.screen.blit(
            basic.scale_by(pygame.image.load("./resources/Image/animation/change.png"), self.size_change),
            (self.center_x, self.center_y))
        pygame.display.flip()
        time.sleep(0.7)

    def shield_animation(self, index):
        self.draw()
        self.screen.blit(
            basic.scale_by(pygame.image.load("./resources/Image/animation/shield.png"), self.size_change),
            (self.center_x, self.center_y))
        pygame.display.flip()
        time.sleep(0.7)

    def draw(self):
        pass

    def event(self):
        pass

    def run(self):
        self.setting()
        self.background_music.set_volume(self.sound_volume * self.background_volume)
        self.background_music.play(-1)
        self.card_shuffle_music.set_volume(self.sound_volume * self.background_volume)
        self.card_shuffle_music.play(1)
        while self.running:
            self.win()
            Mouse.updateMouseState()
            self.clock.tick(basic.fps)
            # 카드 섞기 발생
            if self.turn_count % 10 == 0:
                self.card_shuffle_music.set_volume(self.sound_volume * self.background_volume)
                self.card_shuffle_music.play(1)
                self.board_card, self.remain_cards = card_reshuffle(self.board_card, self.remain_cards)
            if not self.paused:
                self.game()
            self.draw()
            self.event()
            self.pause_button_process()