import pygame
import sys
import in_game
from button import Button
from option import basic_option as basic
from option.setting_option import Option


# Pygame 초기화
pygame.init()
running = True
clock = pygame.time.Clock()


def settings_button_click_event():
    print('설정 버튼 클릭됨')
    option = Option()
    option.run()
    del option


def exit_button_click_event():
    print('나가기 버튼 클릭됨')
    global running
    running = False


# 화면 표시
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("sUNOftware Engineering")

# 로고 표시
logo = pygame.image.load("resources/Image/logo.jpg")
logo_rect = logo.get_rect()
logo_rect.center = (screen_width // 2, logo_rect.height // 2)

# 버튼
buttons = [Button(screen_width // 2, screen_height // 2, 200, 75, '싱글 플레이', in_game.game),
           Button(screen_width // 2, screen_height // 2 * 1.3, 200, 75, '설정', settings_button_click_event),
           Button(screen_width // 2, screen_height // 2 * 1.6, 200, 75, '나가기', exit_button_click_event)]

selected_button_index = 0
buttons[selected_button_index].selected = True

# 배경 색상
screen.fill((20, 20, 20))

# 메인 화면 표시
while running:
    clock.tick(basic.fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                buttons[selected_button_index].selected = False
                selected_button_index = (selected_button_index - 1) % len(buttons)
                buttons[selected_button_index].selected = True
            elif event.key == pygame.K_DOWN:
                buttons[selected_button_index].selected = False
                selected_button_index = (selected_button_index + 1) % len(buttons)
                buttons[selected_button_index].selected = True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                buttons[selected_button_index].on_click_function()

    for button in buttons:
        button.process()
        screen.blit(button.surface, button.rect)

    screen.blit(logo, logo_rect)

    # 매 프레임마다 화면 업데이트
    pygame.display.flip()


# 나가기
pygame.quit()
sys.exit()
