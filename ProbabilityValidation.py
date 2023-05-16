from controller.card_gen import generate_a_stage_cards, generate_cards
from controller.card_shuffle import stage_a_distribute
from controller.game_utils import computer_color_preference


# 테스팅에 약간 시간이 걸린다.
def testing_stage_a_distribute(repeat_count):
    user_regular_card = 0
    user_special_card = 0
    com_regular_card = 0
    com_special_card = 0
    for i in range(repeat_count):
        regular_cards, special_cards = generate_a_stage_cards(False, 1)
        hands, remaining_cards = stage_a_distribute(2, regular_cards, special_cards, 6)
        print("현재 진행 상황: ", i, "/", repeat_count)
        for n in hands[0]:
            if n.is_special() is False:
                user_regular_card = user_regular_card + 1
            elif n.is_special() is True:
                user_special_card = user_special_card + 1
        for n in hands[1]:
            if n.is_special() is False:
                com_regular_card = com_regular_card + 1
            elif n.is_special() is True:
                com_special_card = com_special_card + 1
    print("유저의 일반 카드 갯수: ", user_regular_card)
    print("유저의 기술 카드 갯수: ", user_special_card)
    print("AI의 일반 카드 갯수: ", com_regular_card)
    print("AI의 기술 카드 갯수 ", com_special_card)
    print("유저 대비 컴퓨터가 기술카드를 받은 배율: ", com_special_card / user_special_card)
    print("컴퓨터 대비 유저가 일반카드를 받은 배율: ", user_regular_card / com_regular_card)


#  color_number 파라미터에 0 = red, 1 = blue, 2 = yellow, 3 = green 이 된다.
def testing_color_preference(repeat_count, color_number):
    color_list = ["red", "blue", "yellow", "green"]
    color_logic_count = 0
    basic_logic_count = 0
    cards = generate_cards(False, 1)
    board_card = [card for card in cards if card.value == "shield"]
    now_player_hands = [card for card in cards if card.value == "1" and card.color == color_list[color_number]]
    color_preference = color_list[color_number]
    for i in range(repeat_count):
        playable, card_index, playable_special_check = computer_color_preference(now_player_hands, board_card,
                                                                                 color_preference)
        if playable is True:
            color_logic_count = color_logic_count + 1
        elif playable is False:
            basic_logic_count = basic_logic_count + 1
    print("색 선호도에 맞는 카드를 선택한 횟수: ", color_logic_count)
    print("기본 로직을 선택한 횟수: ", basic_logic_count)
    print("색 선호도에 맞는 카드를 선택한 비율: ", color_logic_count / (color_logic_count + basic_logic_count))
    print("기본 로직을 선택한 비율: ", basic_logic_count / (color_logic_count + basic_logic_count))


# testing_stage_a_distribute(1000)
# testing_color_preference(1000, 0)
