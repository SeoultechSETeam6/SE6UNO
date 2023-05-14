import random
import pygame


# 유저의 카드를 그리는 함수
def draw_cards_user(screen, cards, x, y, max_per_row, spacing, hovered_card_index=None):
    for i, card in enumerate(cards):
        row = i // max_per_row
        column = i % max_per_row
        card_rect = card.card_img.get_rect()
        card_rect.topleft = (x + column * spacing, y + row * (spacing + 10))
        if i == hovered_card_index:
            card_rect.y -= 50
        screen.blit(card.card_img, card_rect)


# 컴퓨터 플레이어들의 카드를 그리는 함수
def draw_cards_ai(screen, cards, x, y, max_per_row, spacing, hovered_card_index=None, show_back=False):
    for i, card in enumerate(cards):
        row = i // max_per_row
        column = i % max_per_row
        card_rect = card.card_img.get_rect()
        card_rect.topleft = (x + column * spacing, y + row * spacing)
        if i == hovered_card_index:
            card_rect.y -= 50
        if show_back:
            screen.blit(card.card_img_back, card_rect)
        else:
            screen.blit(card.card_img, card_rect)


# 드로우 카드 그리기
def draw_change_card(screen, change_cards, x, y, spacing, hovered_card_index=None):
    for i, card in enumerate(change_cards):
        card_rect = card.card_img.get_rect()
        card_rect.topleft = (x + i * spacing, y)
        if i == hovered_card_index:
            card_rect.y -= 50
        screen.blit(card.card_img, card_rect)


# 마우스 오버를 한 유저 카드를 찾는 함수
def find_hovered_card(cards, x, y, spacing, mouse_x, mouse_y, max_per_row, hovered_card_index):
    for i, card in enumerate(cards):
        card_width, card_height = card.card_img.get_size()
        row = i // max_per_row
        column = i % max_per_row
        card_x = x + column * spacing
        card_y = y + row * (spacing + 10)  # 각 행의 시작 y 좌표를 고려하도록 수정
        if card_x <= mouse_x < card_x + card_width and card_y <= mouse_y < card_y + card_height:
            return i
    return hovered_card_index


# 마우스 오버를 한 체인지 카드 찾기
def find_hovered_change(change, x5, y5, spacing5, mouse_x, mouse_y, hovered_card_index):
    for i, card in enumerate(change):
        card_width, card_height = card.card_img.get_size()
        card_x = x5 + i * spacing5
        card_y = y5
        if card_x <= mouse_x < card_x + card_width and card_y <= mouse_y < card_y + card_height:
            return i
    return hovered_card_index


def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


# 카드 클릭
def get_clicked_card(cards, x, y, spacing, mouse_x, mouse_y, max_per_row):
    for i, card in enumerate(cards):
        card_width, card_height = card.card_img.get_size()
        row = i // max_per_row
        column = i % max_per_row
        card_x = x + column * spacing
        card_y = y + row * (spacing + 10)  # 각 행의 시작 y 좌표를 고려하도록 수정
        if card_x <= mouse_x < card_x + card_width and card_y <= mouse_y < card_y + card_height:
            return i, card
    return None, None


def get_clicked_change(change_cards, x, y, spacing, mouse_x, mouse_y):
    for i, card in enumerate(change_cards):
        column = i
        card_rect = card.card_img.get_rect()
        card_rect.topleft = (x + column * spacing, y)
        if card_rect.collidepoint(mouse_x, mouse_y):
            return i, card
    return None, None


# 드로우 할 수 있을 때 나타나는 문구
def draw_button(screen, text, font, color, rect):
    pygame.draw.rect(screen, (255, 255, 255), rect, 2)
    lines = text.split('\n')
    line_spacing = font.get_linesize() + 5  # Add some additional space between the lines
    total_height = line_spacing * len(lines)

    for index, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = rect.centerx
        text_rect.centery = rect.centery - total_height // 2 + index * line_spacing
        screen.blit(text_surface, text_rect)


# 카드를 가져옴
def get_top_card(deck):
    if deck:
        return deck[-1]
    return None


# 카드 한 장 뽑아옴
def draw_board_card(screen, card, x, y):
    if card:
        screen.blit(card.card_img, (x, y))


# 내는 카드 유효성 검사
def is_valid_move(card, top_card):
    if card.color is None or top_card.color is None or card.color == top_card.color or card.value == top_card.value:
        return True
    return False


def computer_uno(one_flags, uno_current_player):
    one_flags[uno_current_player] = True
    com_uno_current_time = pygame.time.get_ticks()
    com_uno_delay_time = random.randint(2000, 3000)
    return one_flags, com_uno_current_time, com_uno_delay_time


# 컴퓨터 플레이블 카드 체크후 낼 카드 고르기
def computer_playable_card(now_player_hands, board_card):
    top_card = get_top_card(board_card)
    playable_cards = [card for card in now_player_hands if is_valid_move(card, top_card)]
    if playable_cards:
        selected_card = random.choice(playable_cards)
        playable = True
        card_index = now_player_hands.index(selected_card)
    else:
        playable = False
        card_index = None
    return playable, card_index


'''
def computer_color_preference(now_player_hands, board_card, current_player):
    top_card = get_top_card(board_card)
    percentage = random.randint(1, 10)
    if percentage < 6:
        playable_cards = [card for card in now_player_hands if is_valid_move(card, top_card) and card]
    elif percentage > 5:
'''


def playable_attack_card(now_player_hands, board_card):
    top_card = get_top_card(board_card)
    playable_attack_cards = [card for card in now_player_hands if is_valid_move(card, top_card) and
                             (card.value == 'draw_2' or card.value == 'bomb')]
    if playable_attack_cards:
        selected_card = random.choice(playable_attack_cards)
        playable = True
        card_index = now_player_hands.index(selected_card)
        playable_special_check = True
    else:
        playable = False
        card_index = None
        playable_special_check = False
    return playable, card_index, playable_special_check


def playable_special_card(now_player_hands, board_card):
    top_card = get_top_card(board_card)
    playable_special_cards = [card for card in now_player_hands if is_valid_move(card, top_card) and
                             card.is_special() is True]
    if playable_special_cards:
        selected_card = random.choice(playable_special_cards)
        playable = True
        card_index = now_player_hands.index(selected_card)
        playable_special_check = True
    else:
        playable = False
        card_index = None
        playable_special_check = False
    return playable, card_index, playable_special_check


def user_submit_card(card, card_index, board_card, now_player_hand):
    board_card.append(card)
    now_player_hand.pop(card_index)
    pop_card = card
    return board_card, now_player_hand, pop_card


def com_submit_card(card, card_index, board_card, now_player_hand):
    board_card.append(card)
    now_player_hand.pop(card_index)
    return board_card, now_player_hand


# 스페셜 카드 적용
def apply_special_card_effects(card, current_player, direction, player_hands, remain_cards, player_count, stage):

    # 역방향 카드
    if card.value == "reverse":
        direction *= -1
        if stage != "A":
            current_player = (current_player + direction) % player_count
        return current_player, direction

    # 스킵 카드
    elif card.value == "skip":
        pygame.time.delay(100)
        current_player = (current_player + direction + direction) % player_count
        return current_player, direction

    # 2장 드로우 공격
    elif card.value == "draw_2":
        next_player = (current_player + direction) % player_count
        has_shield = next((check_card for check_card in player_hands[next_player] if check_card.value == "shield")
                          , None)
        # shield 카드가 없으면 2장 뽑고, 턴 넘기기
        if not has_shield:
            for _ in range(2):
                add_card = remain_cards.pop()
                player_hands[next_player].append(add_card)
            current_player = (current_player + (direction * 2)) % player_count
            pygame.time.delay(100)
            return current_player, direction
        # shield 카드가 있으면 사용후, 턴 넘기기
        else:
            shield_card = next(check_card for check_card in player_hands[next_player] if check_card.value == "shield")
            player_hands[next_player].remove(shield_card)
            current_player = (current_player + (direction * 2)) % player_count
            pygame.time.delay(100)
            return current_player, direction

    elif card.value == "one_more":
        pygame.time.delay(100)
        return current_player, direction

    # 폭탄 카드
    elif card.value == "bomb":
        for i, hand in enumerate(player_hands):
            if i != current_player:
                add_card = remain_cards.pop()
                hand.append(add_card)
        if stage != "A":
            current_player = (current_player + direction) % player_count
        return current_player, direction

    # 실드 카드(딘순히 내는 동작)
    elif card.value == "shield":
        if stage != "A":
            current_player = (current_player + direction) % player_count
        return current_player, direction

    # 체인지 카드(카드색 바꿈)
    elif card.value == "change":
        if stage != "A":
            current_player = (current_player + direction) % player_count
        return current_player, direction


def random_top_card_color(top_card, dummy_cards, board_card, dummy_cards_for_change):  # stage c애서 발동
    color_list = ['red', 'blue', 'green', 'yellow']
    color = color_list[random.randint(0, 3)]
    print("더미카드 목록: ", dummy_cards)
    print("원래 top card: ", top_card)
    if top_card.value is not None:
        if top_card.color is None:
            print("top_card의 color가 none이므로, 계속 진행합니다.")
            return board_card
        elif top_card.color is not None:
            dummy_card = [card for card in dummy_cards if card.value == top_card.value and card.color == color]
            print("더미 카드: ", dummy_card)
            print("더미 카드 이미지: ", dummy_card[0].card_img)
            board_card.append(dummy_card[0])
    elif top_card.value is None:
        dummy_card = dummy_cards_for_change[random.randint(0, 3)]
        board_card.append(dummy_card)
    return board_card


def card_reshuffle(board_card, remain_cards):
    print("리셔플 발생")
    print(remain_cards)
    top_card = board_card[-1]
    board_card = board_card[:-1]  # top_card를 제외한 나머지 카드를 가져옵니다.

    remain_cards.extend(board_card)  # 가져온 카드를 remain_cards에 추가합니다.
    board_card = [top_card]  # board_card를 top_card만 남겨둡니다.

    # 카드 change, 더미 항목을 제거한다.
    remain_cards = [card for card in remain_cards if card.value is not None or not card.is_dummy]
    random.shuffle(remain_cards)  # remain_cards를 무작위로 섞습니다.
    print("셔플완료")
    print(remain_cards)
    return board_card, remain_cards
