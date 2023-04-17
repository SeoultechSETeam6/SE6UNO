import pygame
from button import Button

pygame.init()

# 창 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 색상 설정
white = (255, 255, 255)
gray = (200, 200, 200)
black = (0, 0, 0)


class Popup:
    def __init__(self, x, y, width=400, height=200, text='Sample', on_click_function=None, font_size=25, pop=False):
        self.x = x - width // 2
        self.y = y - height // 2
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((self.width, self.height))

        self.accept_button = Button(x,
                                    y * 1.25,
                                    self.width // 4,
                                    self.height // 6, '확인', on_click_function,
                                    self.font_size)
        self.close_button = Button(x * 1.3,
                                   y * 0.72,
                                   self.width // 10,
                                   self.height // 9, 'X', self.close,
                                   self.font_size)

        self.pop = pop
        self.on_click_function = self.close

        self.font = pygame.font.Font("./resources/maplestory_font.ttf", font_size)
        self.font = self.font.render(text, True, (255, 255, 255))
        self.surface.fill(black)

    def open(self):
        self.accept_button.process()
        self.close_button.process()

    def close(self):
        print('닫기 버튼 클릭됨')
        self.pop = False

