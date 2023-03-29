'''
elif card.value == "bomb":
for i, hand in enumerate(player_hands):
    if i != current_player_index:
        for _ in range(2):
            hand.append(remain_cards.pop())
current_player_index = (current_player_index + direction) % player_count
return current_player_index, direction
'''

player_hands = []
player_hands = [[1, 2, 3, 4, 5], [9, 8, 7, 6], [77, 88, 99]]
remain_cards = [55, 66, 77, 88, 99, 101, 102, 103, 104, 105, 106]
print(len(player_hands[0]))

for i, hand in enumerate(player_hands):
    print(hand)
    hand.append(7)
    print(hand)
print(player_hands)

has_shield = any(c == 7 for c in player_hands[0])
print(has_shield)