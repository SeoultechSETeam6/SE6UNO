import pygame

# 옵션 정보를 초기화를 위한 변수
display_size = [1920, 1080]
color_weakness = False
key_setting = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT,
               'right': pygame.K_RIGHT, 'enter': pygame.K_RETURN}

# 화면 크기 변경시 같이 크기가 변경되어야 할 변수
button_size = [[200, 75], [167, 62.5], [125, 46.875]]
font_size = [[60, 25], [50, 20], [37, 16]]
logo_size = [[700, 500], [584, 417], [467, 333]]

# 공통된 변수
game_title = "UNO Game"
fps = 60


# 마우스 중복 클릭 방지 메소드
def mouse_event_remove():
    while True:
        pygame.event.clear()
        if not pygame.mouse.get_pressed(num_buttons=3)[0]:
            break
