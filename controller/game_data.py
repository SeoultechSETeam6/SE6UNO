import json
import pygame

# 게임 설정 기본값
FILEPATH = "./game_data.json"
ACHIEVEMENTS = [{
        "name": "승리",
        "description": "싱글 플레이에서 1회 승리",
        "image": "single_player_winner.png"
    }, {
        "name": "스테이지 마스터",
        "description": "스토리의 모든 스테이지 클리어",
        "image": "single_player_winner.png"
    }, {
        "name": "스피드 레이서",
        "description": "싱글 플레이에서 10턴안에 승리",
        "image": "speed_racer.png"
    }, {
        "name": "기사도",
        "description": "기술 카드를 사용하지 않고 승리",
        "image": "chivalry.png"
    }, {
        "name": "간발의 차",
        "description": "다른 플레이어가 UNO 선언한 뒤에 승리",
        "image": "win_by_a_nose.png"
    }, {
        "name": "테러리스트",
        "description": "폭탄 카드를 1회 사용",
        "image": "terrorist.png"
    }, {
        "name": "적절한 방어",
        "description": "방어 카드로 상대방의 공격을 방어",
        "image": "adequate_defense.png"
    }, {
        "name": "욕심쟁이",
        "description": "one_more 카드 사용",
        "image": "greedy_man.png"
    }]
INIT_GAME_DATA = {
    "settings": {
        "resolution": {
            "width": 1920,
            "height": 1080
        },
        "color_weakness": False,
        "key": {
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
    "stage_clear_count": {
        "1st": 0,
        "2nd": 0,
        "3rd": 0,
        "4th": 0
    },
    "achievement": {
        0: {
            "achieved": False,
            "achieved_date": None
        },
        1: {
            "achieved": False,
            "achieved_date": None
        },
        2: {
            "achieved": False,
            "achieved_date": None
        },
        3: {
            "achieved": False,
            "achieved_date": None
        },
        4: {
            "achieved": False,
            "achieved_date": None
        },
        5: {
            "achieved": False,
            "achieved_date": None
        },
        6: {
            "achieved": False,
            "achieved_date": None
        },
        7: {
            "achieved": False,
            "achieved_date": None
        }
    }
}


# 설정 불러오기
def load_settings():
    try:
        with open(FILEPATH, encoding='utf-8') as fr:
            settings_data = json.load(fr)["settings"]
    except FileNotFoundError:
        with open(FILEPATH, 'w', encoding='utf-8') as fw:
            json.dump(INIT_GAME_DATA, fw, indent=4)
            settings_data = INIT_GAME_DATA["settings"]

    return settings_data


# 설정 저장
def save_settings(settings_data):
    with open(FILEPATH, encoding='utf-8') as fr:
        data = json.load(fr)
        data["settings"] = settings_data

    with open(FILEPATH, 'w', encoding='utf-8') as fw:
        json.dump(data, fw, indent=4)


def load_stage_clear():
    try:
        with open(FILEPATH, encoding='utf-8') as fr:
            clear_data = json.load(fr)["stage_clear_count"]
    except FileNotFoundError:
        with open(FILEPATH, 'w', encoding='utf-8') as fw:
            json.dump(INIT_GAME_DATA, fw, indent=4)
            clear_data = INIT_GAME_DATA["stage_clear_count"]

    return clear_data


def load_achieved_status():
    try:
        with open(FILEPATH, encoding='utf-8') as fr:
            data = json.load(fr)["achievement"]
    except FileNotFoundError:
        with open(FILEPATH, 'w', encoding='utf-8') as fw:
            json.dump(INIT_GAME_DATA, fw, indent=4)
            data = INIT_GAME_DATA["achievement"]

    return data
