import pygame
import random
from card_gen import generate_cards, generate_for_change_cards, Card, Option
from card_shuffle import shuffle_cards, distribute_cards
from game_utils import (
    draw_cards_user,
    draw_cards_ai,
    draw_change_card,
    find_hovered_card,
    find_hovered_change,
    draw_text,
    get_clicked_card,
    get_clicked_change,
    draw_button,
    get_top_card,
    draw_board_card,
    is_valid_move,
    check_uno,
    computer_playable_card,
    com_is_uno,
    apply_special_card_effects,
    card_reshuffle
)

FPS = 60

play_drawn_card_button = pygame.Rect(0, 0, 430, 110)


def game():
    pygame.init()
    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Render game elements here
        # Apply color_blind_mode if necessary

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def singleplayer(display_size, color_weakness):
    screen_width, screen_height = display_size[0], display_size[1]
    pygame.init()
    global FPS, event
    computer_action_time = None
    clock = pygame.time.Clock()

    # 플레이어 수와 각 플레이어가 받을 카드 수 지정
    player_count = 2
    card_count = 10

    # 스크린 사이즈 및 폰트
    screen = pygame.display.set_mode(display_size)
    pygame.display.set_caption("UNO Game - Single")
    font = pygame.font.Font("resources/maplestory_font.ttf", 20)
    font_big = pygame.font.Font("resources/maplestory_font.ttf", 40)

    # 배경 설정
    pygame.display.set_caption("UNO Game")
    board_background = pygame.image.load("resources/Image/background/1.jpg")  # 회색
    board_background = pygame.transform.scale(board_background, (1485, 720))
    my_deck_background = pygame.image.load("resources/Image/background/2.jpg")  # 검회색
    my_deck_background = pygame.transform.scale(my_deck_background, (1485, 360))
    player_background = pygame.image.load("resources/Image/background/3.jpg")  # 완전 검은
    player_background = pygame.transform.scale(player_background, (495, 1080))

    # 보드 설정
    card_back = pygame.image.load("resources/Image/background/5.png")  # 퍼렇
    card_back = pygame.transform.scale(card_back, (100, 150))

    # 후에 덱 클래스와 연결해야 함
    card_front = pygame.image.load("resources/Image/background/4.png")  # 초록
    card_front = pygame.transform.scale(card_front, (100, 150))
    uno_button = pygame.image.load("resources/Image/background/4.png")
    uno_button = pygame.transform.scale(uno_button, (100, 50))

    # 현재 카드 색깔을 확인해야 함
    card_color = [pygame.image.load("resources/Image/background/1.jpg"),
                  pygame.image.load("resources/Image/background/2.jpg"),
                  pygame.image.load("resources/Image/background/3.jpg"),
                  pygame.image.load("resources/Image/background/4.png")]
    for i in range(len(card_color)):
        card_color[i] = pygame.transform.scale(card_color[i], (50, 50))
    board_background.blit(card_back, (400, 300))
    board_background.blit(card_front, (700, 300))
    board_background.blit(card_color[1], (1000, 300))
    board_background.blit(uno_button, (1000, 400))

    # 플레이어 리스트 설정
    empty_player = pygame.image.load("resources/Image/background/1.jpg")
    empty_player = pygame.transform.scale(empty_player, (390, 190))

    player_name1 = font.render("Player1", True, (0, 0, 0))
    player_list1 = pygame.image.load("resources/Image/background/1.jpg")
    player_list1 = pygame.transform.scale(player_list1, (390, 190))
    player_card_back = pygame.image.load("resources/Image/background/5.png")

    player_list1.blit(player_name1, (10, 10))

    # 우측 컴퓨터 리스트
    temp = 0
    for i in range(player_count):
        player_background.blit(empty_player, (20, 20 + temp))
        temp = temp + 210

    player_background.blit(player_list1, (20, 20))

    # 내 덱 설정
    my_name = font.render("You", True, (0, 0, 0))

    my_deck_background.blit(my_name, (20, 20))

    # 덱 그리기
    screen.blit(board_background, (0, 0))
    screen.blit(my_deck_background, (0, 720))
    screen.blit(player_background, (1485, 0))
    pygame.display.flip()

    # 게임 이미지를 로드
    pause_button_img = pygame.image.load("resources/Image/button_images/pause.png").convert_alpha()
    resume_button_img = pygame.image.load("resources/Image/button_images/resume.png").convert_alpha()
    direction_img = pygame.image.load("resources/Image/direction_images/direction.png").convert_alpha()
    direction_reverse_img = pygame.image.load("resources/Image/direction_images/direction_reverse.png").convert_alpha()
    turn_arrow_img = pygame.image.load("resources/Image/direction_images/turn_arrow.png").convert_alpha()
    next_turn_button_img = pygame.image.load("resources/Image/button_images/next_turn.png").convert_alpha()
    uno_button_img = pygame.image.load("resources/Image/button_images/uno_button.png").convert_alpha()
    uno_button_inactive_img = pygame.image.load("resources/Image/button_images/uno_button_inactive.png").convert_alpha()

    # 이미지 크기 계산, 화면 크기 계싼
    screen = pygame.display.set_mode(display_size)
    image_width, image_height = direction_img.get_size()

    # 화면 중앙 좌표 계산
    center_x = (screen_width - image_width) // 2
    center_y = (screen_height - image_height) // 2

    # 색약 모드 설정
    option = Option(False)  # False: 일반 모드, True: 색약 모드

    # 카드 생성 및 셔플
    cards = generate_cards(color_weakness)
    shuffled_cards = shuffle_cards(cards)

    # 카드 분배, 유저는 player_hands[0]이고, 나머지는 인공지능으로 설정한다. change는 카드 체인지를 위한 카드들.
    player_hands, remain_cards = distribute_cards(shuffled_cards, player_count, card_count)
    change = generate_for_change_cards(color_weakness)

    # 플레이어 순서 결정
    player_order = list(range(player_count))
    # 초기 플레이어 순서를 위한 설정 값.
    current_player_index = (random.randint(0, len(player_order) - 1))
    # 플레이어 순서 (1: 정방향, -1: 역방향)
    direction = 1

    # 보드에 뒤집힌 카드 설정 (카드 한 장을 뽑아서 남은 카드 덱 옆에 보이게 놓기)
    board_card = [remain_cards.pop()]
    print(remain_cards)

    # 게임 루프
    running = True

    # 카드 약간 띄우는 초기값 index는 플레이어, index2는 ai,
    hovered_card_index = None
    hovered_card_index2 = None
    hovered_change_index = None

    # 각 카드들의 위치 설정, (x, y, spacing)는 유저의 카드, (x2, y2, spacing2, max_per_row)는 AI의 카드 위치를 잡는다.
    x = screen_width/10
    y = screen_height * 0.8
    spacing = screen_height * 0.08
    x2 = screen_width * 0.72
    y2 = screen_height * 0.08
    spacing2 = screen_height * 0.04
    max_per_row = 7
    # turn_arrow_img의 위치를 계산. (x3, y3)는 유저 좌표, (x4, y4, spacing4)는 AI의 좌표
    x3 = screen_width/10 - 150
    y3 = screen_height * 0.8 - 100
    x4 = screen_width * 0.63
    y4 = screen_height * 0.07 - 100
    spacing4 = screen_height * 0.2
    # change카드 좌표, spacing은 공백
    x5 = 100
    y5 = 100
    spacing5 = 200
    # 플레이어들이 카드를 뽑고 남은 카드들의 위치를 잡는데 사용
    remain_cards_x_position = (screen.get_rect().centerx - 100)
    remain_cards_y_position = (screen.get_rect().centery - 50)
    # remain카드
    remain_cards_rect = remain_cards[0].card_img_back.get_rect()
    remain_cards_rect.topleft = (remain_cards_x_position, remain_cards_y_position)
    # pause버튼
    pause_button_rect = pause_button_img.get_rect()
    pause_button_rect.topleft = (25, 25)
    # next_turn버튼
    next_turn_button_rect = next_turn_button_img.get_rect()
    next_turn_button_rect.topleft = (x, y - 150)
    # uno_button
    uno_button_rect = uno_button_img.get_rect()
    uno_button_rect.topleft = (150, screen_height * 0.5)
    uno_button_inactive_rect = uno_button_inactive_img.get_rect()
    uno_button_inactive_rect.topleft = (150, screen_height * 0.5)
    # 일시정지 초기값
    paused = False
    # 게임 위너 메시지
    winner_message = ""
    # 게임 오버 초기값
    game_over = False
    # 리스타트 초기값
    restart_game = False
    # 전에 유저 턴이었는지 확인하는 초기값
    prev_user_turn = False
    # 유저가 draw 했는지 확인하는 초기값
    draw_requested = False
    # 컴퓨터가 draw 했는지 확인하는 초기값
    com_draw_requested = False
    # draw한 카드가 어떤 카드인가의 초기값
    new_drawn_card = None
    # 컴퓨터가 뽑은 카드 초기값
    com_pop_card = None
    # 유저가 뽑은 카드 초기값
    pop_card = None
    # 유저 우노 체크
    user_uno_check = False
    clicked_card = None
    clicked_remain_cards = False
    clicked_next_turn_button = False
    # uno 초기값
    uno_click_time = None
    user_uno_clicked = False
    computer_uno_clicked = False
    com_drawn_card = None
    com_uno_check = False
    one_flags = [False, False, False, False, False, False]
    change_card = False
    com_change_card = False
    clicked_change_index = None
    com_change_index = None

    # 턴 카운트
    turn_count = 0

    # 10초 제한 설정
    time_limit = 10000
    # 현재 시간 저장
    turn_start_time = pygame.time.get_ticks()

    while running:
        # 마우스의 위치를 가져옴
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # 현재 플레이어 결정
        current_player = player_order[current_player_index]

        # 현재 플레이어가 유저인지 확인
        user_turn = (current_player == 0)
        if user_turn and not prev_user_turn:
            turn_start_time = pygame.time.get_ticks()  # 현재 시간 저장
            pop_card = None  # 카드를 냈는지 확인
        # 유저 턴 여부를 prev_user_turn에 저장
        prev_user_turn = user_turn
        # 게임 승리조건 불만족일 경우
        if not game_over:
            screen.fill((111, 111, 111))  # 화면
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button_rect.collidepoint(mouse_x, mouse_y):
                        paused = not paused
                    if uno_button_rect.collidepoint(mouse_x, mouse_y) and len(player_hands[current_player]) == 1:
                        user_uno_clicked = True
                        uno_click_time = pygame.time.get_ticks()
                        print('우노클릭발생')
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                elif event.type == pygame.QUIT:
                    running = False
            # 퍼즈가 아닐 경우
            if not paused:
                current_time = pygame.time.get_ticks()
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
                        # change 클릭 확인
                        clicked_change_index, clicked_change = get_clicked_change(change, x5, y5, spacing5, mouse_x,
                                                                                  mouse_y)
                    if clicked_change_index is not None:
                        print(clicked_change_index)

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
                            clicked_card = None
                            clicked_remain_cards = False
                            clicked_next_turn_button = False
                            user_uno_clicked = False
                            turn_count += 1
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
                                user_uno_clicked = False
                        # 카드를 드로우하지 않고, 카드를 냄
                        elif not draw_requested and pop_card is None:
                            top_card = get_top_card(board_card)
                            # 유효성 검사
                            if clicked_card is not None and is_valid_move(clicked_card, top_card):
                                board_card.append(clicked_card)
                                player_hands[0].pop(clicked_card_index)
                                pop_card = clicked_card
                                user_uno_check = check_uno(player_hands[0])
                                if user_uno_check:
                                    one_flags[0] = True
                                    uno_current_time = pygame.time.get_ticks()
                                    uno_delay_time = random.randint(2000, 3000)
                                    print("check!", uno_current_time, uno_delay_time)
                                    user_uno_clicked = False
                    # 카드를 냈을 때,
                    if pop_card is not None:
                        # 우노일 경우
                        if user_uno_check:
                            uno_clicked = True
                            if user_uno_clicked:
                                one_flags[0] = False
                                uno_clicked = False
                                # 내는 카드가 special인 경우
                                if pop_card.is_special() and pop_card.value != "change":
                                    current_player_index, direction = apply_special_card_effects(pop_card, current_player_index,
                                                                   current_player, direction, player_hands,
                                                                   remain_cards, player_count)
                                    pop_card = None  # 낸 카드 초기화
                                    draw_requested = False
                                    new_drawn_card = None
                                    user_uno_check = False
                                    user_uno_clicked = False
                                    clicked_card = None
                                    clicked_remain_cards = False
                                    clicked_next_turn_button = False
                                    turn_count += 1
                                elif pop_card.is_special() and pop_card.value == "change":
                                    change_card = True
                                    if clicked_change_index is not None:
                                        color_change = change[clicked_change_index]
                                        current_player_index, direction = apply_special_card_effects(
                                            pop_card, current_player_index, current_player, direction, player_hands,
                                            remain_cards, player_count)
                                        board_card.append(color_change)
                                        pop_card = None  # 낸 카드 초기화
                                        draw_requested = False
                                        new_drawn_card = None
                                        user_uno_check = False
                                        user_uno_clicked = False
                                        clicked_card = None
                                        clicked_remain_cards = False
                                        clicked_next_turn_button = False
                                        clicked_change_index = None
                                        change_card = False
                                        turn_count += 1
                                # 내는 카드가 special이 아닌 경우
                                elif not pop_card.is_special():
                                    current_player_index = (current_player_index + direction) % player_count
                                    pop_card = None  # 낸 카드 초기화
                                    draw_requested = False
                                    new_drawn_card = None
                                    user_uno_check = False  # 낸 카드 초기화
                                    user_uno_clicked = False
                                    clicked_card = None
                                    clicked_remain_cards = False
                                    clicked_next_turn_button = False
                                    clicked_change_index = None
                                    turn_count += 1
                        else:
                            # 내는 카드가 special이고 change가 아닐 때,
                            if pop_card.is_special() and pop_card.value != "change":
                                current_player_index, direction = apply_special_card_effects(pop_card,
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
                                user_uno_clicked = False
                                clicked_card = None
                                clicked_remain_cards = False
                                clicked_next_turn_button = False
                                turn_count += 1
                            # 내는 카드가 special이고, change인 경우
                            elif pop_card.is_special() and pop_card.value == "change":
                                change_card = True
                                if clicked_change_index is not None:
                                    color_change = change[clicked_change_index]
                                    current_player_index, direction = apply_special_card_effects(pop_card, current_player_index, current_player, direction, player_hands, remain_cards, player_count)
                                    board_card.append(color_change)
                                    pop_card = None  # 낸 카드 초기화
                                    draw_requested = False
                                    new_drawn_card = None
                                    user_uno_check = False
                                    user_uno_clicked = False
                                    clicked_card = None
                                    clicked_remain_cards = False
                                    clicked_next_turn_button = False
                                    clicked_change_index = None
                                    change_card = False
                                    turn_count += 1
                            # 내는 카드가 special이 아닌 경우
                            else:
                                current_player_index = (current_player_index + direction) % player_count
                                pop_card = None
                                draw_requested = False
                                new_drawn_card = None
                                user_uno_check = False
                                user_uno_clicked = False
                                clicked_card = None
                                clicked_remain_cards = False
                                clicked_next_turn_button = False
                                turn_count += 1

                # 우노 시간 넘기면 발동
                if pop_card is not None and one_flags[0] and user_turn:
                    if current_time - uno_current_time >= uno_delay_time:
                        uno_drawn_card = remain_cards.pop()
                        player_hands[0].append(uno_drawn_card)
                        # 내는 카드가 special이고, change가 아닐 경우
                        if pop_card.is_special() and pop_card.value == "change":
                            print("popcard가 체인지이고 제한시간 넘김")
                            current_player_index, direction = apply_special_card_effects(
                                pop_card, current_player_index, current_player, direction, player_hands, remain_cards,
                                player_count)
                            pop_card = None  # 낸 카드 초기화
                            draw_requested = False
                            new_drawn_card = None
                            one_flags[0] = False
                            user_uno_check = False
                            user_uno_clicked = False
                            clicked_card = None
                            clicked_remain_cards = False
                            clicked_next_turn_button = False
                            change_card = False
                            turn_count += 1
                            turn_count += 1
                        elif pop_card.is_special() and pop_card.value != "change":
                            print("popcard가 체인지아니고 제한시간 넘김")
                            current_player_index, direction = apply_special_card_effects(
                                pop_card, current_player_index, current_player, direction, player_hands, remain_cards,
                                player_count)
                            pop_card = None  # 낸 카드 초기화
                            draw_requested = False
                            new_drawn_card = None
                            one_flags[0] = False
                            user_uno_check = False
                            user_uno_clicked = False
                            clicked_card = None
                            clicked_remain_cards = False
                            clicked_next_turn_button = False
                            change_card = False
                            turn_count += 1
                        # 내는 카드가 special이 아닌 경우
                        elif not pop_card.is_special():
                            current_player_index = (current_player_index + direction) % player_count
                            pop_card = None
                            draw_requested = False
                            new_drawn_card = None
                            one_flags[0] = False
                            user_uno_check = False
                            user_uno_clicked = False
                            clicked_card = None
                            clicked_remain_cards = False
                            clicked_next_turn_button = False
                            change_card = False
                            turn_count += 1
                # 유저의 턴일 때 시간이 초과되면 드로우하고 턴을 넘김
                elif not draw_requested:
                    if user_turn and current_time - turn_start_time >= time_limit:
                        card = remain_cards.pop()
                        player_hands[current_player].append(card)  # 카드를 드로우
                        pop_card = None
                        draw_requested = False
                        new_drawn_card = None
                        clicked_card = None
                        clicked_remain_cards = False
                        clicked_next_turn_button = False
                        change_card = False
                        user_uno_clicked = False
                        turn_count += 1
                        current_player_index = (current_player_index + direction) % player_count
                        # 턴이 넘어갈 때 turn_start_time 업데이트
                        turn_start_time = pygame.time.get_ticks()
                # 유저가 드로우를 하고 시간이 초과되면 턴을 그냥 넘김
                elif draw_requested:
                    if user_turn and current_time - user_draw_time >= time_limit:
                        pop_card = None
                        draw_requested = False
                        new_drawn_card = None
                        clicked_card = None
                        clicked_remain_cards = False
                        clicked_next_turn_button = False
                        change_card = False
                        user_uno_clicked = False
                        turn_count += 1
                        current_player_index = (current_player_index + direction) % player_count

                # 컴퓨터 턴 처리
                if not user_turn:
                    if computer_action_time is None:
                        turn_start_time = pygame.time.get_ticks()
                        delay_time = random.randint(1000, 2000)  # 랜덤한 시간 생성
                        delay_time2 = delay_time + random.randint(900, 2000)  # 랜덤한 시간 생성
                        delay_time3 = delay_time2 + random.randint(900, 2000)
                        computer_action_time = pygame.time.get_ticks() + delay_time  # 현재 시간에 랜덤한 지연 시간을 더함
                        print(turn_start_time, computer_action_time)
                    if current_time >= computer_action_time:  # 설정한 시간이 되면 컴퓨터가 행동함
                        if 1 <= current_player <= 5:
                            # 처음 유효성 검사
                            if not com_draw_requested and com_pop_card is None:
                                playable, com_pop_card_index = computer_playable_card(player_hands[current_player],
                                                                                      board_card)
                            # 카드를 낼 수 있을 때,
                            if playable and not com_draw_requested and com_pop_card is None:
                                print("컴퓨터 카드 낼 수 있을 때")
                                com_pop_card = player_hands[current_player][com_pop_card_index]
                                player_hands[current_player].pop(com_pop_card_index)
                                board_card.append(com_pop_card)
                                com_uno_check = check_uno(player_hands[current_player])
                                if com_uno_check:
                                    one_flags, uno_current_time, uno_delay_time = com_is_uno(one_flags, current_player)
                            # 카드를 낼 수 없을 때 드로우 한다.
                            elif not playable and not com_draw_requested and com_pop_card is None:
                                print("카드를 낼 수 없을 때")
                                com_draw_requested = True
                                com_drawn_card = remain_cards.pop()
                                player_hands[current_player].append(com_drawn_card)
                            # 드로우한 카드가 낼 수 있는 경우
                            elif com_draw_requested and is_valid_move(com_drawn_card, top_card) and com_pop_card is None:
                                print("드로우한 카드를 낼 수 있을 때")
                                print(turn_start_time, current_time)
                                if current_time - turn_start_time >= delay_time2:
                                    com_pop_card = com_drawn_card
                                    com_pop_card_index = player_hands[current_player].index(com_pop_card)
                                    player_hands[current_player].pop(com_pop_card_index)
                                    board_card.append(com_pop_card)
                                    com_uno_check = check_uno(player_hands[current_player])
                                    if com_uno_check:
                                        one_flags, uno_current_time, uno_delay_time = com_is_uno(one_flags, current_player)
                            # 드로우한 카드를 낼 수 없는 경우
                            elif com_draw_requested and not is_valid_move(com_drawn_card, top_card) and com_pop_card is None:
                                print("드로우한 카드를 낼 수 없는 경우")
                                if current_time - turn_start_time >= delay_time2:
                                    current_player_index = (current_player_index + direction) % player_count
                                    com_pop_card = None  # 컴퓨터가 낸 카드 초기화
                                    com_draw_requested = False
                                    com_drawn_card = None
                                    com_uno_check = False
                                    computer_action_time = None
                                    turn_count += 1
                            # 컴퓨터가 우노이고, 유저가 우노를 클릭했을 경우
                            elif user_uno_clicked:
                                if com_uno_check and com_pop_card is not None:
                                    uno_clicked = True
                                    print("우노체크. 유저우노클릭")
                                    one_flags[current_player] = False
                                    print('플래그 false')
                                    uno_clicked = False
                                    com_uno_drawn_card = remain_cards.pop()
                                    print("카드 뽑기")
                                    player_hands[current_player].append(com_uno_drawn_card)
                                    # 컴퓨터가 낸 카드가 special일 경우
                                    if com_pop_card.is_special():
                                        current_player_index, direction = apply_special_card_effects(com_pop_card,
                                                                                                     current_player_index,
                                                                       current_player, direction, player_hands,
                                                                       remain_cards, player_count)
                                        com_pop_card = None  # 컴퓨터가 낸 카드 초기화
                                        com_draw_requested = False
                                        com_drawn_card = None
                                        com_uno_check = False
                                        computer_action_time = None
                                        user_uno_clicked = False
                                        turn_count += 1
                                    # 컴퓨터가 낸 카드가 special이 아닌 경우
                                    elif not com_pop_card.is_special():
                                        current_player_index = (current_player_index + direction) % player_count
                                        com_pop_card = None  # 컴퓨터가 낸 카드 초기화
                                        com_draw_requested = False
                                        com_drawn_card = None
                                        com_uno_check = False
                                        computer_action_time = None
                                        user_uno_clicked = False
                                        turn_count += 1
                            # 컴퓨터가 우노가 아니고, 컴퓨터가 카드를 낸 경우
                            elif not com_uno_check and com_pop_card is not None:
                                #내는 카드가 special이고 change가 아닐 경우
                                if com_pop_card.is_special() and com_pop_card.value != "change":
                                    current_player_index, direction = apply_special_card_effects(com_pop_card, current_player_index, current_player, direction, player_hands,
                                        remain_cards, player_count)
                                    com_pop_card = None  # 컴퓨터가 낸 카드 초기화
                                    com_draw_requested = False
                                    com_drawn_card = None
                                    com_uno_check = False
                                    computer_action_time = None
                                    turn_count += 1
                                #내는 카드가 special이고, change일 경우
                                elif com_pop_card.is_special() and com_pop_card.value == "change":
                                    if current_time - turn_start_time >= delay_time3:
                                        print("우노가 아닌 컴퓨터 change발생")
                                        com_change_index = random.randint(0, 3)
                                        color_change = change[com_change_index]
                                        current_player_index, direction = apply_special_card_effects(com_pop_card,
                                                                                                     current_player_index,
                                                                                                     current_player,
                                                                                                     direction,
                                                                                                     player_hands,
                                                                                                     remain_cards,
                                                                                                     player_count)
                                        board_card.append(color_change)
                                        com_pop_card = None  # 컴퓨터가 낸 카드 초기화
                                        com_draw_requested = False
                                        com_drawn_card = None
                                        com_uno_check = False
                                        computer_action_time = None
                                        com_change_index = None
                                        turn_count += 1
                                # 내는 카드가 special이 아닌 경우
                                elif not com_pop_card.is_special():
                                    current_player_index = (current_player_index + direction) % player_count
                                    com_pop_card = None  # 컴퓨터가 낸 카드 초기화
                                    com_draw_requested = False
                                    com_drawn_card = None
                                    com_uno_check = False
                                    computer_action_time = None
                                    turn_count += 1

                # 컴퓨터의 턴일 때 시간이 초과되면 우노를 넘긴다.
                if com_pop_card is not None and any(one_flags[1:]) and not user_turn:
                    if current_time - uno_current_time >= uno_delay_time:
                        one_flags[current_player_index] = False
                        # 내는 카드가 special이고, change가 아닐 경우
                        if com_pop_card.is_special() and com_pop_card.value != "change":
                            current_player_index, direction = apply_special_card_effects(
                                com_pop_card, current_player_index, current_player, direction, player_hands,
                                remain_cards,
                                player_count)
                            com_pop_card = None  # 컴퓨터가 낸 카드 초기화
                            com_draw_requested = False
                            com_drawn_card = None
                            com_uno_check = False
                            turn_count += 1
                        # 내는 카드가 special이고 change인 경우
                        elif com_pop_card.is_special() and com_pop_card.value == "change":
                            com_change_index = random.randint(0, 3)
                            color_change = change[com_change_index]
                            if current_time - turn_start_time >= delay_time3:
                                current_player_index, direction = apply_special_card_effects(
                                    com_pop_card, current_player_index, current_player, direction, player_hands,
                                    remain_cards,
                                    player_count)
                                board_card.append(color_change)
                                com_pop_card = None  # 컴퓨터가 낸 카드 초기화
                                com_draw_requested = False
                                com_drawn_card = None
                                com_uno_check = False
                                com_change_index = None
                                turn_count += 1
                        # 내는 카드가 special이 아닌 경우
                        elif not com_pop_card.is_special():
                            current_player_index = (current_player_index + direction) % player_count
                            com_pop_card = None  # 컴퓨터가 낸 카드 초기화
                            com_draw_requested = False
                            com_drawn_card = None
                            com_uno_check = False
                            turn_count += 1

            # 게임 진행을 위해 board_card에서 카드를 추출 후, remain_cards에 넣고 섞음
            if turn_count == 10:
                print('카드 섞기 발생')
                board_card, remain_cards = card_reshuffle(board_card, remain_cards)
                turn_count = 0

            # direction 그리기
            if direction == 1:
                screen.blit(direction_img, (center_x, center_y))
            elif direction == -1:
                screen.blit(direction_reverse_img, (center_x, center_y))
            # 누구 턴인지 표시하는 화살표 그리기
            if user_turn:
                screen.blit(turn_arrow_img, (x3, y3))
            else:
                screen.blit(turn_arrow_img, (x4, y4 + spacing4 * (current_player - 1)))

            # 유저턴일때 표시될 사항. (시간제한, 턴 넘기기 버튼)
            if user_turn and not draw_requested and not one_flags[0]:
                remaining_time = time_limit - (current_time - turn_start_time)
                remaining_time_text = f"a남은 시간: {remaining_time // 1000}초"
                draw_text(screen, remaining_time_text, font, (255, 255, 255), screen.get_rect().centerx, 30)
            # draw후 시간제한,턴 넘기기는 draw를 해야지 나옴.
            elif user_turn and draw_requested and not one_flags[0]:
                after_draw_remaining_time = time_limit - (current_time - user_draw_time)
                after_draw_remaining_time_text = f"b남은 시간: {after_draw_remaining_time // 1000}초"
                draw_text(screen, after_draw_remaining_time_text, font, (255, 255, 255), screen.get_rect().centerx, 30)
                # 턴 넘기기는 버튼
                screen.blit(next_turn_button_img, next_turn_button_rect)
            # uno버튼 시간
            elif user_turn and one_flags[0]:
                uno_remaining_time = uno_delay_time - (current_time - uno_current_time)
                uno_remaining_time_text = f"c남은 시간: {uno_remaining_time // 1000}초"
                draw_text(screen, uno_remaining_time_text, font, (255, 255, 255), screen.get_rect().centerx, 30)
            elif not user_turn and any(one_flags[1:]):
                com_uno_remaining_time = uno_delay_time - (current_time - uno_current_time)
                com_uno_remaining_time_text = f"d남은 시간: {com_uno_remaining_time // 1000}초"
                draw_text(screen, com_uno_remaining_time_text, font, (255, 255, 255), screen.get_rect().centerx, 30)

            # 유저 카드에 마우스 대면 위로 작동, 퍼즈일때는 작동 안함
            if not paused:
                hovered_card_index = find_hovered_card(player_hands[0], x, y, spacing, mouse_x, mouse_y)
                hovered_change_index = find_hovered_change(change, x5, y5, spacing5, mouse_x, mouse_y)

            draw_cards_user(screen, player_hands[0], x, y, spacing, hovered_card_index)  # 플레이어의 카드를 그린다.
            if user_turn and change_card:
                draw_change_card(screen, change, x5, y5, spacing5, hovered_change_index)  # 체인지 카드 그림

            for i in range(len(player_hands) - 1):  # ai의 카드를 그린다.
                draw_cards_ai(screen, player_hands[i + 1], x2, y2 + (i * spacing4), max_per_row, spacing2, hovered_card_index2,
                              show_back=False)  # 추후 True로 바꾼다.

            # 남은 카드 더미 그리기
            screen.blit(remain_cards[0].card_img_back, (remain_cards_x_position, remain_cards_y_position))
            # 엎은 카드 그리기
            draw_board_card(screen, board_card[-1], screen.get_rect().centerx, screen.get_rect().centery)

            # 드로우 요청 시 버튼 표시
            if draw_requested and is_valid_move(new_drawn_card, top_card):
                play_drawn_card_button.topleft = (screen.get_rect().centerx + 100, screen.get_rect().centery)
                draw_button(screen, "Click NEXT TURN button to turn.\n Or If you want to submit a drawn card,"
                                    "\nclick on the drawn card.", font, (255, 255, 255), play_drawn_card_button)
            elif draw_requested and not is_valid_move(new_drawn_card, top_card):
                play_drawn_card_button.topleft = (screen.get_rect().centerx + 100, screen.get_rect().centery)
                draw_button(screen, "Click NEXT TURN button to turn.", font, (255, 255, 255),
                            play_drawn_card_button)

            # 우노 버튼 표시
            if any(one_flags):
                screen.blit(uno_button_img, uno_button_rect)
            else:
                screen.blit(uno_button_inactive_img, uno_button_inactive_rect)

            # 퍼즈버튼 그리기(그리는 이미지, 작동되는 함수)
            if not paused:
                screen.blit(pause_button_img, pause_button_rect)
            else:
                screen.blit(resume_button_img, pause_button_rect)

            if len(player_hands[0]) == 0:
                winner_message = "User Wins!"
                game_over = True
            elif any(len(player_hand) == 0 for player_hand in player_hands[1:]):
                winner_message = "Computer wins!"
                game_over = True

            pygame.display.flip()
            clock.tick(FPS)  # FPS를 조절하여 루프 속도를 제한한다.

        # 게임이 끝났을 때,
        elif game_over:
            # 게임 오버 화면 표시
            screen.fill((0, 0, 0))
            draw_text(screen, winner_message, font_big, (255, 255, 255), screen.get_rect().centerx, 100)
            draw_text(screen, "Press 'r' to restart or 'e' to exit", font_big, (255, 255, 255),
                      screen.get_rect().centerx, 300)
            pygame.display.flip()

            # 사용자가 키를 누를 때까지 기다림
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # 게임을 다시 시작
                        restart_game = True
                        break
                    elif event.key == pygame.K_e:
                        break
                elif event.type == pygame.QUIT:
                    break

            # 파이게임 종료 여부 결정
            if restart_game:
                singleplayer()
                return
            elif not restart_game:
                return False


if __name__ == "__main__":
    quit_game = singleplayer()
    if not quit_game:
        pygame.quit()
