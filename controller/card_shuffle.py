import random
# from controller.card_gen import generate_cards, Card


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
    normal_prob = 0.5
    special_prob = 1 - normal_prob

    for i in range(player_count):
        for _ in range(card_count):
            if i == 0:
                card_type = random.choices(['regular', 'special'], [normal_prob, special_prob])[0]
            else:
                card_type = random.choices(['regular', 'special'], [normal_prob - 0.1, special_prob + 0.1])[0]

            if card_type == 'regular':
                card = random.choice(regular_cards)
                regular_cards.remove(card)
            else:
                card = random.choice(special_cards)
                special_cards.remove(card)

            hands[i].append(card)

    remaining_cards = regular_cards + special_cards
    random.shuffle(remaining_cards)
    return hands, remaining_cards
