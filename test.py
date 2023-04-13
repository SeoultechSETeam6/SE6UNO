# 유저의 턴일 경우
if user_turn:
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked_card_index, clicked_card = get_clicked_card(player_hands[0], x, y, spacing, mouse_x,
                                                            mouse_y)
        # remain_cards 클릭 확인
        clicked_remain_cards = remain_cards_rect.collidepoint(mouse_x, mouse_y)
        # next_turn_button 클릭 확인
        clicked_next_turn_button = next_turn_button_rect.collidepoint(mouse_x, mouse_y)

        # 클릭된 카드가 실제로 존재하는지 확인하는 조건문. 클릭된 카드가 존재하면 내부 코드 실행
        if clicked_card is not None or clicked_remain_cards or clicked_next_turn_button or user_uno_clicked:
            top_card = get_top_card(board_card)
            # 카드를 드로우함
            if clicked_remain_cards and not draw_requested and pop_card is None:
                user_draw_time = pygame.time.get_ticks()
                player_hands[0].append(remain_cards.pop())
                new_drawn_card = player_hands[0][-1]
                draw_requested = True
            # 카드를 드로우 하고 턴을 넘기는 함수.
            elif draw_requested and new_drawn_card is not None and clicked_next_turn_button and pop_card is None:
                current_player_index = (current_player_index + direction) % player_count
                draw_requested = False
                new_drawn_card = None
            # 카드를 드로우 하고, 드로우한 카드를 내는 함수.
            elif draw_requested and new_drawn_card is not None and is_valid_move(new_drawn_card,
                                                                                 top_card) and clicked_card == new_drawn_card:
                board_card.append(clicked_card)
                player_hands[0].pop(clicked_card_index)
                pop_card = clicked_card  # 카드를 냄
                user_uno_check = check_uno(player_hands[0])
                if user_uno_check:
                    one_flags[0] = True
                    uno_current_time = pygame.time.get_ticks()
                    uno_delay_time = random.randint(500, 1000)
                    print("check!", uno_current_time, uno_delay_time)
            # 카드를 드로우하지 않고, 카드를 냄
            elif not draw_requested and pop_card is None:
                top_card = get_top_card(board_card)
                # 유효성 검사
                if clicked_card is not None and is_valid_move(clicked_card, top_card):
                    board_card.append(clicked_card)
                    player_hands[0].pop(clicked_card_index)
                    pop_card = clicked_card
                    user_uno_check = check_uno(player_hands[0])
                    print(310)
                    if user_uno_check:
                        print(312)
                        one_flags[0] = True
                        print(314)
                        uno_current_time = pygame.time.get_ticks()
                        uno_delay_time = random.randint(2000, 3000)
                        print("check!", uno_current_time, uno_delay_time)
            # 카드를 냈을 때,
            elif pop_card is not None:
                print("카드를 냄")
                # 우노일 경우
                if user_uno_check:
                    print("우노발동")
                    uno_clicked = True
                    print("click uno", uno_current_time, uno_delay_time, one_flags)
                    if user_uno_clicked:
                        one_flags[0] = False
                        uno_clicked = False
                        # 내는 카드가 special인 경우
                        print("user_uno_click", one_flags)
                        if pop_card.is_special():
                            current_player_index, direction, uno_current_player_index = \
                                apply_special_card_effects(pop_card, current_player_index,
                                                           current_player, direction, player_hands,
                                                           remain_cards, player_count)
                            pop_card = None  # 낸 카드 초기화
                            draw_requested = False
                            new_drawn_card = None
                            user_uno_check = False
                        # 내는 카드가 special이 아닌 경우
                        else:
                            current_player_index = (current_player_index + direction) % player_count
                            pop_card = None  # 낸 카드 초기화
                            draw_requested = False
                            new_drawn_card = None
                            user_uno_check = False  # 낸 카드 초기화
                else:
                    print("우노발동안함")
                    # 내는 카드가 special인 경우
                    if pop_card.is_special():
                        current_player_index, direction, uno_current_player_index = apply_special_card_effects(pop_card,
                                                                                                               current_player_index,
                                                                                                               current_player,
                                                                                                               direction,
                                                                                                               player_hands,
                                                                                                               remain_cards,
                                                                                                               player_count)
                        pop_card = None  # 낸 카드 초기화
                        draw_requested = False
                        new_drawn_card = None
                        user_uno_check = False
                    # 내는 카드가 special이 아닌 경우
                    else:
                        current_player_index = (current_player_index + direction) % player_count
                        pop_card = None
                        draw_requested = False
                        new_drawn_card = None
                        user_uno_check = False
current_time = pygame.time.get_ticks()

# 유저의 턴일 때 시간이 초과되면 드로우하고 턴을 넘김
if pop_card is not None and one_flags[0] and user_turn:
    if current_time - uno_current_time >= uno_delay_time:
        uno_drawn_card = remain_cards.pop()
        player_hands[0].append(uno_drawn_card)
        # 내는 카드가 special인 경우
        if pop_card.is_special():
            current_player_index, direction, uno_current_player_index = apply_special_card_effects(
                pop_card, current_player_index, current_player, direction, player_hands, remain_cards,
                player_count)
            pop_card = None  # 낸 카드 초기화
            draw_requested = False
            new_drawn_card = None
            one_flags[0] = False
            user_uno_check = False
            uno_clicked = False
        # 내는 카드가 special이 아닌 경우
        else:
            current_player_index = (current_player_index + direction) % player_count
            pop_card = None
            draw_requested = False
            new_drawn_card = None
            one_flags[0] = False
            user_uno_check = False
            uno_clicked = False
elif not draw_requested:
    if user_turn and current_time - turn_start_time >= time_limit:
        card = remain_cards.pop()
        player_hands[current_player].append(card)  # 카드를 드로우
        pop_card = None
        draw_requested = False
        new_drawn_card = None
        current_player_index = (current_player_index + direction) % player_count
        # 턴이 넘어갈 때 turn_start_time 업데이트
        turn_start_time = pygame.time.get_ticks()
# 유저가 드로우를 하고 시간이 초과되면 턴을 그냥 넘김
elif draw_requested:
    if user_turn and current_time - user_draw_time >= time_limit:
        pop_card = None
        draw_requested = False
        new_drawn_card = None
        current_player_index = (current_player_index + direction) % player_count