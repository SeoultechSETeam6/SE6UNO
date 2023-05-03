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
        self.winner_message = ""  # 승리 메세지

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

        # 화면 중앙 좌표 계산
        self.image_width, self.image_height = self.direction_img.get_size()
        self.center_x = (self.display_size[0] - self.image_width) // 2
        self.center_y = (self.display_size[1] - self.image_height) // 2

        # 카드 생성 및 셔플
        self.cards = generate_cards(self.color_weakness, self.size_change)
        self.shuffled_cards = shuffle_cards(self.cards)

        # 카드 분배, 유저는 player_hands[0]이고, 나머지는 인공지능으로 설정한다. change는 카드 체인지를 위한 카드들.
        self.player_hands, self.remain_cards = distribute_cards(self.shuffled_cards, self.player_count, self.card_count)
        self.change_color_list = generate_for_change_cards(self.color_weakness, self.size_change)

        # 플레이어 순서 결정
        self.player_order = list(range(self.player_count))
        # 초기 플레이어 순서를 위한 설정 값.
        self.current_player = (random.randint(0, self.player_count - 1))
        # 게임 순서 방향 (1: 정방향, -1: 역방향)
        self.game_direction = 1

        # 보드에 뒤집힌 카드 설정 (카드 한 장을 뽑아서 남은 카드 덱 옆에 보이게 놓기)
        self.board_card = [self.remain_cards.pop()]

    def setting(self):
        pass

    def game(self):
        pass

    def win(self):
        pass

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