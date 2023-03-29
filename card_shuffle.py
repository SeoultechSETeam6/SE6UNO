import random
from card_gen import generate_cards, Card


def shuffle_cards(cards):
    random.shuffle(cards)
    return cards


def distribute_cards(cards, player_count, card_count):
    hands = []
    for _ in range(player_count):
        hand = [cards.pop() for _ in range(card_count)]
        hands.append(hand)

    return hands, cards


# 카드 생성 및 셔플
cards = generate_cards()
shuffled_cards = shuffle_cards(cards)
'''
# 플레이어 수와 각 플레이어가 받을 카드 수 지정
player_count = 4
card_count = 7

# 카드 분배
player_hands, remain_cards = distribute_cards(shuffled_cards, player_count, card_count)
print(remain_cards)
print(player_hands)

has_shield = any(c.value == "shield" for c in player_hands[0])
print(has_shield)

current_player_index = 0
for i, hand in enumerate(player_hands):
    print(hand)
    if i != current_player_index:
        for _ in range(2):
            card = remain_cards.pop()
            hand.append(card)
print(player_hands)
'''

'''임시 코드 (추후 삭제)
print(player_hands)
print(remain_cards)

print(player_hands[0])
'''