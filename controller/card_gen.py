import pygame
from controller.game_view import scale_by

# 색 카드 추가를 위한 리스트
colors = ['red', 'green', 'blue', 'yellow']
values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'skip', 'reverse', 'draw_2', 'one_more', 'bomb']
change_colors = ['red', 'green', 'blue', 'yellow']
change_value = None


class Card:
    def __init__(self, color, value, card_img, card_img_cw, card_img_back):
        self.color = color  # 색
        self.value = value  # 숫자
        self.card_img = None  # 플레이어가 볼 자신의 카드 이미지
        self.card_img_back = None  # 상대방 에게 보여질 카드 뒷면
        self.image = card_img
        self.image_cw = card_img_cw
        self.image_back = card_img_back

    def __str__(self):
        return f"{self.color} {self.value}"

    def __repr__(self):
        return self.__str__()

    def is_special(self):
        return self.value in ["skip", "reverse", "draw_2", "one_more", "bomb", "shield", "change"]

    def is_dummy(self):
        return False


class Dummy(Card):
    def __init__(self, color, value, card_img, card_img_cw, card_img_back):
        super().__init__(color, value, card_img, card_img_cw, card_img_back)

    def is_dummy(self):
        return True


def generate_cards(color_weakness, size_by, computer_logic):
    special_cards = []
    regular_cards = []
    card_back_image = pygame.image.load("./resources/Image/card_images/card_back.png")

    card_folder_cw = "./resources/Image/cw_card_images"
    card_folder = "./resources/Image/card_images"

    # 색약 모드와 경로 차별화
    for color in colors:
        for value in values:
            card_image_cw = pygame.image.load(f"{card_folder_cw}/{color}_{value}.png")
            card_image = pygame.image.load(f"{card_folder}/{color}_{value}.png")
            card = Card(color, value, card_image, card_image_cw, card_back_image)
            if color_weakness:
                card.card_img = scale_by(card_image_cw, size_by)
            else:
                card.card_img = scale_by(card_image, size_by)
            card.card_img_back = scale_by(card_back_image, size_by)

            if card.is_special():
                special_cards.append(card)
            else:
                regular_cards.append(card)
            if value == "bomb":
                break

    # 색 없는 실드 카드를 추가
    for i in range(2):
        card_image = pygame.image.load(f"./resources/Image/card_images/none_shield.png")
        card = Card(None, 'shield', card_image, card_image, card_back_image)
        card.card_img = scale_by(card_image, size_by)
        card.card_img_back = scale_by(card_back_image, size_by)
        special_cards.append(card)

    # 색 없는 색변경 카드를 추가
    for i in range(2):
        card_image = pygame.image.load(f"./resources/Image/card_images/none_change.png")
        card = Card(None, 'change', card_image, card_image, card_back_image)
        card.card_img = scale_by(card_image, size_by)
        card.card_img_back = scale_by(card_back_image, size_by)
        special_cards.append(card)

    if 'D' in computer_logic:
        for i in range(2):
            for color in colors:
                card_image_cw = pygame.image.load(f"{card_folder_cw}/{color}_bomb.png")
                card_image = pygame.image.load(f"{card_folder}/{color}_bomb.png")
                card = Card(color, "bomb", card_image, card_image_cw, card_back_image)
                special_cards.append(card)
                print("D로직 붐카드 2장 추가")
            for color in colors:
                card_image_cw = pygame.image.load(f"{card_folder_cw}/{color}_draw_2.png")
                card_image = pygame.image.load(f"{card_folder}/{color}_draw_2.png")
                card = Card(color, "draw_2", card_image, card_image_cw, card_back_image)
                special_cards.append(card)
                print("D로직 드로우2카드 2장 추가")

    return regular_cards, special_cards


# 체인지카드 발동시 유저한테 보여질 카드.
def generate_for_change_cards(color_weakness, size_by):
    for_change_cards = []
    change_card_folder_cw = "./resources/Image/colorshow_icon"
    change_card_folder = "./resources/Image/colorshow"
    card_back_image = pygame.image.load("./resources/Image/card_images/card_back.png")

    for color in change_colors:
        card_image_cw = pygame.image.load(f"{change_card_folder_cw}/{color}_{change_value}.png")
        card_image = pygame.image.load(f"{change_card_folder}/{color}_{change_value}.png")
        for_change_card = Card(color, change_value, card_image, card_image_cw, card_back_image)
        if color_weakness:
            for_change_card.card_img = scale_by(card_image_cw, size_by)
        else:
            for_change_card.card_img = scale_by(card_image, size_by)
        for_change_card.card_img_back = scale_by(card_back_image, size_by)
        for_change_cards.append(for_change_card)

    return for_change_cards


def generate_c_stage_cards(color_weakness, size_by):
    cards = []
    card_back_image = scale_by(pygame.image.load("./resources/Image/card_images/card_back.png"), size_by)

    # 색약 모드와 경로 차별화
    card_folder_cw = "./resources/Image/cw_card_images"
    card_folder = "./resources/Image/card_images"

    # 색 더미 카드 추가
    for color in colors:
        for value in values:
            card_image = pygame.image.load(f"{card_folder}/{color}_{value}.png")
            card_image_cw = pygame.image.load(f"{card_folder_cw}/{color}_{value}.png")
            card = Dummy(color, value, card_image, card_image_cw, card_back_image)
            if color_weakness:
                card.card_img = scale_by(card_image_cw, size_by)
            else:
                card.card_img = scale_by(card_image, size_by)
            card.card_img_back = scale_by(card_back_image, size_by)
            cards.append(card)

    # 색 없는 실드카드를 한 번에 추가합니다.
    card_image = pygame.image.load(f"./resources/Image/card_images/none_shield.png")
    card = Dummy(None, 'shield', card_image, card_image, card_back_image)
    card.card_img = scale_by(card_image, size_by)
    card.card_img_back = scale_by(card_back_image, size_by)
    cards.append(card)

    return cards


def generate_c_for_change_cards(color_weakness, size_by):
    for_change_cards = []

    change_card_folder_cw = "./resources/Image/colorshow_icon"
    change_card_folder = "./resources/Image/colorshow"
    card_back_image = scale_by(pygame.image.load("./resources/Image/card_images/card_back.png"), size_by)

    for color in change_colors:
        card_image_cw = pygame.image.load(f"{change_card_folder_cw}/{color}_{change_value}.png")
        card_image = pygame.image.load(f"{change_card_folder}/{color}_{change_value}.png")
        for_change_card = Dummy(color, change_value, card_image, card_image_cw, card_back_image)
        if color_weakness:
            for_change_card.card_img = scale_by(card_image_cw, size_by)
        else:
            for_change_card.card_img = scale_by(card_image, size_by)
        for_change_card.card_img_back = scale_by(card_back_image, size_by)

        for_change_cards.append(for_change_card)
    return for_change_cards
