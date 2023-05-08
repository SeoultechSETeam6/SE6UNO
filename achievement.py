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
        self.achievement_image = None
        self.single_player_winner_image = None
        self.stage_all_clear_image = None
        self.speed_racer_image = None
        self.chivalry_image = None
        self.win_by_a_nose_image = None
        self.terrorist_image = None
        self.adequate_defense_image = None
        self.greedy_man_image = None

        self.single_player_winner_clear = None
        self.stage_all_clear_clear = None
        self.speed_racer_clear = None
        self.chivalry_clear = None
        self.win_by_a_nose_clear = None
        self.terrorist_clear = None
        self.adequate_defense_clear = None
        self.greedy_man_clear = None

        # 로고 가로 변수
        self.achievement_image_width = None

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
            self.single_player_winner_coordinate = (0, 100)
            self.stage_all_clear_coordinate = (300, 100)
            self.speed_racer_coordinate = (800, 100)
            self.chivalry_coordinate = (1200, 100)
            self.win_by_a_nose_coordinate = (1500, 100)
            self.terrorist_coordinate = (0, 450)
            self.adequate_defense_coordinate = (400, 450)
            self.greedy_man_coordinate = (800, 450)
            self.exit_button_coordinate = (1700, 900)
        elif self.display_size[0] == 1600:
            self.achievement_folder = "./resources/Image/achievements/middle"
            self.single_player_winner_coordinate = (0, 100)
            self.stage_all_clear_coordinate = (300, 100)
            self.speed_racer_coordinate = (600, 100)
            self.chivalry_coordinate = (1000, 100)
            self.win_by_a_nose_coordinate = (0, 450)
            self.terrorist_coordinate = (400, 450)
            self.adequate_defense_coordinate = (800, 450)
            self.greedy_man_coordinate = (1200, 450)
            self.exit_button_coordinate = (1300, 800)
        else:
            self.achievement_folder = "./resources/Image/achievements/small"
            self.single_player_winner_coordinate = (0, 100)
            self.stage_all_clear_coordinate = (300, 100)
            self.speed_racer_coordinate = (600, 100)
            self.chivalry_coordinate = (900, 100)
            self.win_by_a_nose_coordinate = (0, 350)
            self.terrorist_coordinate = (300, 350)
            self.adequate_defense_coordinate = (600, 350)
            self.greedy_man_coordinate = (900, 350)
            self.exit_button_coordinate = (1100, 700)

        # 나가기 버튼
        self.exit_button = Button(self.exit_button_coordinate[0], self.exit_button_coordinate[1], self.button_size[0],
                                  self.button_size[1], "나가기", self.exit_event, self.font_size[1])

    def exit_event(self):
        print('나가기')
        self.running = False

    def load_achievement_logo(self):
        self.achievement_image = pygame.image.load(
            f"{self.achievement_folder}/achievement.png").convert_alpha()
        self.achievement_image_width = self.achievement_image.get_width()

    # 업적 달성 여부 체크후, 이미지 로드
    def load_single_player_winner_image(self):
        self.single_player_winner_image = pygame.image.load(
            f"{self.achievement_folder}/single_player_winner.png").convert_alpha()
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['single_player_winner']['achieved']:
            self.single_player_winner_clear = pygame.image.load(
                f"{self.achievement_folder}/clear.png").convert_alpha()
        self.single_player_winner_image_height = self.single_player_winner_image.get_height()

    def load_stage_all_clear_image(self):
        self.stage_all_clear_image = pygame.image.load(
            f"{self.achievement_folder}/stage_all_clear.png").convert_alpha()
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['stage_all_clear']['achieved']:
            self.stage_all_clear_clear = pygame.image.load(
                f"{self.achievement_folder}/clear.png").convert_alpha()
        self.stage_all_clear_image_height = self.stage_all_clear_image.get_height()

    def load_speed_racer_image(self):
        self.speed_racer_image = pygame.image.load(
            f"{self.achievement_folder}/speed_racer.png").convert_alpha()
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['speed_racer']['achieved']:
            self.speed_racer_clear = pygame.image.load(
                f"{self.achievement_folder}/clear.png").convert_alpha()
        self.speed_racer_image_height = self.speed_racer_image.get_height()

    def load_chivalry_image(self):
        self.chivalry_image = pygame.image.load(
            f"{self.achievement_folder}/chivalry.png").convert_alpha()
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['chivalry']['achieved']:
            self.chivalry_clear = pygame.image.load(
                f"{self.achievement_folder}/clear.png").convert_alpha()
        self.chivalry_image_height = self.chivalry_image.get_height()

    def load_win_by_a_nose_image(self):
        self.win_by_a_nose_image = pygame.image.load(
            f"{self.achievement_folder}/win_by_a_nose.png").convert_alpha()
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['win_by_a_nose']['achieved']:
            self.win_by_a_nose_clear = pygame.image.load(
                f"{self.achievement_folder}/clear.png").convert_alpha()
        self.win_by_a_nose_image_height = self.win_by_a_nose_image.get_height()

    def load_terrorist_image(self):
        self.terrorist_image = pygame.image.load(
            f"{self.achievement_folder}/terrorist.png").convert_alpha()
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['terrorist']['achieved']:
            self.terrorist_clear = pygame.image.load(
                f"{self.achievement_folder}/clear.png").convert_alpha()
        self.terrorist_image_height = self.terrorist_image.get_height()

    def load_adequate_defense_image(self):
        self.adequate_defense_image = pygame.image.load(
            f"{self.achievement_folder}/adequate_defense.png").convert_alpha()
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['adequate_defense']['achieved']:
            self.adequate_defense_clear = pygame.image.load(
                f"{self.achievement_folder}/clear.png").convert_alpha()
        self.adequate_defense_image_height = self.adequate_defense_image.get_height()

    def load_greedy_man_image(self):
        self.greedy_man_image = pygame.image.load(
            f"{self.achievement_folder}/greedy_man.png").convert_alpha()
        with open('game_data.json', 'r', encoding='utf-8') as file:
            game_data = json.load(file)
        if game_data['achievements']['greedy_man']['achieved']:
            self.greedy_man_clear = pygame.image.load(
                f"{self.achievement_folder}/clear.png").convert_alpha()
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

    def draw(self):
        self.screen.fill((20, 20, 20))

        # 업적 로고 표시
        self.screen.blit(self.achievement_image, (((self.display_size[0]/2) - (self.achievement_image_width/2)), 0))


        # 업적 표시
        self.screen.blit(self.single_player_winner_image, self.single_player_winner_coordinate)
        self.screen.blit(self.stage_all_clear_image, self.stage_all_clear_coordinate)
        self.screen.blit(self.speed_racer_image, self.speed_racer_coordinate)
        self.screen.blit(self.chivalry_image, self.chivalry_coordinate)
        self.screen.blit(self.win_by_a_nose_image, self.win_by_a_nose_coordinate)
        self.screen.blit(self.terrorist_image, self.terrorist_coordinate)
        self.screen.blit(self.adequate_defense_image, self.adequate_defense_coordinate)
        self.screen.blit(self.greedy_man_image, self.greedy_man_coordinate)

        # 클리어 이미지 표시
        if self.single_player_winner_clear is not None:
            self.screen.blit(self.single_player_winner_clear, self.single_player_winner_coordinate)
        if self.stage_all_clear_clear is not None:
            self.screen.blit(self.stage_all_clear_clear, self.stage_all_clear_coordinate)
        if self.speed_racer_clear is not None:
            self.screen.blit(self.speed_racer_clear, self.speed_racer_coordinate)
        if self.chivalry_clear is not None:
            self.screen.blit(self.chivalry_clear, self.chivalry_coordinate)
        if self.win_by_a_nose_clear is not None:
            self.screen.blit(self.win_by_a_nose_clear, self.win_by_a_nose_clear)
        if self.terrorist_clear is not None:
            self.screen.blit(self.terrorist_clear, self.terrorist_coordinate)
        if self.adequate_defense_clear is not None:
            self.screen.blit(self.adequate_defense_clear, self.adequate_defense_coordinate)
        if self.greedy_man_clear is not None:
            self.screen.blit(self.greedy_man_clear, self.greedy_man_coordinate)

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
        self.draw_achievement_info(achievements['greedy_man'], self.greedy_man_coordinate[0],
                                   self.greedy_man_coordinate[1] + self.greedy_man_image_height)

        # 나가기 버튼
        self.exit_button.process()
        self.screen.blit(self.exit_button.surface, self.exit_button.rect)
        
        # 버튼 체크박스
        self.screen.blit(self.exit_button.selected_image, (self.exit_button.rect.x,
                                                           self.exit_button.rect.y - self.font_size[1]))

        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == self.key_setting['enter']:
                    self.exit_button.on_click_function()
                elif event.key == pygame.K_ESCAPE:
                    self.exit_button.on_click_function()

    def run(self):
        while self.running:
            self.event()
            Mouse.updateMouseState()
            self.clock.tick(basic.fps)
            self.load_achievement_logo()
            self.load_single_player_winner_image()
            self.load_stage_all_clear_image()
            self.load_speed_racer_image()
            self.load_chivalry_image()
            self.load_win_by_a_nose_image()
            self.load_terrorist_image()
            self.load_adequate_defense_image()
            self.load_greedy_man_image()
            self.draw()
