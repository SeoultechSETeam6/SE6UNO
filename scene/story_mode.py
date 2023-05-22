import pygame
import random

from controller import game_view, game_data
from scene.single_play import SinglePlay
from ui.popup import Popup


# 콤보 사용, 기술 카드를 낼 수 있으면 기술카드를 먼저 냄
class StageA(SinglePlay):
    def __init__(self):
        super().__init__([False, False, True, False, False], 'You', ['A'], True)


# 모든 카드를 플레이어들에게 나눠줌. 50퍼센트 확률로 컴퓨터가 색 선호도에 따라 카드 선택함
class StageB(SinglePlay):
    def __init__(self):
        super().__init__([True, False, True, False, True], 'You', ['B', 'B', 'B'], True)


# 5턴 마다 낼 수 있는 카드의 색상이 무작위로 변경됨, 30퍼센트 확률로 카드를 낼 수 있어도 카드를 뽑고 턴을 넘김.
class StageC(SinglePlay):
    def __init__(self):
        super().__init__([True, False, True, False, False], 'You', ['C', 'C'], True)
        self.turn_count = 1


# 공격 카드, 폭탄 카드가 다수 추가됨. 공격, 폭탄카드 사용 가능시 먼저 사용
class StageD(SinglePlay):
    def __init__(self):
        super().__init__([True, False, True, False, True], 'You', ['D', 'D', 'D'], True)

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
