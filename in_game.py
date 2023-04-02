import pygame
import random
from card_gen import generate_cards, Card, Option
from card_shuffle import shuffle_cards, distribute_cards
from game_utils import (
    draw_cards_user,
    draw_cards_ai,
    find_hovered_card,
    draw_text,
    get_clicked_card,
    draw_button,
    get_top_card,
    draw_top_card,
    is_valid_move,
    computer_turn,
    apply_special_card_effects
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


def singleplayer():
    pygame.init()
    global FPS, event
    computer_action_time = None
    clock = pygame.time.Clock()

    # 플레이어 수와 각 플레이어가 받을 카드 수 지정
    player_count = 3
    card_count = 7

    # 스크린 사이즈 및 폰트
    screen = pygame.display.set_mode((1800, 1000))
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

    # 색약 모드 설정
    option = Option(False)  # False: 일반 모드, True: 색약 모드

    # 카드 생성 및 셔플
    cards = generate_cards()
    shuffled_cards = shuffle_cards(cards)

    # 카드 분배, 유저는 player_hands[0]이고, 나머지는 인공지능으로 설정한다.
    player_hands, remain_cards = distribute_cards(shuffled_cards, player_count, card_count)
    print(player_hands)
    # 플레이어 순서 결정
    player_order = list(range(player_count))
    # random.shuffle(player_order) (추후 필요하면 on)
    current_player_index = 0  # 초기 플레이어 순서를 위한 설정 값.
    direction = 1  # 플레이어 순서 (1: 정방향, -1: 역방향)

    # 보드에 뒤집힌 카드 설정 (카드 한 장을 뽑아서 남은 카드 덱 옆에 보이게 놓기)
    board_card = [remain_cards.pop()]
    print(board_card)

    # 게임 루프
    running = True

    # 카드 약간 띄우는 초기값 index는 플레이어, index2는 ai
    hovered_card_index = None
    hovered_card_index2 = None

    # 각 카드들의 위치 설정, (x, y, spacing)는 유저의 카드, (x2, y2, spacing2, max_per_row)는 AI의 카드 위치를 잡는다.
    x = 150
    y = 800
    spacing = 80
    x2 = 1300
    y2 = 80
    spacing2 = 40
    max_per_row = 7

    # 플레이어들이 카드를 뽑고 남은 카드들의 위치를 잡는데 사용
    remain_cards_x_position = screen.get_rect().centerx - 100
    remain_cards_y_position = screen.get_rect().centery - 50

    prev_user_turn = False
    draw_requested = False
    new_drawn_card = None
    # remain카드
    remain_cards_rect = remain_cards[0].card_img_back.get_rect()
    remain_cards_rect.topleft = (remain_cards_x_position, remain_cards_y_position)
    # pause버튼
    pause_button_rect = pause_button_img.get_rect()
    pause_button_rect.topleft = (100, 100)
    # 일시정지 초기값
    paused = False
    # 10초 제한 설정
    time_limit = 10000
    # 현재 시간 저장
    turn_start_time = pygame.time.get_ticks()

    while running:
        screen.fill((111, 111, 111))  # 화면 초기화

        # 현재 플레이어 결정
        current_player = player_order[current_player_index]

        # 현재 플레이어가 유저인지 확인
        user_turn = (current_player == 0)

        if user_turn and not prev_user_turn:
            turn_start_time = pygame.time.get_ticks()  # 현재 시간 저장
        # 유저 턴 여부를 prev_user_turn에 저장
        prev_user_turn = user_turn

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(mouse_x, mouse_y):
                    paused = not paused
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        # 퍼즈가 아닐 경우
        if not paused:
            # 유저의 턴일 경우
            if user_turn:
                if event.type == pygame.MOUSEBUTTONDOWN and user_turn:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    clicked_card_index, clicked_card = get_clicked_card(player_hands[0], x, y, spacing, mouse_x,
                                                                        mouse_y)
                    # remain_cards 클릭 확인
                    if clicked_card is None:
                        remain_cards_rect = remain_cards[0].card_img_back.get_rect()
                        remain_cards_rect.topleft = (screen.get_rect().centerx, screen.get_rect().centery)
                        clicked_remain_cards = remain_cards_rect.collidepoint(mouse_x, mouse_y)
                    else:
                        clicked_remain_cards = False

                    # 클릭된 카드가 실제로 존재하는지 확인하는 조건문. 클릭된 카드가 존재하면 내부 코드 실행
                    if clicked_card is not None or clicked_remain_cards:
                        top_card = get_top_card(board_card)
                        # 카드를 드로우함
                        user_draw_time = pygame.time.get_ticks()
                        if clicked_remain_cards and not draw_requested:
                            player_hands[0].append(remain_cards.pop())
                            new_drawn_card = player_hands[0][-1]
                            draw_requested = True
                            print(player_hands[0])
                            print("카드 드로우 성공")
                        # 카드를 드로우 하고, 드로우한 카드를 내는 함수.
                        elif draw_requested and new_drawn_card is not None and not clicked_remain_cards:
                            if is_valid_move(new_drawn_card, top_card) and clicked_card == new_drawn_card:
                                board_card.append(clicked_card)
                                player_hands[0].pop(clicked_card_index)
                                print("드로우한 카드를 냄")
                                # 내는 카드가 special인 경우
                                if clicked_card.is_special():
                                    current_player_index, direction = apply_special_card_effects(clicked_card,
                                                                                                 current_player_index,
                                                                                                 current_player,
                                                                                                 direction,
                                                                                                 player_hands,
                                                                                                 remain_cards,
                                                                                                 player_count)
                                    draw_requested = False
                                    new_drawn_card = None
                                    print("드로우한 스페셜카드 처리 성공")
                                # 내는 카드가 special이 아닌 경우
                                elif not clicked_card.is_special():
                                    current_player_index = (current_player_index + direction) % player_count
                                    draw_requested = False
                                    new_drawn_card = None
                                    print("스페셜 아닌 드로우한 카드 처리 성공")
                            # 카드를 드로우 하고 턴을 넘기는 함수.
                            elif draw_requested and new_drawn_card is not None and clicked_remain_cards:
                                current_player_index = (current_player_index + direction) % player_count
                                draw_requested = False
                                new_drawn_card = None
                                print("카드 드로우만 하고 턴 넘기기 성공")
                        # 드로우를 하지 않고 유저 덱에서 카드를 낼 경우.
                        elif not draw_requested:
                            top_card = get_top_card(board_card)
                            # 유효성 검사
                            if clicked_card is not None and is_valid_move(clicked_card, top_card):
                                board_card.append(clicked_card)
                                player_hands[0].pop(clicked_card_index)
                                # 내는 카드가 special인 경우
                                if clicked_card.is_special():
                                    current_player_index, direction = apply_special_card_effects(clicked_card,
                                                                                                 current_player_index,
                                                                                                 current_player,
                                                                                                 direction,
                                                                                                 player_hands,
                                                                                                 remain_cards,
                                                                                                 player_count)
                                # 내는 카드가 special이 아닌 경우
                                elif not clicked_card.is_special():
                                    # 턴을 넘김
                                    current_player_index = (current_player_index + direction) % player_count
            current_time = pygame.time.get_ticks()

            # 유저의 턴일 때 시간이 초과되면 드로우하고 턴을 넘김
            if not draw_requested:
                if user_turn and current_time - turn_start_time >= time_limit:
                    card = remain_cards.pop()
                    player_hands[current_player].append(card)  # 카드를 드로우
                    draw_requested = False
                    new_drawn_card = None
                    current_player_index = (current_player_index + direction) % player_count
                    # 턴이 넘어갈 때 turn_start_time 업데이트
                    turn_start_time = pygame.time.get_ticks()
            # 유저가 드로우를 하고 시간이 초과되면 턴을 그냥 넘김
            elif draw_requested:
                if user_turn and current_time - user_draw_time >= time_limit:
                    draw_requested = False
                    new_drawn_card = None
                    current_player_index = (current_player_index + direction) % player_count

            # 컴퓨터 턴 처리
            if not user_turn and not paused:
                if computer_action_time is None:
                    turn_start_time = pygame.time.get_ticks()
                    delay_time = random.randint(1000, 3000)  # 1~3초 사이의 랜덤한 시간 생성
                    delay_time2 = random.randint(1000, 2000)  # 1~2초 사이의 랜덤한 시간 생성
                    computer_action_time = pygame.time.get_ticks() + delay_time  # 현재 시간에 랜덤한 지연 시간을 더함

                if pygame.time.get_ticks() >= computer_action_time:  # 설정한 시간이 되면 컴퓨터가 행동함
                    if 1 <= current_player <= 5:
                        current_player_index, direction = computer_turn(player_hands[current_player],
                                                                        current_player_index, current_player,
                                                                        board_card, remain_cards, player_count,
                                                                        direction, player_hands, delay_time2)
                    computer_action_time = None  # 행동을 완료한 후, 다음 행동 시간을 초기화 함.

        # 게임 진행을 위해 board_card에서 카드를 추출 후, remain_cards에 넣고 섞음
        if len(remain_cards) < 10:
            print('카드 섞기 발생')
            top_card = board_card[-1]
            board_card = board_card[:-1]  # top_card를 제외한 나머지 카드를 가져옵니다.

            remain_cards.extend(board_card)  # 가져온 카드를 remain_cards에 추가합니다.
            board_card = [top_card]  # board_card를 top_card만 남겨둡니다.

            shuffle_cards(remain_cards)  # remain_cards를 무작위로 섞습니다.

        mouse_x, mouse_y = pygame.mouse.get_pos()  # 마우스의 위치를 가져옴
        hovered_card_index = find_hovered_card(player_hands[0], x, y, spacing, mouse_x, mouse_y)

        draw_cards_user(screen, player_hands[0], x, y, spacing, hovered_card_index)  # 플레이어의 카드를 그린다.

        for i in range(len(player_hands) - 1):  # ai의 카드를 그린다.
            draw_cards_ai(screen, player_hands[i + 1], x2, y2 + (i * 200), max_per_row, spacing2, hovered_card_index2,
                          show_back=False)  # 추후 True로 바꾼다.

        # 남은 카드 더미 그리기
        if remain_cards:
            screen.blit(remain_cards[0].card_img_back, (screen.get_rect().centerx, screen.get_rect().centery))

        top_card = get_top_card(board_card)
        draw_top_card(screen, top_card, remain_cards_x_position, remain_cards_y_position)

        # 드로우 요청 시 버튼 표시
        if draw_requested and is_valid_move(new_drawn_card, top_card):
            play_drawn_card_button.topleft = (screen.get_rect().centerx + 100, screen.get_rect().centery)
            draw_button(screen, "Click on the remaining deck to turn.\n Or If you want to submit a drawn card,"
                                "\nclick on the drawn card.", font, (255, 255, 255), play_drawn_card_button)
        elif draw_requested and not is_valid_move(new_drawn_card, top_card):
            play_drawn_card_button.topleft = (screen.get_rect().centerx + 100, screen.get_rect().centery)
            draw_button(screen, "Click on the remaining deck to turn.", font, (255, 255, 255),
                        play_drawn_card_button)

        # 퍼즈버튼 그리기(그리는 이미지, 작동되는 함수)
        if not paused:
            screen.blit(pause_button_img, pause_button_rect)
        else:
            screen.blit(resume_button_img, pause_button_rect)

        # 게임 종료 조건 확인 및 메시지 출력
        if len(player_hands[0]) == 0:
            draw_text(screen, "user wins!", font_big, (255, 255, 255), screen.get_rect().centerx, 100)
            pygame.time.delay(3000)
            running = False
        elif any(len(player_hand) == 0 for player_hand in player_hands[1:]):
            draw_text(screen, "Computer wins!", font_big, (255, 255, 255), screen.get_rect().centerx, 100)
            pygame.time.delay(3000)
            running = False
        print(paused)
        pygame.display.flip()
        clock.tick(FPS)  # FPS를 조절하여 루프 속도를 제한한다.
