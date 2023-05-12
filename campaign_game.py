from single_game_yhj import SingleGameYhj
import pygame
import pickle
import random
import time
from mouse import Mouse, MouseState
from button import Button
from option.setting_option import Option
from card_gen import generate_cards, generate_for_change_cards, generate_c_stage_cards, generate_c_for_change_cards, \
    generate_d_stage_cards
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
    computer_playable_card,
    playable_attack_card,
    user_submit_card,
    com_submit_card,
    apply_special_card_effects,
    random_top_card_color,
    card_reshuffle
)


class StageA(SingleGameYhj):
    def __init__(self):
        super().__init__([False, False, True, False, False], 'You')


class StageB(SingleGameYhj):
    def __init__(self):
        super().__init__([True, False, True, False, True], 'You')
        self.turn_count = 1
        self.cards = generate_cards(self.color_weakness, self.size_change)
        self.shuffled_cards = shuffle_cards(self.cards)
        self.card_count = 28
        self.player_hands, self.remain_cards = distribute_cards(self.shuffled_cards, self.player_count, self.card_count)

        # 나머지 3장 카드 처분
        self.player_hands[0].append(self.remain_cards.pop())
        self.player_hands[1].append(self.remain_cards.pop())
        self.player_hands[2].append(self.remain_cards.pop())


# 5턴 마다 낼 수 있는 카드의 색상이 무작위로 변경됨, 컴퓨터는 낼 수 있는 카드 중 공격카드를 먼저 사용.
class StageC(SingleGameYhj):
    def __init__(self):
        super().__init__([True, False, True, False, False], 'You')
        self.turn_count = 1
        self.dummy_cards = generate_c_stage_cards(self.color_weakness, self.size_change)
        self.dummy_cards_for_change = generate_c_for_change_cards(self.color_weakness, self.size_change)

    def reset(self):
        self.is_draw = False

        self.turn_start_time = None

        self.change_card = False
        self.clicked_card_index = None
        self.clicked_change_index = None
        self.change_index = None
        self.playable = False
        self.playable_attack_check = False
        self.clicked_change = False
        self.color_change = None

        self.pop_card = None  # 뽑은 카드 초기값
        self.pop_card_index = None  # 뽑은 카드 인덱스 숫자 초기값
        self.new_drawn_card = None  # draw한 카드가 어떤 카드인가의 초기값

        self.clicked_card = None  # 클릭 카드 초기값
        self.clicked_remain_cards = False  # remain_cards 클릭 여부 초기값
        self.clicked_next_turn_button = False  # 다음턴 클릭여부 초기값

        self.check_reshuffle_method()
        self.check_change_top_card_method()

    def check_change_top_card_method(self):
        if self.turn_count % 5 == 0:
            self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card,
                                                    self.dummy_cards_for_change)

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
                # 공격 카드 체크
                if self.new_drawn_card is None and self.pop_card is None and self.playable_attack_check is False:
                    self.playable, self.pop_card_index, self.playable_attack_check = \
                        playable_attack_card(self.player_hands[self.current_player], self.board_card)
                    print('공격카드 체크')
                # 유효성 검사
                if self.new_drawn_card is None and self.pop_card is None and self.playable_attack_check is False:
                    self.playable, self.pop_card_index = computer_playable_card(self.player_hands[self.current_player],
                                                                                self.board_card)
                    print('공격카드 외 체크')
                # 카드를 낼 수 있을 때 낸다.
                if self.playable and self.new_drawn_card is None and self.pop_card is None:
                    self.place_animation(self.current_player)
                    self.pop_card = self.player_hands[self.current_player][self.pop_card_index]
                    self.board_card, self.player_hands[self.current_player] = com_submit_card(self.pop_card,
                                                                                              self.pop_card_index,
                                                                                              self.board_card,
                                                                                              self.player_hands
                                                                                              [self.current_player])
                # 카드를 낼 수 없을 때 드로우 한다.
                elif not self.playable and self.new_drawn_card is None and self.pop_card is None:
                    self.draw_animation(self.current_player)
                    self.new_drawn_card = self.remain_cards.pop()
                    self.player_hands[self.current_player].append(self.new_drawn_card)
                    self.turn_start_time = pygame.time.get_ticks()
                # 드로우한 카드가 낼 수 있는 경우
                elif self.new_drawn_card is not None and is_valid_move(self.new_drawn_card, self.top_card) and \
                        self.pop_card is None:
                    if self.current_time - self.turn_start_time >= self.delay_time2:
                        self.place_animation(self.current_player)
                        self.pop_card = self.new_drawn_card
                        self.pop_card_index = self.player_hands[self.current_player].index(self.pop_card)
                        self.board_card, self.player_hands[self.current_player] = com_submit_card(self.pop_card,
                                                                                                  self.pop_card_index,
                                                                                                  self.board_card,
                                                                                                  self.player_hands
                                                                                                  [self.current_player])
                # 드로우한 카드를 낼 수 없는 경우
                elif self.new_drawn_card is not None and not is_valid_move(self.new_drawn_card, self.top_card) and \
                        self.pop_card is None:
                    if self.current_time - self.turn_start_time >= self.delay_time2:
                        self.turn_count = self.turn_count + 1
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()


class StageD(SingleGameYhj):
    def __init__(self):
        super().__init__([False, True, True, True, True], 'You')
        self.cards = generate_d_stage_cards(self.color_weakness, self.size_change)
