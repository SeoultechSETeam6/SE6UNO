from scene.single_play import SinglePlay
import pygame
import random
from controller.game_view import scale_by
from controller.mouse import Mouse, MouseState
from controller.card_gen import (
    generate_cards,
    generate_a_stage_cards,
    generate_c_stage_cards,
    generate_c_for_change_cards,
    generate_d_stage_cards
)
from controller.card_shuffle import shuffle_cards, distribute_cards, stage_a_distribute
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
    playable_attack_card,
    user_submit_card,
    com_submit_card,
    apply_special_card_effects,
    random_top_card_color,
    card_reshuffle)


class StageA(SinglePlay):
    def __init__(self):
        super().__init__([False, False, True, False, False], 'You')
        self.regular_cards, self.special_cards = generate_a_stage_cards(self.settings_data["color_weakness"],
                                                                        self.ui_size["change"])
        self.player_hands, self.remain_cards = stage_a_distribute(self.player_count, self.regular_cards,
                                                                  self.special_cards, self.card_count)
        self.stage = "A"

    def turn_and_reset(self):
        if self.new_drawn_card is not None:
            if self.pop_card is None:
                pass
            elif self.pop_card.is_special() is False:
                self.current_player = (self.current_player + self.game_direction) % self.player_count
            self.turn_end_method()
        elif self.new_drawn_card is None:
            self.reset()

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
                # 기술 카드 체크
                if self.new_drawn_card is None and self.pop_card is None and self.playable_special_check is False:
                    self.playable, self.pop_card_index, self.playable_special_check = \
                        playable_attack_card(self.player_hands[self.current_player], self.board_card)
                    print('기술카드 체크')
                # 유효성 검사
                if self.new_drawn_card is None and self.pop_card is None and self.playable_special_check is False:
                    self.playable, self.pop_card_index = computer_playable_card(self.player_hands[self.current_player],
                                                                                self.board_card)
                    print('기술카드 외 체크')
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
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.turn_end_method()

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
                self.turn_and_reset()
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
                        self.turn_and_reset()
                else:
                    self.change_index = random.randint(0, 3)
                    self.color_change = self.change_color_list[self.change_index]
                    if self.current_time - self.turn_start_time >= self.delay_time3:
                        self.current_player, self.game_direction = apply_special_card_effects(
                            self.pop_card, self.current_player, self.game_direction, self.player_hands,
                            self.remain_cards, self.player_count, self.stage)
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.board_card.append(self.color_change)
                        self.turn_and_reset()
            # 내는 카드가 special이 아닌 경우
            elif len(self.remain_cards) > 5 and not self.pop_card.is_special():
                self.turn_and_reset()
            # 5장 이하인 경우에는 특수카드 발동x, 그냥 넘어감.
            elif len(self.remain_cards) <= 5:
                print('5장 미만 발동')
                self.turn_and_reset()


class StageB(SinglePlay):
    def __init__(self):
        super().__init__([True, False, True, False, True], 'You')
        self.turn_count = 1
        self.cards = generate_cards(self.settings_data["color_weakness"], self.ui_size["change"])
        self.shuffled_cards = shuffle_cards(self.cards)
        self.player_hands, self.remain_cards = distribute_cards(self.shuffled_cards, self.player_count, self.card_count)
        # 가장 첫번째 카드를 빼놓기
        saved_card = self.remain_cards.pop(0)

        # 나머지 카드를 플레이어들에게 순차적으로 나눠주기
        player_index = 0
        while self.remain_cards:
            self.player_hands[player_index].append(self.remain_cards.pop())
            player_index = (player_index + 1) % self.player_count

        # saved_card를 다시 remain_cards에 추가하기
        self.remain_cards.append(saved_card)

        self.stage = "B"


# 5턴 마다 낼 수 있는 카드의 색상이 무작위로 변경됨, 컴퓨터는 낼 수 있는 카드 중 공격카드를 먼저 사용.
class StageC(SinglePlay):
    def __init__(self):
        super().__init__([True, False, True, False, False], 'You')
        self.turn_count = 1
        self.dummy_cards = generate_c_stage_cards(self.settings_data["color_weakness"], self.ui_size["change"])
        self.dummy_cards_c = generate_c_for_change_cards(self.settings_data["color_weakness"], self.ui_size["change"])

        self.stage = "C"

    def turn_end_method(self):
        self.reset()
        self.check_reshuffle_method()
        self.check_change_top_card_method()
        print("턴카운트: ", self.turn_count)

    def check_change_top_card_method(self):
        if self.turn_count % 5 == 0:
            self.board_card = random_top_card_color(self.board_card[-1], self.dummy_cards, self.board_card,
                                                    self.dummy_cards_c)

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
                if self.new_drawn_card is None and self.pop_card is None and self.playable_special_check is False:
                    self.playable, self.pop_card_index, self.playable_special_check = \
                        playable_attack_card(self.player_hands[self.current_player], self.board_card)
                    print('공격카드 체크')
                # 유효성 검사
                if self.new_drawn_card is None and self.pop_card is None and self.playable_special_check is False:
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
                        self.turn_end_method()


# 공격 카드, 폭탄 카드가 다수 추가됨
class StageD(SinglePlay):
    def __init__(self):
        super().__init__([True, False, True, False, True], 'You')
        self.turn_count = 1
        self.cards = generate_d_stage_cards(self.settings_data["color_weakness"], self.ui_size["change"])

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
                if self.new_drawn_card is None and self.pop_card is None and self.playable_special_check is False:
                    self.playable, self.pop_card_index, self.playable_special_check = \
                        playable_attack_card(self.player_hands[self.current_player], self.board_card)
                    print('공격카드 체크')
                # 유효성 검사
                if self.new_drawn_card is None and self.pop_card is None and self.playable_special_check is False:
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
                        self.turn_end_method()
