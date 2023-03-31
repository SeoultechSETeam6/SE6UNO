import random
import pygame


# 유저의 카드를 그리는 함수
def draw_cards_user(screen, cards, x, y, spacing, hovered_card_index=None):
    for i, card in enumerate(cards):
        card_rect = card.card_img.get_rect()
        card_rect.topleft = (x + i * spacing, y)
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


# 마우스 오버를 한 카드를 찾는 함수
def find_hovered_card(cards, x, y, spacing, mouse_x, mouse_y):
    for i, card in enumerate(cards):
        card_width, card_height = card.card_img.get_size()
        card_x = x + i * spacing
        card_y = y
        if card_x <= mouse_x < card_x + card_width and card_y <= mouse_y < card_y + card_height:
            return i
    return None


def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


# 카드 클릭
def get_clicked_card(cards, x, y, spacing, mouse_x, mouse_y):
    for i, card in enumerate(cards):
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
def draw_top_card(screen, card, x, y):
    if card:
        screen.blit(card.card_img, (x, y))


# 내는 카드 유효성 검사
def is_valid_move(card, top_card):
    if card.color == top_card.color or card.value == top_card.value or card.color == "none" or top_card.color == "none":
        return True
    return False


# ai 턴
def computer_turn(now_player_hands, current_player_index, current_player, board_card, remain_cards, player_count,
                  direction, player_hands, delay_time2):
    top_card = get_top_card(board_card)
    playable_cards = [card for card in now_player_hands if is_valid_move(card, top_card)]

    # 낼 카드가 있는 경우
    if playable_cards:
        selected_card = random.choice(playable_cards)
        board_card.append(selected_card)
        now_player_hands.remove(selected_card)

        # 특수 카드 처리
        if selected_card.is_special():
            current_player_index, direction = apply_special_card_effects(selected_card, current_player_index,
                                                                         current_player, direction, player_hands,
                                                                         remain_cards, player_count)
            return current_player_index, direction
        else:
            current_player_index = (current_player_index + direction) % player_count
            return current_player_index, direction
    # 컴퓨터가 놓을 수 있는 카드가 없는 경우
    else:
        if remain_cards:
            drawn_card = remain_cards.pop()
            now_player_hands.append(drawn_card)
            pygame.time.delay(delay_time2)
            # 드로우 한 카드를 낼 수 있는 경우 카드를 낸다
            if is_valid_move(drawn_card, top_card):
                drawn_card_index = now_player_hands.index(drawn_card)
                now_player_hands.pop(drawn_card_index)
                board_card.append(drawn_card)
                # board_card.append(drawn_card) 오류 구문 해결
                # now_player_hands.pop(drawn_card) 오류 구문 해결
                # 뽑은 카드가 special일 때,
                if drawn_card.is_special():
                    current_player_index, direction = apply_special_card_effects(drawn_card, current_player_index,
                                                                                 current_player, direction, player_hands
                                                                                 , remain_cards, player_count)
                    return current_player_index, direction
                # 뽑은 카드가 special이 아닐때,
                else:
                    current_player_index = (current_player_index + direction) % player_count
                    return current_player_index, direction
            # 낼 수 없으면, 턴을 넘긴다.
            else:
                current_player_index = (current_player_index + direction) % player_count
                return current_player_index, direction
        else:
            # 작동하지 않는 함수. 혹시몰라서 넣어둠. 이 함수는 remain_cards에 남은 카드가 없을 때 발동함.
            current_player_index = (current_player_index + direction) % player_count
            return current_player_index, direction


# 스페셜 카드 적용
def apply_special_card_effects(card, current_player_index, current_player, direction, player_hands, remain_cards,
                               player_count):
    # 역방향 카드
    if card.value == "reverse":
        print("reverse카드 이벤트 발생")
        direction *= -1
        current_player_index = (current_player_index + direction) % player_count
        print(current_player_index, direction)
        return current_player_index, direction

    # 스킵 카드
    elif card.value == "skip":
        print("skip카드 이벤트 발생")
        current_player_index = (current_player_index + direction + direction) % player_count
        print(current_player_index, direction)
        return current_player_index, direction

    # 2장 드로우 공격
    elif card.value == "draw_2":
        print("draw_2카드 이벤트 발생")
        next_player_index = (current_player_index + direction) % player_count
        # has_shield = any(check_card.value == "shield" for check_card in player_hands[next_player_index])
        has_shield = next((check_card for check_card in player_hands[next_player_index] if card.value == "shield"),
                          None)
        # shield 카드가 없으면 2장 뽑고, 턴 넘기기
        if not has_shield:
            for _ in range(2):
                add_card = remain_cards.pop()
                player_hands[next_player_index].append(add_card)
            current_player_index = (current_player_index + (direction * 2)) % player_count
            print(current_player_index, direction)
            return current_player_index, direction
        # shield 카드가 있으면 사용후, 턴 넘기기
        else:
            shield_card = next(check_card for check_card in player_hands[next_player_index] if card.value == "shield")
            player_hands[next_player_index].remove(shield_card)
            current_player_index = (current_player_index + (direction * 2)) % player_count
            print(current_player_index, direction)
            return current_player_index, direction

    elif card.value == "one_more":
        print("one_more카드 이벤트 발생")
        return current_player_index, direction

    # 폭탄 카드
    elif card.value == "bomb":
        print("bomb카드 이벤트 발생")
        for i, hand in enumerate(player_hands):
            if i != current_player:
                for _ in range(2):
                    add_card = remain_cards.pop()
                    hand.append(add_card)
        current_player_index = (current_player_index + direction) % player_count
        print(current_player_index, direction)
        return current_player_index, direction

    # 실드 카드(딘순히 내는 동작)
    elif card.value == "shield":
        print("shield카드 냈음")
        current_player_index = (current_player_index + direction) % player_count
        print(current_player_index, direction)
        return current_player_index, direction
