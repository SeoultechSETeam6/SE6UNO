import pygame
import sys
from button import Button


# Pygame 초기화
pygame.init()
running = True


def single_play_button_click_event():
    print('싱글 플레이 버튼 클릭됨')


def settings_button_click_event():
    print('설정 버튼 클릭됨')


def exit_button_click_event():
    print('나가기 버튼 클릭됨')
    global running
    running = False


# 화면 표시
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("sUNOftware Engineering")

# 로고 표시
logo = pygame.image.load("logo.jpg")
logo_rect = logo.get_rect()
logo_rect.center = (screen_width // 2, logo_rect.height // 2)

# 버튼
buttons = [Button(screen_width // 2, screen_height // 2, 200, 75, '싱글 플레이', single_play_button_click_event),
           Button(screen_width // 2, screen_height // 2 * 1.3, 200, 75, '설정', settings_button_click_event),
           Button(screen_width // 2, screen_height // 2 * 1.6, 200, 75, '나가기', exit_button_click_event)]


# 메인 화면 표시
while running:
    # 배경 색상
    screen.fill((20, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for button in buttons:
        button.process()
        screen.blit(button.surface, button.rect)

    screen.blit(logo, logo_rect)

    # 매 프레임마다 화면 업데이트
    pygame.display.flip()


# 나가기
pygame.quit()
sys.exit()
