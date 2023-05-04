import pygame
import pickle
import json

from mouse import Mouse, MouseState
from option import basic_option as basic
from button import Button


class Achievement:
    def __init__(self):
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

        # 이미지 변수 초기화
        self.single_player_winner_image = None
        self.stage_all_clear_image = None
        self.speed_racer_image = None
        self.chivalry_image = None
        self.win_by_a_nose_image = None
        self.terrorist_image = None
        self.adequate_defense_image = None
        self.greedy_man_image = None

        # 이미지 높이 변수 초기화
        self.single_player_winner_image_height = None
        self.stage_all_clear_image_height = None
        self.speed_racer_image_height = None
        self.chivalry_image_height = None
        self.win_by_a_nose_image_height = None
        self.terrorist_image_height = None
        self.adequate_defense_image_height = None
        self.greedy_man_image_height = None

        pygame.init()
        self.screen = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption(basic.game_title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font("./resources/maplestory_font.ttf", self.font_size[0])
        self.small_font = pygame.font.Font("./resources/maplestory_font.ttf", self.font_size[1])

        # 화면 크기에 맞춰 이미지 경로 수정 및 좌표수정
        if self.display_size[0] == 1920:
            self.achievement_folder = "./resources/Image/achievements/big"
            self.single_player_winner_coordinate = (0, 0)
            self.stage_all_clear_coordinate = (300, 0)
            self.speed_racer_coordinate = (600, 0)
            self.chivalry_coordinate = (900, 0)
            self.win_by_a_nose_coordinate = (1200, 0)
            self.terrorist_coordinate = (1500, 0)
            self.adequate_defense_coordinate = (0, 350)
            self.check_greedy_man_coordinate = (300, 350)
            self.exit_button_coordinate = (1700, 900)
        elif self.display_size[0] == 1600:
            self.achievement_folder = "./resources/Image/achievements/middle"
            self.single_player_winner_coordinate = (0, 0)
            self.stage_all_clear_coordinate = (300, 0)
            self.speed_racer_coordinate = (600, 0)
            self.chivalry_coordinate = (900, 0)
            self.win_by_a_nose_coordinate = (1200, 0)
            self.terrorist_coordinate = (0, 350)
            self.adequate_defense_coordinate = (300, 350)
            self.check_greedy_man_coordinate = (600, 350)
            self.exit_button_coordinate = (1300, 800)
        else:
            self.achievement_folder = "./resources/Image/achievements/small"
            self.single_player_winner_coordinate = (0, 0)
            self.stage_all_clear_coordinate = (300, 0)
            self.speed_racer_coordinate = (600, 0)
            self.chivalry_coordinate = (900, 0)
            self.win_by_a_nose_coordinate = (0, 350)
            self.terrorist_coordinate = (300, 350)
            self.adequate_defense_coordinate = (600, 350)
            self.check_greedy_man_coordinate = (900, 350)
            self.exit_button_coordinate = (1100, 700)

        # 나가기 버튼
        self.exit_button = Button(self.exit_button_coordinate[0], self.exit_button_coordinate[1], self.button_size[0],
                                  self.button_size[1], "나가기", self.check_exit_button, self.font_size[1])

    def exit_event(self):
        print('나가기')
        self.running = False

    # 업적 달성 여부 체크후, 이미지 로드
    def load_single_player_winner_image(self):
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['single_player_winner']['achieved']:
            self.single_player_winner_image = pygame.image.load(
                f"{self.achievement_folder}/single_player_winner_unlocked.png").convert_alpha()
        else:
            self.single_player_winner_image = pygame.image.load(
                f"{self.achievement_folder}/single_player_winner_locked.png").convert_alpha()
        self.single_player_winner_image_height = self.single_player_winner_image.get_height()

    def load_stage_all_clear_image(self):
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['stage_all_clear']['achieved']:
            self.stage_all_clear_image = pygame.image.load(
                f"{self.achievement_folder}/stage_all_clear_unlocked.png").convert_alpha()
        else:
            self.stage_all_clear_image = pygame.image.load(
                f"{self.achievement_folder}/stage_all_clear_locked.png").convert_alpha()
        self.stage_all_clear_image_height = self.stage_all_clear_image.get_height()

    def load_speed_racer_image(self):
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['speed_racer']['achieved']:
            self.speed_racer_image = pygame.image.load(
                f"{self.achievement_folder}/speed_racer_unlocked.png").convert_alpha()
        else:
            self.speed_racer_image = pygame.image.load(
                f"{self.achievement_folder}/speed_racer_locked.png").convert_alpha()
        self.speed_racer_image_height = self.speed_racer_image.get_height()

    def load_chivalry_image(self):
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['chivalry']['achieved']:
            self.chivalry_image = pygame.image.load(
                f"{self.achievement_folder}/chivalry_unlocked.png").convert_alpha()
        else:
            self.chivalry_image = pygame.image.load(
                f"{self.achievement_folder}/chivalry_locked.png").convert_alpha()
        self.chivalry_image_height = self.chivalry_image.get_height()

    def load_win_by_a_nose_image(self):
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['win_by_a_nose']['achieved']:
            self.win_by_a_nose_image = pygame.image.load(
                f"{self.achievement_folder}/win_by_a_nose_unlocked.png").convert_alpha()
        else:
            self.win_by_a_nose_image = pygame.image.load(
                f"{self.achievement_folder}/win_by_a_nose_locked.png").convert_alpha()
        self.win_by_a_nose_image_height = self.win_by_a_nose_image.get_height()

    def load_terrorist_image(self):
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['terrorist']['achieved']:
            self.terrorist_image = pygame.image.load(
                f"{self.achievement_folder}/terrorist_unlocked.png").convert_alpha()
        else:
            self.terrorist_image = pygame.image.load(
                f"{self.achievement_folder}/terrorist_locked.png").convert_alpha()
        self.terrorist_image_height = self.terrorist_image.get_height()

    def load_adequate_defense_image(self):
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['adequate_defense']['achieved']:
            self.adequate_defense_image = pygame.image.load(
                f"{self.achievement_folder}/adequate_defense_unlocked.png").convert_alpha()
        else:
            self.adequate_defense_image = pygame.image.load(
                f"{self.achievement_folder}/adequate_defense_locked.png").convert_alpha()
        self.adequate_defense_image_height = self.adequate_defense_image.get_height()

    def load_greedy_man_image(self):
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['greedy_man']['achieved']:
            self.greedy_man_image = pygame.image.load(
                f"{self.achievement_folder}/greedy_man_unlocked.png").convert_alpha()
        else:
            self.greedy_man_image = pygame.image.load(
                f"{self.achievement_folder}/greedy_man_locked.png").convert_alpha()
        self.greedy_man_image_height = self.greedy_man_image.get_height()

    # 업적 정보
    def draw_achievement_info(self, achievement_data, x, y):
        name = achievement_data["name"]
        description = achievement_data["description"]
        achieved_date = achievement_data["achieved_date"]

        name_text = self.font.render(name, True, (255, 255, 255))
        description_text = self.small_font.render(description, True, (255, 255, 255))

        if achieved_date:
            achieved_date_text = self.small_font.render(achieved_date, True, (255, 255, 255))
            self.screen.blit(achieved_date_text, (x, y + self.font_size[0] * 2))
        self.screen.blit(name_text, (x, y))
        self.screen.blit(description_text, (x, y + self.font_size[0]))

    def check_exit_button(self):
        mouse_x, mouse_y = Mouse.getMousePos()
        mouse_state = Mouse.getMouseState()

        if self.exit_button.rect.collidepoint(mouse_x, mouse_y):
            if mouse_state == MouseState.CLICK:
                self.exit_event()

    def draw(self):
        self.screen.fill((20, 20, 20))

        # 업적 로고 표시
        self.screen.blit(self.single_player_winner_image, self.single_player_winner_coordinate)
        self.screen.blit(self.stage_all_clear_image, self.stage_all_clear_coordinate)
        self.screen.blit(self.speed_racer_image, self.speed_racer_coordinate)
        self.screen.blit(self.chivalry_image, self.chivalry_coordinate)
        self.screen.blit(self.win_by_a_nose_image, self.win_by_a_nose_coordinate)
        self.screen.blit(self.terrorist_image, self.terrorist_coordinate)
        self.screen.blit(self.adequate_defense_image, self.adequate_defense_coordinate)
        self.screen.blit(self.greedy_man_image, self.check_greedy_man_coordinate)

        # 업적 정보 표시
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        achievements = game_data['achievements']
        self.draw_achievement_info(achievements['single_player_winner'], self.single_player_winner_coordinate[0],
                                   self.single_player_winner_coordinate[1] + self.single_player_winner_image_height)
        self.draw_achievement_info(achievements['stage_all_clear'], self.stage_all_clear_coordinate[0],
                                   self.stage_all_clear_coordinate[1] + self.stage_all_clear_image_height)
        self.draw_achievement_info(achievements['speed_racer'], self.speed_racer_coordinate[0],
                                   self.speed_racer_coordinate[1] + self.speed_racer_image_height)
        self.draw_achievement_info(achievements['chivalry'], self.chivalry_coordinate[0],
                                   self.chivalry_coordinate[1] + self.chivalry_image_height)
        self.draw_achievement_info(achievements['win_by_a_nose'], self.win_by_a_nose_coordinate[0],
                                   self.win_by_a_nose_coordinate[1] + self.win_by_a_nose_image_height)
        self.draw_achievement_info(achievements['terrorist'], self.terrorist_coordinate[0],
                                   self.terrorist_coordinate[1] + self.terrorist_image_height)
        self.draw_achievement_info(achievements['adequate_defense'], self.adequate_defense_coordinate[0],
                                   self.adequate_defense_coordinate[1] + self.adequate_defense_image_height)
        self.draw_achievement_info(achievements['greedy_man'], self.check_greedy_man_coordinate[0],
                                   self.check_greedy_man_coordinate[1] + self.greedy_man_image_height)

        # 나가기 버튼
        self.exit_button.process()
        self.screen.blit(self.exit_button.surface, self.exit_button.rect)
        self.screen.blit(self.exit_button.selected_image,
                         (self.exit_button.rect.x, self.exit_button.rect.y - self.font_size[1]))

        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            Mouse.updateMouseState()
            self.clock.tick(basic.fps)
            self.load_single_player_winner_image()
            self.load_stage_all_clear_image()
            self.load_speed_racer_image()
            self.load_chivalry_image()
            self.load_win_by_a_nose_image()
            self.load_terrorist_image()
            self.load_adequate_defense_image()
            self.load_greedy_man_image()
            self.draw()
            self.check_exit_button()
