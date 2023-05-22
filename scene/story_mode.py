import pygame
import random

from controller import game_view, game_data
from controller.card_gen import (
    generate_cards,
    generate_a_stage_cards,
    generate_c_stage_cards,
    generate_c_for_change_cards,
    generate_d_stage_cards
)
from controller.card_shuffle import shuffle_cards, distribute_cards, stage_a_distribute
from controller.game_utils import (
    draw_text,
    apply_special_card_effects,
    random_top_card_color
)
from scene.single_play import SinglePlay
from ui.popup import Popup


# 콤보 사용, 기술 카드를 낼 수 있으면 기술카드를 먼저 냄
class StageA(SinglePlay):
    def __init__(self):
        super().__init__([False, False, True, False, False], 'You', ['A'], True)
        self.regular_cards, self.special_cards = generate_a_stage_cards(self.settings_data["color_weakness"],
                                                                        self.ui_size["change"])
        self.player_hands, self.remain_cards = stage_a_distribute(self.player_count, self.regular_cards,
                                                                  self.special_cards, self.card_count)
        self.stage = "A"
        self.draw_override = True
        self.combo_text = f"combo: {self.combo}"

    def turn_and_reset(self):
        if self.new_drawn_card is not None:
            if self.pop_card is None:
                pass
            elif self.pop_card.is_special() is False:
                self.current_player = (self.current_player + self.game_direction) % self.player_count
            self.turn_end_method()
            self.combo = 0
        elif self.new_drawn_card is None:
            self.reset()
            self.combo = self.combo + 1
            print(self.combo)

    def draw_and_reset_combo(self):
        if self.new_drawn_card is not None:
            self.combo = 0

    def card_playing(self):
        self.draw_and_reset_combo()
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

    def draw_combo(self):
        self.combo_text = f"combo: {self.combo}"
        draw_text(self.screen, self.combo_text, self.font, (255, 255, 255), self.center_x, self.center_y + 100)

    def draw(self):
        super().draw()
        if self.combo > 0:
            self.draw_combo()
        pygame.display.flip()


# 모든 카드를 플레이어들에게 나눠줌. 50퍼센트 확률로 컴퓨터가 색 선호도에 따라 카드 선택함
class StageB(SinglePlay):
    def __init__(self):
        super().__init__([True, False, True, False, True], 'You', ['B', 'B', 'B'], True)
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


# 5턴 마다 낼 수 있는 카드의 색상이 무작위로 변경됨, 30퍼센트 확률로 카드를 낼 수 있어도 카드를 뽑고 턴을 넘김.
class StageC(SinglePlay):
    def __init__(self):
        super().__init__([True, False, True, False, False], 'You', ['C', 'C'], True)
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


# 공격 카드, 폭탄 카드가 다수 추가됨. 공격, 폭탄카드 사용 가능시 먼저 사용
class StageD(SinglePlay):
    def __init__(self):
        super().__init__([True, False, True, False, True], 'You', ['D', 'D', 'D'], True)
        self.turn_count = 1
        self.cards = generate_d_stage_cards(self.settings_data["color_weakness"], self.ui_size["change"])

        self.stage = "D"
    def win(self):
        popup = None
        if len(self.player_hands[0]) == 0:
            popup = game_view.scale_by(pygame.image.load("./resources/Image/win.png"), self.ui_size["change"])
            self.game_over = True
            self.win_flag = True
            if not self.achievement_data[1]["achieved"]:
                self.popup_achieved = Popup(self.screen.get_width() * 0.5,
                                            self.screen.get_height() * 0.7,
                                            self.screen.get_width() // 3,
                                            self.screen.get_height() // 6,
                                            self.screen,
                                            "업적 달성: " + game_data.ACHIEVEMENTS[1]["name"],
                                            self.ui_size["font"][1])
                self.popup_achievement_image = game_view.scale_by(
                    pygame.image.load(self.popup_achievement_image_path +
                                      game_data.ACHIEVEMENTS[1]["image"]).convert_alpha(),
                    self.ui_size["change"] * 0.6)
                game_data.save_achieved_status(1)
                self.popup_achieved.pop = True
        elif any(len(player_hand) == 0 for player_hand in self.player_hands[1:]):
            popup = game_view.scale_by(pygame.image.load("./resources/Image/lose.png"), self.ui_size["change"])
            self.game_over = True
        if self.game_over:
            self.background_music.stop()
            self.sound_shuffle.stop()
            self.screen.fill((0, 0, 0))
            self.screen.blit(popup, (self.screen.get_width() // 2 - popup.get_size()[0] // 2,
                                     self.screen.get_height() // 2 - popup.get_size()[1] // 2))
            if self.popup_achieved.pop:
                self.popup_achieved.open()
                self.screen.blit(self.popup_achievement_image,
                                 (self.screen.get_width() * 0.34, self.screen.get_height() * 0.64))

            pygame.display.flip()
            popup_running = True
            while popup_running:
                for popup_event in pygame.event.get():
                    if popup_event.type == pygame.KEYDOWN:
                        game_data.increment_stage_clear_count(3)
                        self.running = False
                        popup_running = False
                    if popup_event.type == pygame.MOUSEBUTTONDOWN:
                        game_data.increment_stage_clear_count(3)
                        self.running = False
                        popup_running = False