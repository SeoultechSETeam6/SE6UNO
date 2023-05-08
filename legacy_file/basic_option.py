import pygame

# 옵션 정보를 초기화를 위한 변수
display_size = [1920, 1080]
color_weakness = False
key_setting = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT,
               'right': pygame.K_RIGHT, 'enter': pygame.K_RETURN}

# 화면 크기 변경시 같이 크기가 변경되어야 할 변수
button_size = [[200, 75], [167, 62.5], [125, 46.875]]
campaign_map_button_size = [[500, 347], [417.5, 290], [312.5, 217]]
font_size = [[60, 25], [50, 20], [37, 16]]
logo_size = [[700, 500], [584, 417], [467, 333]]
change_size = [1, 0.83, 0.66]

# 공통된 변수
game_title = "UNO Game"
fps = 60
sound_volume = 1.0
background_volume = 1.0
effect_volume = 1.0


def scale_by(surface, scale_factor):
    width, height = surface.get_size()
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return pygame.transform.scale(surface, (new_width, new_height))
