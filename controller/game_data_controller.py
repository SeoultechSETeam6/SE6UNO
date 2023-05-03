import json
import pygame

FILEPATH = "../game_settings.json"
INIT_GAME_DATA = {
    "settings": {
        "display_size": {
            "width": 1920,
            "height": 1080
        },
        "color_weakness": False,
        "key_setting": {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "enter": pygame.K_RETURN
        },
        "volume": {
            "sound": 1.0,
            "background": 1.0,
            "effect": 1.0
        }
    },
    "stage_clear_status": {
        "1st": 0,
        "2nd": 0,
        "3rd": 0,
        "4th": 0
    }
}
game_data = INIT_GAME_DATA


def get_settings_data():
    try:
        with open(FILEPATH) as fr:
            settings_data = json.load(fr)["settings"]
    except FileNotFoundError:
        with open(FILEPATH, 'w') as fw:
            json.dump(INIT_GAME_DATA, fw, indent=4)
            settings_data = INIT_GAME_DATA["settings"]

    return settings_data


def set_settings_data():
    with open(FILEPATH, 'w') as fw:
        json.dump(game_data, fw, indent=4)


def get_stage_clear_data():
    try:
        with open(FILEPATH) as fr:
            clear_data = json.load(fr)["stage_clear_status"]
    except FileNotFoundError:
        with open(FILEPATH, 'w') as fw:
            json.dump(game_data, fw, indent=4)
            clear_data = INIT_GAME_DATA["stage_clear_status"]

    return clear_data
