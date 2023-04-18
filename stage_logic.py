from single_game import SingleGame
import pygame
import pickle
import random
import time
import math
from mouse import Mouse, MouseState
from slider import Slider
from button import Button
from option import save_option as save
from card_gen import generate_cards, generate_for_change_cards, generate_a_stage_cards, generate_c_stage_cards, generate_c_for_change_cards, generate_d_stage_cards
from card_shuffle import shuffle_cards, distribute_cards, stage_a_distribute
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
    find_combos,
    card_reshuffle
)


class StageA(SingleGame):
    def __init__(self):
        super().__init__([False, False, True, False, False], 'You')
        self.regular_cards, self.special_cards = generate_a_stage_cards(self.color_weakness, self.size_change)
        self.player_hands, self.remain_cards = stage_a_distribute(self.player_count, self.regular_cards, self.special_cards, self.card_count)


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
                self.Uno_button_music.set_volume(self.sound_volume * self.effect_volume)
                self.Uno_button_music.play(1)
                self.user_uno_clicked = True
        self.hovered_card_index = find_hovered_card(self.player_hands[0], self.user_coordinate[0],
                                                    self.user_coordinate[1], self.user_spacing, mouse_x, mouse_y, self.max_per_row, self.hovered_card_index)
        self.hovered_change_index = find_hovered_change(self.change_color_list, self.x5, self.y5, self.spacing5, mouse_x, mouse_y, self.hovered_card_index)

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
                    self.draw_animation(self.current_player)
                    self.user_draw_time = pygame.time.get_ticks()
                    self.player_hands[0].append(self.remain_cards.pop())
                    self.new_drawn_card = self.player_hands[0][-1]
                # 카드를 드로우 하고 턴을 넘기는 함수.
                elif self.new_drawn_card is not None and self.clicked_next_turn_button:
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.reset()
                    self.turn_count = self.turn_count + 1
                # 카드를 드로우 하고, 드로우한 카드를 내는 함수.
                elif self.new_drawn_card is not None and self.pop_card is None:
                    # 유효성 검사 및 클릭카드가 new_drawn_card인지 확인
                    if self.new_drawn_card is not None and is_valid_move(self.new_drawn_card, self.top_card) and self.clicked_card == self.new_drawn_card and self.pop_card is None:
                        self.place_animation(self.current_player)
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
                        self.place_animation(self.current_player)
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
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.reset()
                            self.turn_count = self.turn_count + 1
                        # 내는 카드가 special이고, change일 경우
                        elif self.pop_card.is_special() and self.pop_card.value == "change":
                            self.change_card = True
                            if self.clicked_change_index is not None:
                                self.color_change = self.change_color_list[self.clicked_change_index]
                                self.current_player, self.game_direction = apply_special_card_effects(
                                    self.pop_card, self.current_player, self.game_direction,
                                    self.player_hands, self.remain_cards, self.player_count)
                                self.animation_method[self.pop_card.value](self.current_player)
                                self.board_card.append(self.color_change)
                                self.reset()
                                self.turn_count = self.turn_count + 1
                        # 내는 카드가 special이 아닌 경우
                        elif not self.pop_card.is_special():
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.reset()
                            self.turn_count = self.turn_count + 1
                elif not self.uno_check:
                    # 내는 카드가 special이고 change가 아닐 때,
                    if self.pop_card.is_special() and self.pop_card.value != "change":
                        self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                     self.current_player,
                                                                                     self.game_direction,
                                                                                     self.player_hands,
                                                                                     self.remain_cards,
                                                                                     self.player_count)
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.reset()
                        self.turn_count = self.turn_count + 1
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
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.board_card.append(self.color_change)
                            self.reset()
                            self.turn_count = self.turn_count + 1
                    # 내는 카드가 special이 아닌 경우
                    else:
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        self.turn_count = self.turn_count + 1

            # 우노 시간 넘기면 발동
            if self.pop_card is not None and self.one_flags[0]:
                if self.current_time - self.uno_current_time >= self.uno_delay_time:
                    self.draw_animation(self.current_player)
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
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.reset()
                        self.turn_count = self.turn_count + 1

                    # 내는 카드가 special이 아닌 경우
                    elif not self.pop_card.is_special():
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        self.turn_count = self.turn_count + 1
            # 우노 마치고, change_card 제한시간 넘는 경우
            elif self.change_uno_expire:
                if self.user_turn and self.current_time - self.turn_start_time >= self.time_limit:
                    self.current_player, self.game_direction = apply_special_card_effects(
                        self.pop_card, self.current_player, self.game_direction, self.player_hands,
                        self.remain_cards,
                        self.player_count)
                    self.animation_method[self.pop_card.value](self.current_player)
                    self.reset()
                    self.turn_count = self.turn_count + 1
            # 유저의 턴일 때 시간이 초과되면 드로우하고 턴을 넘김
            elif self.new_drawn_card is None:
                if self.user_turn and self.current_time - self.turn_start_time >= self.time_limit:
                    self.draw_animation(self.current_player)
                    self.new_drawn_card = self.remain_cards.pop()
                    self.player_hands[self.current_player].append(self.new_drawn_card)  # 카드를 드로우
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.reset()
                    self.turn_count = self.turn_count + 1

            # 유저가 드로우를 하고 시간이 초과되면 턴을 그냥 넘김
            elif self.new_drawn_card is not None:
                if self.user_turn and self.current_time - self.user_draw_time >= self.time_limit:
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.reset()
                    self.turn_count = self.turn_count + 1

        # 컴퓨터 턴 처리
        if not self.user_turn:
            if self.current_time >= self.computer_action_time:  # 설정한 시간이 되면 컴퓨터가 행동함
                # 처음 유효성 검사
                if self.new_drawn_card is None and self.pop_card is None:
                    self.playable, self.pop_card_index = computer_playable_card(self.player_hands[self.current_player], self.board_card)
                # 카드를 낼 수 있을 때 낸다.
                elif self.playable and self.new_drawn_card is None and self.pop_card is None:
                    self.place_animation(self.current_player)
                    self.pop_card = self.player_hands[self.current_player][self.pop_card_index]
                    self.board_card, self.player_hands[self.current_player] = com_submit_card\
                        (self.pop_card, self.pop_card_index, self.board_card, self.player_hands[self.current_player])
                    self.uno_check = check_uno(self.player_hands[self.current_player])
                    if self.uno_check:
                        self.one_flags, self.uno_current_time, self.uno_delay_time = is_uno(self.one_flags, self.current_player)
                # 카드를 낼 수 없을 때 드로우 한다.
                elif not self.playable and self.new_drawn_card is None and self.pop_card is None:
                    self.draw_animation(self.current_player)
                    self.new_drawn_card = self.remain_cards.pop()
                    self.player_hands[self.current_player].append(self.new_drawn_card)
                    self.turn_count = self.turn_count + 1
                # 드로우한 카드가 낼 수 있는 경우
                elif self.new_drawn_card is not None and is_valid_move(self.new_drawn_card, self.top_card) and self.pop_card is None:
                    if self.current_time - self.turn_start_time >= self.delay_time2:
                        self.place_animation(self.current_player)
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
                        self.turn_count = self.turn_count + 1
                # 컴퓨터가 우노이고, 유저가 우노를 클릭했을 경우
                elif self.uno_check:
                    if self.user_uno_clicked:
                        self.draw_animation(self.current_player)
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
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.reset()
                            self.turn_count = self.turn_count + 1
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
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.reset()
                            self.turn_count = self.turn_count + 1
                        # 컴퓨터가 낸 카드가 special이 아닌 경우
                        elif not self.pop_card.is_special():
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.reset()
                            self.turn_count = self.turn_count + 1
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
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.reset()
                        self.turn_count = self.turn_count + 1
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
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.board_card.append(self.color_change)
                            self.reset()
                            self.turn_count = self.turn_count + 1
                    # 내는 카드가 special이 아닌 경우
                    elif not self.pop_card.is_special():
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        self.turn_count = self.turn_count + 1

            # 컴퓨터의 턴일 때 시간이 초과되면 우노를 넘긴다.
            if any(self.one_flags[1:]) and not self.user_turn:
                if self.current_time - self.uno_current_time >= self.uno_delay_time:
                    # 내는 카드가 special이고, change가 아닐 경우
                    if self.pop_card.is_special() and self.pop_card.value != "change":
                        self.current_player, self.game_direction = apply_special_card_effects(
                            self.pop_card, self.current_player, self.game_direction, self.player_hands,
                            self.remain_cards,
                            self.player_count)
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.reset()
                        self.turn_count = self.turn_count + 1

                    # 내는 카드가 special이고 change인 경우
                    elif self.pop_card.is_special() and self.pop_card.value == "change":
                        self.change_index = random.randint(0, 3)
                        self.color_change = self.change_color_list[self.change_index]
                        if self.current_time - self.turn_start_time >= self.delay_time3:
                            self.current_player, self.game_direction = apply_special_card_effects(
                                self.pop_card, self.current_player, self.game_direction, self.player_hands,
                                self.remain_cards,
                                self.player_count)
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.board_card.append(self.color_change)
                            self.reset()
                            self.turn_count = self.turn_count + 1
                    # 내는 카드가 special이 아닌 경우
                    elif not self.pop_card.is_special():
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        self.turn_count = self.turn_count + 1


class StageB(SingleGame):
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
                                                    self.user_coordinate[1], self.user_spacing, mouse_x, mouse_y,
                                                    self.max_per_row, self.hovered_card_index)
        self.hovered_change_index = find_hovered_change(self.change_color_list, self.x5, self.y5, self.spacing5,
                                                        mouse_x, mouse_y, self.hovered_card_index)

        # 현재 플레이어가 유저인지 확인
        if self.user_turn:
            if self.turn_start_time is None:
                self.turn_start_time = pygame.time.get_ticks()
            if Mouse.getMouseState() == MouseState.CLICK:
                self.clicked_card_index, self.clicked_card = get_clicked_card(self.player_hands[0],
                                                                              self.user_coordinate[0],
                                                                              self.user_coordinate[1],
                                                                              self.user_spacing, mouse_x, mouse_y,
                                                                              self.max_per_row)
                # remain_cards 클릭 확인
                self.clicked_remain_cards = self.remain_cards_rect.collidepoint(mouse_x, mouse_y)
                # next_turn_button 클릭 확인
                self.clicked_next_turn_button = self.next_turn_button_rect.collidepoint(mouse_x, mouse_y)
                # change 클릭 확인
                self.clicked_change_index, self.clicked_change = get_clicked_change(self.change_color_list, self.x5,
                                                                                    self.y5, self.spacing5, mouse_x,
                                                                                    mouse_y)
            if self.clicked_card is not None or self.clicked_remain_cards or self.clicked_next_turn_button or self.user_uno_clicked:
                # 카드를 드로우함
                if self.clicked_remain_cards and self.new_drawn_card is None and self.pop_card is None and len(self.remain_cards) > 5:
                    self.draw_animation(self.current_player)
                    self.user_draw_time = pygame.time.get_ticks()
                    self.player_hands[0].append(self.remain_cards.pop())
                    self.new_drawn_card = self.player_hands[0][-1]
                # 카드를 드로우 하고 턴을 넘기는 함수.
                elif self.new_drawn_card is not None and self.clicked_next_turn_button:
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.reset()
                    self.turn_count = self.turn_count + 1
                # 카드를 드로우 하고, 드로우한 카드를 내는 함수.
                elif self.new_drawn_card is not None and self.pop_card is None:
                    # 유효성 검사 및 클릭카드가 new_drawn_card인지 확인
                    if self.new_drawn_card is not None and is_valid_move(self.new_drawn_card,
                                                                         self.top_card) and self.clicked_card == self.new_drawn_card and self.pop_card is None:
                        self.place_animation(self.current_player)
                        if len(self.remain_cards) > 3:  # 리메인 카드에 3장 이상 있을 때, 드로우 가능
                            self.board_card, self.player_hands[self.current_player], self.pop_card = user_submit_card \
                                (self.clicked_card, self.clicked_card_index, self.board_card,
                                 self.player_hands[self.current_player])
                            self.uno_check = check_uno(self.player_hands[0])
                        if self.uno_check:
                            self.one_flags, self.uno_current_time, self.uno_delay_time = is_uno(self.one_flags,
                                                                                                self.current_player)
                # 카드를 드로우하지 않고, 카드를 냄
                elif self.new_drawn_card is None and self.pop_card is None:
                    # 유효성 검사
                    if self.clicked_card is not None and is_valid_move(self.clicked_card, self.top_card):
                        self.place_animation(self.current_player)
                        self.board_card, self.player_hands[self.current_player], self.pop_card = user_submit_card \
                            (self.clicked_card, self.clicked_card_index, self.board_card,
                             self.player_hands[self.current_player])
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
                            if len(self.remain_cards) > 5:
                                self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                                      self.current_player,
                                                                                                      self.game_direction,
                                                                                                      self.player_hands,
                                                                                                      self.remain_cards,
                                                                                                      self.player_count)
                                self.animation_method[self.pop_card.value](self.current_player)
                                self.reset()
                                self.turn_count = self.turn_count + 1
                            elif len(self.remain_cards) <= 5:
                                self.current_player = (self.current_player + self.game_direction) % self.player_count
                                self.animation_method[self.pop_card.value](self.current_player)
                                self.reset()
                                self.turn_count = self.turn_count + 1
                        # 내는 카드가 special이고, change일 경우
                        elif self.pop_card.is_special() and self.pop_card.value == "change":
                            if len(self.remain_cards) > 5:
                                self.change_card = True
                                if self.clicked_change_index is not None:
                                    self.color_change = self.change_color_list[self.clicked_change_index]
                                    self.current_player, self.game_direction = apply_special_card_effects(
                                        self.pop_card, self.current_player, self.game_direction,
                                        self.player_hands, self.remain_cards, self.player_count)
                                    self.animation_method[self.pop_card.value](self.current_player)
                                    self.board_card.append(self.color_change)
                                    self.reset()
                                    self.turn_count = self.turn_count + 1
                            elif len(self.remain_cards) < 5:
                                self.current_player = (self.current_player + self.game_direction) % self.player_count
                                self.animation_method[self.pop_card.value](self.current_player)
                                self.reset()
                                self.turn_count = self.turn_count + 1
                        # 내는 카드가 special이 아닌 경우
                        elif not self.pop_card.is_special():
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.reset()
                            self.turn_count = self.turn_count + 1
                elif not self.uno_check:
                    # 내는 카드가 special이고 change가 아닐 때,
                    if self.pop_card.is_special() and self.pop_card.value != "change":
                        if len(self.remain_cards) > 5:
                            self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                                  self.current_player,
                                                                                                  self.game_direction,
                                                                                                  self.player_hands,
                                                                                                  self.remain_cards,
                                                                                                  self.player_count)
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.reset()
                            self.turn_count = self.turn_count + 1
                        elif len(self.remain_cards) <= 5:
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.reset()
                            self.turn_count = self.turn_count + 1
                    # 내는 카드가 change인 경우
                    elif self.pop_card.value == "change":
                        if len(self.remain_cards) > 5:
                            self.change_card = True
                            if self.clicked_change_index is not None:
                                self.color_change = self.change_color_list[self.clicked_change_index]
                                self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                                      self.current_player,
                                                                                                      self.game_direction,
                                                                                                      self.player_hands,
                                                                                                      self.remain_cards,
                                                                                                      self.player_count)
                                self.animation_method[self.pop_card.value](self.current_player)
                                self.board_card.append(self.color_change)
                                self.reset()
                                self.turn_count = self.turn_count + 1
                        elif len(self.remain_cards) <= 5:
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.reset()
                            self.turn_count = self.turn_count + 1
                    # 내는 카드가 special이 아닌 경우
                    else:
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        self.turn_count = self.turn_count + 1

            # 우노 시간 넘기면 발동
            if self.pop_card is not None and self.one_flags[0]:
                if self.current_time - self.uno_current_time >= self.uno_delay_time:
                    self.draw_animation(self.current_player)
                    # remain_cards가 5 이상이어야 카드를 뽑을 수 있음
                    if len(self.remain_cards) > 5:
                        self.uno_drawn_card = self.remain_cards.pop()
                        self.player_hands[0].append(self.uno_drawn_card)
                    # 내는 카드가 special이고, change일 경우
                    if self.pop_card.is_special() and self.pop_card.value == "change":
                        if len(self.remain_cards) > 5:
                            self.one_flags[0] = False
                            self.uno_check = False
                            self.user_uno_clicked = False
                            self.change_uno_expire = True
                            self.reset()
                            self.turn_count = self.turn_count + 1
                        elif len(self.remain_cards) <= 5:
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.reset()
                            self.turn_count = self.turn_count + 1
                    # 내는 카드가 special이고, change가 아닐 경우
                    elif self.pop_card.is_special() and self.pop_card.value != "change":
                        if len(self.remain_cards) > 5:
                            self.current_player, self.game_direction = apply_special_card_effects(
                                self.pop_card, self.current_player, self.game_direction, self.player_hands,
                                self.remain_cards,
                                self.player_count)
                            self.animation_method[self.pop_card.value](self.current_player)
                        elif len(self.remain_cards) <= 5:
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        self.turn_count = self.turn_count + 1

                    # 내는 카드가 special이 아닌 경우
                    elif not self.pop_card.is_special():
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        self.turn_count = self.turn_count + 1
            # 우노 마치고, change_card 제한시간 넘는 경우
            elif self.change_uno_expire:
                if self.user_turn and self.current_time - self.turn_start_time >= self.time_limit:
                    if len(self.remain_cards) > 5:
                        self.current_player, self.game_direction = apply_special_card_effects(
                            self.pop_card, self.current_player, self.game_direction, self.player_hands,
                            self.remain_cards,
                            self.player_count)
                    elif len(self.remain_cards) <= 5:
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.animation_method[self.pop_card.value](self.current_player)
                    self.reset()
                    self.turn_count = self.turn_count + 1
            # 유저의 턴일 때 시간이 초과되면 드로우하고 턴을 넘김
            elif self.new_drawn_card is None:
                if self.user_turn and self.current_time - self.turn_start_time >= self.time_limit:
                    self.draw_animation(self.current_player)
                    if len(self.remain_cards) > 5:
                        self.new_drawn_card = self.remain_cards.pop()
                        self.player_hands[self.current_player].append(self.new_drawn_card)  # 카드를 드로우
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.reset()
                    self.turn_count = self.turn_count + 1

            # 유저가 드로우를 하고 시간이 초과되면 턴을 그냥 넘김
            elif self.new_drawn_card is not None:
                if self.user_turn and self.current_time - self.user_draw_time >= self.time_limit:
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.reset()
                    self.turn_count = self.turn_count + 1

        # 컴퓨터 턴 처리
        if not self.user_turn:
            if self.current_time >= self.computer_action_time:  # 설정한 시간이 되면 컴퓨터가 행동함
                # 처음 유효성 검사
                if self.new_drawn_card is None and self.pop_card is None:
                    self.playable, self.pop_card_index = computer_playable_card(self.player_hands[self.current_player],
                                                                                self.board_card)
                # 카드를 낼 수 있을 때 낸다.
                if self.playable and self.new_drawn_card is None and self.pop_card is None:
                    self.place_animation(self.current_player)
                    self.pop_card = self.player_hands[self.current_player][self.pop_card_index]
                    self.board_card, self.player_hands[self.current_player] = com_submit_card \
                        (self.pop_card, self.pop_card_index, self.board_card, self.player_hands[self.current_player])
                    self.uno_check = check_uno(self.player_hands[self.current_player])
                    if self.uno_check:
                        self.one_flags, self.uno_current_time, self.uno_delay_time = is_uno(self.one_flags,
                                                                                            self.current_player)
                # 카드를 낼 수 없을 때 드로우 한다.
                elif not self.playable and self.new_drawn_card is None and self.pop_card is None:
                    self.draw_animation(self.current_player)
                    if len(self.remain_cards) > 5:
                        self.new_drawn_card = self.remain_cards.pop()
                        self.player_hands[self.current_player].append(self.new_drawn_card)
                    elif len(self.remain_cards) <= 5:
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.turn_count = self.turn_count + 1
                # 드로우한 카드가 낼 수 있는 경우
                elif self.new_drawn_card is not None and is_valid_move(self.new_drawn_card,
                                                                       self.top_card) and self.pop_card is None:
                    if self.current_time - self.turn_start_time >= self.delay_time2:
                        self.place_animation(self.current_player)
                        self.pop_card = self.new_drawn_card
                        self.pop_card_index = self.player_hands[self.current_player].index(self.pop_card)
                        self.board_card, self.player_hands[self.current_player] = com_submit_card \
                            (self.pop_card, self.pop_card_index, self.board_card,
                             self.player_hands[self.current_player])
                        self.uno_check = check_uno(self.player_hands[self.current_player])
                        if self.uno_check:
                            self.one_flags, self.uno_current_time, self.uno_delay_time = is_uno(self.one_flags,
                                                                                                self.current_player)
                # 드로우한 카드를 낼 수 없는 경우
                elif self.new_drawn_card is not None and not is_valid_move(self.new_drawn_card,
                                                                           self.top_card) and self.pop_card is None:
                    if self.current_time - self.turn_start_time >= self.delay_time2:
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.new_drawn_card = None
                        self.computer_action_time = pygame.time.get_ticks() + self.delay_time
                        self.turn_start_time = pygame.time.get_ticks()
                        self.turn_count = self.turn_count + 1
                # 컴퓨터가 우노이고, 유저가 우노를 클릭했을 경우
                elif self.uno_check:
                    if self.user_uno_clicked:
                        self.draw_animation(self.current_player)
                        self.one_flags[self.current_player] = False
                        if len(self.remain_cards) > 5 and self.uno_drawn_card is not None:
                            self.uno_drawn_card = self.remain_cards.pop()
                            self.player_hands[self.current_player].append(self.uno_drawn_card)
                        # 컴퓨터가 낸 카드가 special일 경우
                        if self.pop_card.is_special() and self.pop_card.value != "change":
                            if len(self.remain_cards) > 5:
                                self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                                      self.current_player,
                                                                                                      self.game_direction,
                                                                                                      self.player_hands,
                                                                                                      self.remain_cards,
                                                                                                      self.player_count)
                            elif len(self.remain_cards) <= 5:
                                self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.reset()
                            self.turn_count = self.turn_count + 1
                        # 컴퓨터가 낸 카드가 change일 경우
                        elif self.pop_card.value == "change":
                            self.change_index = random.randint(0, 3)
                            self.color_change = self.change_color_list[self.change_index]
                            self.board_card.append(self.color_change)
                            if len(self.remain_cards) > 5:
                                self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                                  self.current_player,
                                                                                                  self.game_direction,
                                                                                                  self.player_hands,
                                                                                                  self.remain_cards,
                                                                                                  self.player_count)
                            elif len(self.remain_cards) <= 5:
                                self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.reset()
                            self.turn_count = self.turn_count + 1
                        # 컴퓨터가 낸 카드가 special이 아닌 경우
                        elif not self.pop_card.is_special():
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.reset()
                            self.turn_count = self.turn_count + 1
                # 컴퓨터가 우노가 아니고, 컴퓨터가 카드를 낸 경우
                elif not self.uno_check and self.pop_card is not None:
                    # 내는 카드가 special이고 change가 아닐 경우
                    if self.pop_card.is_special() and self.pop_card.value != "change":
                        if len(self.remain_cards) > 5:
                            self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                              self.current_player,
                                                                                              self.game_direction,
                                                                                              self.player_hands,
                                                                                              self.remain_cards,
                                                                                              self.player_count)
                        elif len(self.remain_cards) <= 5:
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.reset()
                        self.turn_count = self.turn_count + 1
                    # 내는 카드가 special이고, change일 경우
                    elif self.pop_card.is_special() and self.pop_card.value == "change":
                        if self.current_time - self.turn_start_time >= self.delay_time3:
                            if len(self.remain_cards) > 5:
                                self.change_index = random.randint(0, 3)
                                self.color_change = self.change_color_list[self.change_index]
                                self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                                  self.current_player,
                                                                                                  self.game_direction,
                                                                                                  self.player_hands,
                                                                                                  self.remain_cards,
                                                                                                  self.player_count)
                                self.animation_method[self.pop_card.value](self.current_player)
                                self.board_card.append(self.color_change)
                                self.reset()
                                self.turn_count = self.turn_count + 1
                            elif len(self.remain_cards) <= 5:
                                self.current_player = (self.current_player + self.game_direction) % self.player_count
                                self.animation_method[self.pop_card.value](self.current_player)
                                self.reset()
                                self.turn_count = self.turn_count + 1
                    # 내는 카드가 special이 아닌 경우
                    elif not self.pop_card.is_special():
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        self.turn_count = self.turn_count + 1
            # 컴퓨터의 턴일 때 시간이 초과되면 우노를 넘긴다.
            if any(self.one_flags[1:]) and not self.user_turn:
                if self.current_time - self.uno_current_time >= self.uno_delay_time:
                    # 내는 카드가 special이고, change가 아닐 경우
                    if self.pop_card.is_special() and self.pop_card.value != "change":
                        if len(self.remain_cards) > 5:
                            self.current_player, self.game_direction = apply_special_card_effects(
                                self.pop_card, self.current_player, self.game_direction, self.player_hands,
                                self.remain_cards,
                                self.player_count)
                        elif len(self.remain_cards) <= 5:
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.reset()
                        self.turn_count = self.turn_count + 1
                    # 내는 카드가 special이고 change인 경우
                    elif self.pop_card.is_special() and self.pop_card.value == "change":
                        if len(self.remain_cards) > 5:
                            self.change_index = random.randint(0, 3)
                            self.color_change = self.change_color_list[self.change_index]
                            if self.current_time - self.turn_start_time >= self.delay_time3:
                                self.current_player, self.game_direction = apply_special_card_effects(
                                    self.pop_card, self.current_player, self.game_direction, self.player_hands,
                                    self.remain_cards,
                                    self.player_count)
                                self.animation_method[self.pop_card.value](self.current_player)
                                self.board_card.append(self.color_change)
                                self.reset()
                                self.turn_count = self.turn_count + 1
                        elif len(self.remain_cards) <= 5:
                            if self.current_time - self.turn_start_time >= self.delay_time3:
                                self.current_player = (self.current_player + self.game_direction) % self.player_count
                                self.animation_method[self.pop_card.value](self.current_player)
                                self.board_card.append(self.color_change)
                                self.reset()
                                self.turn_count = self.turn_count + 1
                    # 내는 카드가 special이 아닌 경우
                    elif not self.pop_card.is_special():
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        self.turn_count = self.turn_count + 1


class StageC(SingleGame):
    def __init__(self):
        super().__init__([True, False, True, False, False], 'You')
        self.turn_count = 1
        self.dummy_cards = generate_c_stage_cards(self.color_weakness, self.size_change)
        self.dummy_cards_c = generate_c_for_change_cards(self.color_weakness, self.size_change)

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
                                                    self.user_coordinate[1], self.user_spacing, mouse_x, mouse_y, self.max_per_row, self.hovered_card_index)
        self.hovered_change_index = find_hovered_change(self.change_color_list, self.x5, self.y5, self.spacing5, mouse_x, mouse_y, self.hovered_card_index)

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
                    self.draw_animation(self.current_player)
                    self.user_draw_time = pygame.time.get_ticks()
                    self.player_hands[0].append(self.remain_cards.pop())
                    self.new_drawn_card = self.player_hands[0][-1]
                # 카드를 드로우 하고 턴을 넘기는 함수.
                elif self.new_drawn_card is not None and self.clicked_next_turn_button:
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.reset()
                    print("턴 종료")
                    self.turn_count = self.turn_count + 1
                    if self.turn_count % 5 == 0:
                        self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)
                # 카드를 드로우 하고, 드로우한 카드를 내는 함수.
                elif self.new_drawn_card is not None and self.pop_card is None:
                    # 유효성 검사 및 클릭카드가 new_drawn_card인지 확인
                    if self.new_drawn_card is not None and is_valid_move(self.new_drawn_card, self.top_card) and self.clicked_card == self.new_drawn_card and self.pop_card is None:
                        self.place_animation(self.current_player)
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
                        self.place_animation(self.current_player)
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
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.reset()
                            print("턴 종료")
                            self.turn_count = self.turn_count + 1
                            if self.turn_count % 5 == 0:
                                self.board_card = random_top_card_color(self.top_card, self.dummy_cards,
                                                                        self.board_card, self.dummy_cards_c)
                        # 내는 카드가 special이고, change일 경우
                        elif self.pop_card.is_special() and self.pop_card.value == "change":
                            self.change_card = True
                            if self.clicked_change_index is not None:
                                self.color_change = self.change_color_list[self.clicked_change_index]
                                self.current_player, self.game_direction = apply_special_card_effects(
                                    self.pop_card, self.current_player, self.game_direction,
                                    self.player_hands, self.remain_cards, self.player_count)
                                self.animation_method[self.pop_card.value](self.current_player)
                                self.board_card.append(self.color_change)
                                self.reset()
                                print("턴 종료")
                                self.turn_count = self.turn_count + 1
                                if self.turn_count % 5 == 0:
                                    self.board_card = random_top_card_color(self.top_card, self.dummy_cards,
                                                                            self.board_card, self.dummy_cards_c)
                        # 내는 카드가 special이 아닌 경우
                        elif not self.pop_card.is_special():
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.reset()
                            print("턴 종료")
                            self.turn_count = self.turn_count + 1
                            if self.turn_count % 5 == 0:
                                self.board_card = random_top_card_color(self.top_card, self.dummy_cards,
                                                                        self.board_card, self.dummy_cards_c)
                elif not self.uno_check:
                    # 내는 카드가 special이고 change가 아닐 때,
                    if self.pop_card.is_special() and self.pop_card.value != "change":
                        self.current_player, self.game_direction = apply_special_card_effects(self.pop_card,
                                                                                     self.current_player,
                                                                                     self.game_direction,
                                                                                     self.player_hands,
                                                                                     self.remain_cards,
                                                                                     self.player_count)
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.reset()
                        print("턴 종료")
                        self.turn_count = self.turn_count + 1
                        if self.turn_count % 5 == 0:
                            self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)
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
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.board_card.append(self.color_change)
                            self.reset()
                            print("턴 종료")
                            self.turn_count = self.turn_count + 1
                            if self.turn_count % 5 == 0:
                                self.board_card = random_top_card_color(self.top_card, self.dummy_cards,
                                                                        self.board_card, self.dummy_cards_c)
                    # 내는 카드가 special이 아닌 경우
                    else:
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        print("턴 종료")
                        self.turn_count = self.turn_count + 1
                        if self.turn_count % 5 == 0:
                            self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)

            # 우노 시간 넘기면 발동
            if self.pop_card is not None and self.one_flags[0]:
                if self.current_time - self.uno_current_time >= self.uno_delay_time:
                    self.draw_animation(self.current_player)
                    self.uno_drawn_card = self.remain_cards.pop()
                    self.player_hands[0].append(self.uno_drawn_card)
                    # 내는 카드가 special이고, change일 경우
                    if self.pop_card.is_special() and self.pop_card.value == "change":
                        self.one_flags[0] = False
                        self.uno_check = False
                        self.user_uno_clicked = False
                        self.change_uno_expire = True
                        print("턴 종료")
                        self.turn_count = self.turn_count + 1
                        if self.turn_count % 5 == 0:
                            self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)
                    # 내는 카드가 special이고, change가 아닐 경우
                    elif self.pop_card.is_special() and self.pop_card.value != "change":
                        self.current_player, self.game_direction = apply_special_card_effects(
                            self.pop_card, self.current_player, self.game_direction, self.player_hands,
                            self.remain_cards,
                            self.player_count)
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.reset()
                        print("턴 종료")
                        self.turn_count = self.turn_count + 1
                        if self.turn_count % 5 == 0:
                            self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)

                    # 내는 카드가 special이 아닌 경우
                    elif not self.pop_card.is_special():
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        print("턴 종료")
                        self.turn_count = self.turn_count + 1
                        if self.turn_count % 5 == 0:
                            self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)
            # 우노 마치고, change_card 제한시간 넘는 경우
            elif self.change_uno_expire:
                if self.user_turn and self.current_time - self.turn_start_time >= self.time_limit:
                    self.current_player, self.game_direction = apply_special_card_effects(
                        self.pop_card, self.current_player, self.game_direction, self.player_hands,
                        self.remain_cards,
                        self.player_count)
                    self.animation_method[self.pop_card.value](self.current_player)
                    self.reset()
                    print("턴 종료")
                    self.turn_count = self.turn_count + 1
                    if self.turn_count % 5 == 0:
                        self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)
            # 유저의 턴일 때 시간이 초과되면 드로우하고 턴을 넘김
            elif self.new_drawn_card is None:
                if self.user_turn and self.current_time - self.turn_start_time >= self.time_limit:
                    self.draw_animation(self.current_player)
                    self.new_drawn_card = self.remain_cards.pop()
                    self.player_hands[self.current_player].append(self.new_drawn_card)  # 카드를 드로우
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.reset()
                    print("턴 종료")
                    self.turn_count = self.turn_count + 1
                    if self.turn_count % 5 == 0:
                        self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)

            # 유저가 드로우를 하고 시간이 초과되면 턴을 그냥 넘김
            elif self.new_drawn_card is not None:
                if self.user_turn and self.current_time - self.user_draw_time >= self.time_limit:
                    self.current_player = (self.current_player + self.game_direction) % self.player_count
                    self.reset()
                    print("턴 종료")
                    self.turn_count = self.turn_count + 1
                    if self.turn_count % 5 == 0:
                        self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)

        # 컴퓨터 턴 처리
        if not self.user_turn:
            if self.current_time >= self.computer_action_time:  # 설정한 시간이 되면 컴퓨터가 행동함
                # 처음 유효성 검사
                if self.new_drawn_card is None and self.pop_card is None:
                    self.playable, self.pop_card_index = computer_playable_card(self.player_hands[self.current_player], self.board_card)
                # 카드를 낼 수 있을 때 낸다.
                if self.playable and self.new_drawn_card is None and self.pop_card is None:
                    self.place_animation(self.current_player)
                    self.pop_card = self.player_hands[self.current_player][self.pop_card_index]
                    self.board_card, self.player_hands[self.current_player] = com_submit_card\
                        (self.pop_card, self.pop_card_index, self.board_card, self.player_hands[self.current_player])
                    self.uno_check = check_uno(self.player_hands[self.current_player])
                    if self.uno_check:
                        self.one_flags, self.uno_current_time, self.uno_delay_time = is_uno(self.one_flags, self.current_player)
                # 카드를 낼 수 없을 때 드로우 한다.
                elif not self.playable and self.new_drawn_card is None and self.pop_card is None:
                    self.draw_animation(self.current_player)
                    self.new_drawn_card = self.remain_cards.pop()
                    self.player_hands[self.current_player].append(self.new_drawn_card)
                # 드로우한 카드가 낼 수 있는 경우
                elif self.new_drawn_card is not None and is_valid_move(self.new_drawn_card, self.top_card) and self.pop_card is None:
                    if self.current_time - self.turn_start_time >= self.delay_time2:
                        self.place_animation(self.current_player)
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
                        print("턴 종료")
                        self.turn_count = self.turn_count + 1
                        if self.turn_count % 5 == 0:
                            self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)
                # 컴퓨터가 우노이고, 유저가 우노를 클릭했을 경우
                elif self.uno_check:
                    if self.user_uno_clicked:
                        self.draw_animation(self.current_player)
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
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.reset()
                            print("턴 종료")
                            self.turn_count = self.turn_count + 1
                            if self.turn_count % 5 == 0:
                                self.board_card = random_top_card_color(self.top_card, self.dummy_cards,
                                                                        self.board_card, self.dummy_cards_c)
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
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.reset()
                            print("턴 종료")
                            self.turn_count = self.turn_count + 1
                            if self.turn_count % 5 == 0:
                                self.board_card = random_top_card_color(self.top_card, self.dummy_cards,
                                                                        self.board_card, self.dummy_cards_c)
                        # 컴퓨터가 낸 카드가 special이 아닌 경우
                        elif not self.pop_card.is_special():
                            self.current_player = (self.current_player + self.game_direction) % self.player_count
                            self.reset()
                            print("턴 종료")
                            self.turn_count = self.turn_count + 1
                            if self.turn_count % 5 == 0:
                                self.board_card = random_top_card_color(self.top_card, self.dummy_cards,
                                                                        self.board_card, self.dummy_cards_c)
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
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.reset()
                        print("턴 종료")
                        self.turn_count = self.turn_count + 1
                        if self.turn_count % 5 == 0:
                            self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)
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
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.board_card.append(self.color_change)
                            self.reset()
                            print("턴 종료")
                            self.turn_count = self.turn_count + 1
                            if self.turn_count % 5 == 0:
                                self.board_card = random_top_card_color(self.top_card, self.dummy_cards,
                                                                        self.board_card, self.dummy_cards_c)
                    # 내는 카드가 special이 아닌 경우
                    elif not self.pop_card.is_special():
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        print("턴 종료")
                        self.turn_count = self.turn_count + 1
                        if self.turn_count % 5 == 0:
                            self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)

            # 컴퓨터의 턴일 때 시간이 초과되면 우노를 넘긴다.
            if any(self.one_flags[1:]) and not self.user_turn:
                if self.current_time - self.uno_current_time >= self.uno_delay_time:
                    # 내는 카드가 special이고, change가 아닐 경우
                    if self.pop_card.is_special() and self.pop_card.value != "change":
                        self.current_player, self.game_direction = apply_special_card_effects(
                            self.pop_card, self.current_player, self.game_direction, self.player_hands,
                            self.remain_cards,
                            self.player_count)
                        self.animation_method[self.pop_card.value](self.current_player)
                        self.reset()
                        print("턴 종료")
                        self.turn_count = self.turn_count + 1
                        if self.turn_count % 5 == 0:
                            self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)

                    # 내는 카드가 special이고 change인 경우
                    elif self.pop_card.is_special() and self.pop_card.value == "change":
                        self.change_index = random.randint(0, 3)
                        self.color_change = self.change_color_list[self.change_index]
                        if self.current_time - self.turn_start_time >= self.delay_time3:
                            self.current_player, self.game_direction = apply_special_card_effects(
                                self.pop_card, self.current_player, self.game_direction, self.player_hands,
                                self.remain_cards,
                                self.player_count)
                            self.animation_method[self.pop_card.value](self.current_player)
                            self.board_card.append(self.color_change)
                            self.reset()
                            print("턴 종료")
                            self.turn_count = self.turn_count + 1
                            if self.turn_count % 5 == 0:
                                self.board_card = random_top_card_color(self.top_card, self.dummy_cards,
                                                                        self.board_card, self.dummy_cards_c)
                    # 내는 카드가 special이 아닌 경우
                    elif not self.pop_card.is_special():
                        self.current_player = (self.current_player + self.game_direction) % self.player_count
                        self.reset()
                        print("턴 종료")
                        self.turn_count = self.turn_count + 1
                        if self.turn_count%5 == 0:
                            self.board_card = random_top_card_color(self.top_card, self.dummy_cards, self.board_card, self.dummy_cards_c)


class StageD(SingleGame):
    def __init__(self):
        super().__init__([False, True, True, True, True], 'You')
        self.cards = generate_d_stage_cards(self.color_weakness, self.size_change)

    def win(self):
        popup = None
        if len(self.player_hands[0]) == 0 or any(len(player_hand) >= 5 for player_hand in self.player_hands[1:]):
            popup = basic.scale_by(pygame.image.load("./resources/Image/win.png"), self.size_change)
            self.game_over = True
        elif any(len(player_hand) == 0 for player_hand in self.player_hands[1:]) or len(self.player_hands[0]) == 5:
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