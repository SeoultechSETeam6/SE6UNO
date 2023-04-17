import pygame

# 색 카드 추가를 위한 리스트
colors = ['red', 'green', 'blue', 'yellow']
values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'skip', 'reverse', 'draw_2', 'bomb', 'one_more']
change_colors = ['red', 'green', 'blue', 'yellow']
change_value = None
regular_cards = []
special_cards = []

class Card:
    def __init__(self, color, value, card_img, card_img_back):
        self.color = color  # 색
        self.value = value  # 숫자
        self.card_img = card_img  # 플레이어가 볼 자신의 카드 이미지
        self.card_img_back = card_img_back  # 상대방 에게 보여질 카드 뒷면

    def __str__(self):
        return f"{self.color} {self.value}"

    def __repr__(self):
        return self.__str__()

    def is_special(self):
        return self.value in ["skip", "reverse", "draw_2", "bomb", "one_more", "shield", "change"]

def generate_cards(color_weakness):
    cards = []
    card_back_image = pygame.image.load("resources/Image/card_images/card_back.png")

    card_folder = "resources/image/cw_card_images" if color_weakness else "resources/image/card_images"
    # 색약 모드와 경로 차별화

    for i in range(2):
        for color in colors:
            for value in values:
                card_image = pygame.image.load(f"{card_folder}/{color}_{value}.png")
                card = Card(color, value, card_image, card_back_image)
                if card.is_special():
                    special_cards.append(card)
                else:
                    regular_cards.append(card)
                if value == "bomb":
                    break

    # 색 없는 실드카드를 한 번에 추가합니다.
    for i in range(2):
        card_image = pygame.image.load(f"resources/Image/card_images/none_shield.png")
        card = Card('none', 'shield', card_image, card_back_image)
        special_cards.append(card)

    # 색 없는 색변경 카드를 추가
    for i in range(2):
        card_image = pygame.image.load(f"resources/Image/card_images/none_change.png")
        card = Card('none', 'change', card_image, card_back_image)
        special_cards.append(card)

    return regular_cards, special_cards
