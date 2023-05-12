import pygame

# 화면 크기 변경시 같이 크기가 변경되어야 할 변수
BUTTON_SIZE = [[200, 75], [167, 62.5], [125, 46.875]]
STAGE_BUTTON_SIZE = [[500, 347], [417.5, 290], [312.5, 217]]
FONT_SIZE = [[60, 25], [50, 20], [37, 16]]
GAME_LOGO_SIZE = [[700, 500], [584, 417], [467, 333]]
CHANGE_SIZE = [1, 0.83, 0.66]

# 공통된 변수
GAME_TITLE = "UNO Game"
FONT_PATH = "./resources/maplestory_font.ttf"
FPS = 60

# 해상도 설정이 변경됐는지 확인하는 변수
resolution_changed = False

def set_size(width=1920):
    """
    해상도의 가로를 인수로 받아 게임의 각종 오브젝트의 크기를 dictionary 형태로 Return하는 함수입니다.\n
    :return: dict
    """
    if width == 1920:
        size = {
            "button": BUTTON_SIZE[0],
            "stage": STAGE_BUTTON_SIZE[0],
            "font": FONT_SIZE[0],
            "logo": GAME_LOGO_SIZE[0],
            "change": CHANGE_SIZE[0]
        }
    elif width == 1600:
        size = {
            "button": BUTTON_SIZE[1],
            "stage_button": STAGE_BUTTON_SIZE[1],
            "font": FONT_SIZE[1],
            "logo": GAME_LOGO_SIZE[1],
            "change": CHANGE_SIZE[1]
        }
    else:
        size = {
            "button": BUTTON_SIZE[2],
            "stage_button": STAGE_BUTTON_SIZE[2],
            "font": FONT_SIZE[2],
            "logo": GAME_LOGO_SIZE[2],
            "change": CHANGE_SIZE[2]
        }
    return size


def scale_by(surface, scale_factor):
    width, height = surface.get_size()
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return pygame.transform.scale(surface, (new_width, new_height))