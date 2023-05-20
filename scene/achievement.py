import pygame

from controller.mouse import Mouse
from controller import game_data, game_view
from ui.button import Button


class Achievement:
    def __init__(self):
        # 게임 설정 불러오기
        self.settings_data = game_data.load_settings()

        # 로고 가로 변수
        self.achievement_image_width = None

        # pygame 초기화
        pygame.init()
        pygame.display.set_caption(game_view.GAME_TITLE + ": Achievement")
        self.ui_size = game_view.set_size(self.settings_data["resolution"]["width"])
        self.screen = pygame.display.set_mode((self.settings_data["resolution"]["width"],
                                               self.settings_data["resolution"]["height"]))
        self.clock = pygame.time.Clock()
        self.running = True

        # 글꼴 설정
        self.font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][0])
        self.small_font = pygame.font.Font(game_view.FONT_PATH, self.ui_size["font"][1])

        # 나가기 버튼
        self.button_quit = Button(self.screen.get_width() * 0.07,
                                  self.screen.get_height() * 0.06,
                                  self.ui_size["button"][0],
                                  self.ui_size["button"][1],
                                  self.screen,
                                  0xffffff,
                                  "나가기",
                                  self.ui_size["font"][1],
                                  on_click_function=self.event_quit)

        # 공통 이미지 경로
        self.image_path = "./resources/Image/achievements/"

        # 업적 그림, 이름과 설명
        self.achievements = []
        for achievement in game_data.ACHIEVEMENTS:
            achievement_obj = {}
            achievement_obj.update(
                {"image": game_view.scale_by(
                    pygame.image.load(self.image_path + achievement["image"]).convert_alpha(),
                    self.ui_size["change"]),
                    "name": self.font.render(achievement["name"], True, (255, 255, 255)),
                    "description": self.small_font.render(achievement["description"], True, (255, 255, 255))})
            self.achievements.append(achievement_obj)

        # 업적 달성 날짜
        self.achieved_data = game_data.load_achieved_status()
        self.texts_achieved_date = []
        for i, achievement in enumerate(self.achievements):
            achievement.update({"date": self.small_font.render("달성 일시: " + str(self.achieved_data[i]["achieved_date"]), True, (255, 255, 255))})

        # 상단 글자 이미지
        self.image_achievement_title = game_view.scale_by(
            pygame.image.load(self.image_path + "achievement.png").convert_alpha(),
            self.ui_size["change"])

        # 클리어 이미지
        self.image_clear_mark = game_view.scale_by(
            pygame.image.load(self.image_path + "clear.png").convert_alpha(),
            self.ui_size["change"])

    def event_quit(self):
        print('나가기')
        self.running = False

    def draw(self):
        self.screen.fill((20, 20, 20))

        # 업적 로고 표시
        self.screen.blit(self.image_achievement_title,
                         (self.screen.get_width() / 2 - self.image_achievement_title.get_width() / 2, 0))

        # 업적 표시
        x = self.screen.get_width() * 0.05
        y = self.screen.get_height() * 0.2
        for i, achievement in enumerate(self.achievements):
            self.screen.blit(achievement["image"], (x, y))
            self.screen.blit(achievement["name"], (x, y + self.screen.get_height() * 0.25))
            self.screen.blit(achievement["description"], (x, y + self.screen.get_height() * 0.32))
            if self.achieved_data[i]["achieved"]:
                self.screen.blit(self.image_clear_mark, (x, y + self.screen.get_height() * 0.05))
                self.screen.blit(achievement["date"], (x, y + self.screen.get_height() * 0.35))
            x += self.screen.get_width() // 4
            if x > self.screen.get_width():
                x = self.screen.get_width() * 0.05
                y += self.screen.get_height() // 2.5

        # 나가기 버튼
        self.button_quit.draw()
        self.button_quit.detect_event()

        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == self.settings_data["key"]['enter'] or pygame.K_ESCAPE:
                    self.button_quit.on_click_function()

    def run(self):
        while self.running:
            self.event()
            Mouse.updateMouseState()
            self.clock.tick(game_view.FPS)
            self.draw()
