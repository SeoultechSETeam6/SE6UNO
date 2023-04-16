import pygame
from button import Button
import sys

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
    def __int__(self, width, height, text='Sample', on_click_function=None, font_size=25, pop=False):
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.on_click_function = on_click_function
        self.pop = pop

# 팝업창 설정
popup_width = 400
popup_height = 200
popup = pygame.Surface((popup_width, popup_height))
popup.fill(white)

# 버튼 설정
button_width = 100
button_height = 40
close_button = pygame.Rect(popup_width // 2 - button_width - 10, popup_height - 70, button_width, button_height)
ok_button = pygame.Rect(popup_width // 2 + 10, popup_height - 70, button_width, button_height)

# 텍스트 설정
font = pygame.font.Font(None, 32)
text = font.render("This is a popup window", True, black)
popup.blit(text, (50, 50))


def draw_button(button, text, surface):
    pygame.draw.rect(surface, gray, button)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=button.center)
    surface.blit(text_surface, text_rect)


popup_open = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(white)

    if popup_open:
        screen.blit(popup, (screen_width // 2 - popup_width // 2, screen_height // 2 - popup_height // 2))
        draw_button(close_button, "Close", popup)
        draw_button(ok_button, "OK", popup)

        # 마우스 이벤트 처리
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()

        if close_button.collidepoint(mouse_pos) and mouse_clicked[0]:
            popup_open = False
        if ok_button.collidepoint(mouse_pos) and mouse_clicked[0]:
            print("OK button clicked")
            popup_open = False

    pygame.display.flip()
