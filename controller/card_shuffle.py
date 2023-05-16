import random
from controller.card_gen import generate_a_stage_cards, Card


def shuffle_cards(cards):
    random.shuffle(cards)
    return cards


def distribute_cards(cards, player_count, card_count):
    hands = []
    for _ in range(player_count):
        hand = [cards.pop() for _ in range(card_count)]
        hands.append(hand)
    return hands, cards


def stage_a_distribute(player_count, regular_cards, special_cards, card_count):
    hands = [[] for _ in range(player_count)]
    user_normal_prob = 0.6
    user_special_prob = 1 - user_normal_prob
    com_special_prob = user_special_prob * 1.5
    com_normal_prob = 1 - com_special_prob

    for i in range(player_count):
        for _ in range(card_count):
            if i == 0:
                card_type = random.choices(['regular', 'special'], [user_normal_prob, user_special_prob])[0]
            else:
                card_type = random.choices(['regular', 'special'], [com_normal_prob, com_special_prob])[0]

            if card_type == 'regular':
                card = random.choice(regular_cards)
                regular_cards.remove(card)
            elif card_type == 'special':
                if len(special_cards) > 0:
                    card = random.choice(special_cards)
                    special_cards.remove(card)
                elif len(special_cards) == 0:
                    print("남은 기술 카드가 존재하지 않으므로, 일반 카드를 부여합니다.")
                    card = random.choice(regular_cards)
                    regular_cards.remove(card)

            hands[i].append(card)

    remaining_cards = regular_cards + special_cards
    random.shuffle(remaining_cards)
    return hands, remaining_cards


