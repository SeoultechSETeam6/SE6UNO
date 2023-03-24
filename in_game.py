import pygame


def game():
    # pygame.init()

    font = pygame.font.Font("resources/maplestory_font.ttf", 20)
    # 현재 몇명의 플레이어가 있는지
    now_player = 5

    # 크기 설정
    screen_size = [1920, 1080]
    screen = pygame.display.set_mode(screen_size)

    # 배경 설정
    pygame.display.set_caption("UNO Game")
    board_background = pygame.image.load("resources/Image/background/1.jpg")
    board_background = pygame.transform.scale(board_background, (1485, 720))
    my_deck_background = pygame.image.load("resources/Image/background/2.jpg")
    my_deck_background = pygame.transform.scale(my_deck_background, (1485, 360))
    player_background = pygame.image.load("resources/Image/background/3.jpg")
    player_background = pygame.transform.scale(player_background, (495, 1080))

    # 보드 설정
    card_back = pygame.image.load("resources/Image/background/5.png")
    card_back = pygame.transform.scale(card_back, (100, 150))

    # 후에 덱 클래스와 연결해야 함
    card_front = pygame.image.load("resources/Image/background/4.png")
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

    player_card1 = 7
    player_name1 = font.render("Player1", True, (0, 0, 0))
    player_list1 = pygame.image.load("resources/Image/background/1.jpg")
    player_list1 = pygame.transform.scale(player_list1, (390, 190))
    player_card_back = pygame.image.load("resources/Image/background/5.png")
    player_card_back = pygame.transform.scale(player_card_back, (45, 70))

    player_list1.blit(player_name1, (10, 10))
    temp = 0

    for _ in range(player_card1):
        player_list1.blit(player_card_back, (10 + temp, 100))
        temp = temp + 50

    temp = 0
    for i in range(now_player):
        player_background.blit(empty_player, (20, 20 + temp))
        temp = temp + 210

    player_background.blit(player_list1, (20, 20))

    # 내 덱 설정
    my_card = 7
    my_name = font.render("You", True, (0, 0, 0))

    my_deck_background.blit(my_name, (20, 20))
    temp = 0
    for _ in range(my_card):
        my_deck_background.blit(card_front, (50 + temp, 100))
        temp = temp + 110

    screen.blit(board_background, (0, 0))
    screen.blit(my_deck_background, (0, 720))
    screen.blit(player_background, (1485, 0))
    pygame.display.flip()

    # 루프 시작
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    exit()
