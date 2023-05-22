import pygame
import socket
import threading
import random
import json

from scene.single_play import SinglePlay
from controller import game_view, game_data
from controller.card_gen import generate_cards, generate_for_change_cards, Card
from controller.card_shuffle import shuffle_cards, distribute_cards


class MultiPlay(SinglePlay):
    def __init__(self, computer_attends, username, computer_logic):
        self.server_ip = '127.0.0.1'  # 서버 IP 주소 설정 (이 경우 로컬 IP)
        self.server_port = 10613  # 포트 번호 설정

        # 소켓 객체 생성 (TCP)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.game_start = False
        self.settings_data = game_data.load_settings()
        pygame.init()
        pygame.display.set_caption(game_view.GAME_TITLE + ": Multi Play")
        self.clock = pygame.time.Clock()
        self.running = True
        self.draw_override = False

        # single_game 변수
        self.player_count = 1  # 플레이어 수
        self.card_count = 7  # 처음 시작하는 카드 수

        # 글꼴 설정
        self.ui_size = game_view.set_size(self.settings_data["resolution"]["width"])
        self.font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][0])
        self.small_font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][1])

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

        self.computer_color = [None]

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
        self.is_draw = False  # 드로우한 시간인지 아닌지 구분
        self.delay_time = random.randint(1000, 2000)  # 컴퓨터 딜레이 타임1
        self.delay_time2 = random.randint(900, 2000)  # 컴퓨터 딜레이 타임2
        self.delay_time3 = random.randint(900, 2000)  # 컴퓨터 딜레이 타임3

        self.select_color = ["red", "blue", "green", "yellow"]

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

    def recv_data(self):
        while True:
            data = self.client_socket.recv(1024)
            print("recive : ", repr(data.decode()))
            if data.decode() == 'start_game':
                print("start_game")
                self.game_start = True
                self.send_data()
                data = None
                self.run()
            if self.game_start:
                if data is not None:
                    with open(data, "r") as f:
                        self.player_hands = json.load(f)
                        self.remain_cards = json.load(f)
                        self.current_player = json.load(f)
                        self.game_direction = json.load(f)
                        self.board_card = json.load(f)

                        self.is_draw = json.load(f)

                        self.turn_start_time = json.load(f)

                        self.change_card = json.load(f)
                        self.clicked_card_index = json.load(f)
                        self.clicked_change_index = json.load(f)
                        self.change_index = json.load(f)
                        self.playable = json.load(f)
                        self.playable_special_check = json.load(f)
                        self.clicked_change = json.load(f)
                        self.color_change = json.load(f)

                        self.pop_card = json.load(f)
                        self.pop_card_index = json.load(f)
                        self.new_drawn_card = json.load(f)

                        self.clicked_card = json.load(f)
                        self.clicked_remain_cards = json.load(f)
                        self.clicked_next_turn_button = json.load(f)

    def send_msg(self):
        msg = input()
        self.client_socket.sendall(msg.encode())

    def send_data(self):
        with open("./MultiData.json", "w") as f:
            json.dump(self.player_hands, f)
            json.dump(self.remain_cards, f)
            json.dump(self.current_player, f)
            json.dump(self.game_direction, f)
            json.dump(self.board_card, f)
            json.dump(self.is_draw, f)

            json.dump(self.turn_start_time, f)

            json.dump(self.change_card, f)
            json.dump(self.clicked_card_index, f)
            json.dump(self.clicked_change_index, f)
            json.dump(self.change_index, f)
            json.dump(self.playable, f)
            json.dump(self.playable_special_check, f)
            json.dump(self.clicked_change, f)
            json.dump(self.color_change, f)

            json.dump(self.pop_card, f)
            json.dump(self.pop_card_index, f)
            json.dump(self.new_drawn_card, f)

            json.dump(self.clicked_card, f)
            json.dump(self.clicked_remain_cards, f)
            json.dump(self.clicked_next_turn_button, f)
        self.client_socket.sendall("./MultiData.json")

    def connect(self):
        try:
            # 서버에 연결
            self.client_socket.connect((self.server_ip, self.server_port))
            print('>> Connect Server')
            thread = threading.Thread(target=self.recv_data)
            thread.start()
        except:
            print(">> Can't Connect Server")

    def serialize_card(self, obj):
        if isinstance(obj, Card):
            return {'color': obj.color, 'value': obj.value, 'card_img': obj.card_img, 'card_img_back': obj.card_img_back, 'image': obj.image, 'image_cw': obj.image_cw, 'image_back': obj.image_back}
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


game_client = MultiPlay([False, False, False, False, False], 'you', None)
game_client.connect()
while True:
    game_client.send_msg()
