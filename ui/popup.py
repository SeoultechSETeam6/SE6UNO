import pygame

from controller import game_view
from ui.button import Button

# 색상 설정
white = (255, 255, 255)
gray = (200, 200, 200)
black = (0, 0, 0)


class Popup:
    """
    캔버스 위에 확인, 닫기 버튼을 포함한 검정색 팝업을 띄우는 클래스입니다.\n
    **x, y**: 팝업이 위치할 x, y 좌표 (버튼의 중앙 기준)\n
    **width, height**: 팝업의 가로, 세로\n
    **screen**: 팝업이 그려질 캔버스\n
    **text**: 팝업의 대화 상자에 표시할 글\n
    **text_size**: 글자의 크기\n
    **on_click_funtion**: 확인 버튼 클릭 시 일어날 이벤트 메서드
    """
    def __init__(self, x, y, width, height, screen, text='Sample', text_size=25, on_click_function=None):
        self.x = x - width // 2
        self.y = y - height // 2
        self.width = width
        self.height = height
        self.screen = screen
        self.text = text
        self.text_size = text_size
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((self.width, self.height))
        self.on_click_function = on_click_function

        self.button_accept = Button(x,
                                    y * 1.25,
                                    self.width // 4,
                                    self.height // 6,
                                    self.screen,
                                    0xffffff,
                                    '확인',
                                    self.text_size,
                                    on_click_function=self.on_click_function)
        self.button_close = Button(x + self.width // 2.5,
                                   y - self.height // 3,
                                   self.width // 8,
                                   self.height // 7,
                                   self.screen,
                                   0xffffff,
                                   'X',
                                   self.text_size,
                                   on_click_function=self.close)

        self.pop = False

        self.font = pygame.font.Font(game_view.FONT_PATH, text_size).render(text, True, 0x000000)
        self.surface.fill(gray)

    def open(self):
        self.screen.blit(self.surface, self.rect)
        self.screen.blit(self.font, [
            (self.x + self.width // 2) - self.font.get_rect().width / 2,
            (self.y + self.height // 2.2) - self.font.get_rect().height / 2])
        self.screen.blit(self.button_close.surface, self.button_close.rect)
        if self.on_click_function is not None:
            self.screen.blit(self.button_accept.surface, self.button_accept.rect)
            self.button_accept.draw()
            self.button_accept.detect_event()
        self.button_close.draw()
        self.button_close.detect_event()

    def close(self):
        print('닫기 버튼 클릭됨')
        self.pop = False

