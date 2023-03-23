import pygame
import pickle
from button import Button
import reset_option as reset

pygame.init()

# 옵션 변경을 위한 변수
try:
    with open("save_option.pickle", "rb") as f:
        display_size = pickle.load(f)
        color_weakness = pickle.load(f)
        key_setting = pickle.load(f)
except EOFError:
    display_size = reset.display_size
    color_weakness = reset.color_weakness
    key_setting = reset.key_setting

if display_size[0] == 1920:
    font_size = reset.font_size[0]
    button_size = reset.button_size[0]
elif display_size[0] == 1600:
    font_size = reset.font_size[1]
    button_size = reset.button_size[1]
else:
    font_size = reset.font_size[2]
    button_size = reset.button_size[2]

font = pygame.font.Font("../Maplestory Bold.ttf", font_size[0])
small_font = pygame.font.Font("../Maplestory Bold.ttf", font_size[1])


# 버튼 클릭시 메소드 구현
def size_1920_event():
    reset.display_size = [1920, 1080]
    screen_size_button[0].fill_colors['normal'] = '#666666'
    screen_size_button[1].fill_colors['normal'] = '#ffffff'
    screen_size_button[2].fill_colors['normal'] = '#ffffff'


def size_1600_event():
    reset.display_size = [1600, 900]
    screen_size_button[0].fill_colors['normal'] = '#ffffff'
    screen_size_button[1].fill_colors['normal'] = '#666666'
    screen_size_button[2].fill_colors['normal'] = '#ffffff'


def size_1200_event():
    reset.display_size = [1200, 720]
    screen_size_button[0].fill_colors['normal'] = '#ffffff'
    screen_size_button[1].fill_colors['normal'] = '#ffffff'
    screen_size_button[2].fill_colors['normal'] = '#666666'


def color_weakness_event():
    if reset.color_weakness:
        color_weakness_button.font = small_font.render("ON", True, (0, 0, 0))
        reset.color_weakness = False
    else:
        color_weakness_button.font = small_font.render("OFF", True, (0, 0, 0))
        reset.color_weakness = True


def key_up_event():
    pop_up('up')
    key_setting_button[0].font = small_font.render("UP: "+pygame.key.name(reset.key_setting['up']), True, (0, 0, 0))


def key_down_event():
    pop_up('down')
    key_setting_button[1].font = small_font.render("DOWN: " + pygame.key.name(reset.key_setting['down']), True, (0, 0, 0))


def key_left_event():
    pop_up('left')
    key_setting_button[2].font = small_font.render("LEFT: " + pygame.key.name(reset.key_setting['left']), True, (0, 0, 0))


def key_right_event():
    pop_up('right')
    key_setting_button[3].font = small_font.render("RIGHT: " + pygame.key.name(reset.key_setting['right']), True, (0, 0, 0))


def key_enter_event():
    pop_up('enter')
    key_setting_button[4].font = small_font.render("ENTER: " + pygame.key.name(reset.key_setting['enter']), True, (0, 0, 0))


def reset_event():
    with open("save_option.pickle", "wb"):
        pass
    global running
    running = False


def save_event():
    with open("save_option.pickle", "wb") as sf:
        pickle.dump(reset.display_size, sf)
        pickle.dump(reset.color_weakness, sf)
        pickle.dump(reset.key_setting, sf)
    global running
    running = False


def exit_event():
    global running
    running = False


def pop_up(direction):
    popup = small_font.render("바꾸고자하는 키를 입력하시오.", True, (0, 0, 0))
    screen.fill((255, 255, 255))
    screen.blit(popup, (screen.get_width() // 2 - 150, screen.get_height() // 2))
    pygame.display.flip()
    popup_running = True
    while popup_running:
        for popup_event in pygame.event.get():
            if popup_event.type == pygame.KEYDOWN:
                reset.key_setting[direction] = popup_event.key
                popup_running = False


# 옵션 화면 세팅
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("UNO Game")

change_screen_size = font.render("화면 크기 변경", True, (255, 255, 255))
change_color_weakness = font.render("색약 모드 변경", True, (255, 255, 255))
change_key_setting = font.render("사용 키 설정 변경", True, (255, 255, 255))
screen_size_button = [Button(screen.get_width() // 3 * 2 - screen.get_width() // 8, screen.get_height() // 5, button_size[0], button_size[1], "1920 * 1080", size_1920_event, font_size[1]),
                      Button(screen.get_width() // 3 * 2, screen.get_height() // 5, button_size[0], button_size[1], "1600 * 900", size_1600_event, font_size[1]),
                      Button(screen.get_width() // 3 * 2 + screen.get_width() // 8, screen.get_height() // 5, button_size[0], button_size[1], "1200 * 720", size_1200_event, font_size[1])]

if display_size[0] == 1920:
    screen_size_button[0].fill_colors['normal'] = '#666666'
elif display_size[0] == 1600:
    screen_size_button[1].fill_colors['normal'] = '#666666'
else:
    screen_size_button[2].fill_colors['normal'] = '#666666'

if color_weakness:
    color_weakness_button = Button(screen.get_width() // 3 * 2, screen.get_height() // 5 * 2, button_size[0], button_size[1], "OFF", color_weakness_event, font_size[1])
else:
    color_weakness_button = Button(screen.get_width() // 3 * 2, screen.get_height() // 5 * 2, button_size[0], button_size[1], "ON", color_weakness_event, font_size[1])
key_setting_button = [Button(screen.get_width() // 3 * 2 - screen.get_width() // 9 * 2, screen.get_height() * 3 // 5, button_size[0], button_size[1], "UP: up", key_up_event, font_size[1]),
                      Button(screen.get_width() // 3 * 2 - screen.get_width() // 9, screen.get_height() * 3 // 5, button_size[0], button_size[1], "DOWN: down", key_down_event, font_size[1]),
                      Button(screen.get_width() // 3 * 2, screen.get_height() * 3 // 5, button_size[0], button_size[1], "LEFT: left", key_left_event, font_size[1]),
                      Button(screen.get_width() // 3 * 2 + screen.get_width() // 9, screen.get_height() * 3 // 5, button_size[0], button_size[1], "RIGHT: right", key_right_event, font_size[1]),
                      Button(screen.get_width() // 3 * 2 + screen.get_width() // 9 * 2, screen.get_height() * 3 // 5, button_size[0], button_size[1], "ENTER: return", key_enter_event, font_size[1])]
reset_setting = Button(screen.get_width() // 4, screen.get_height() // 5 * 4, button_size[0], button_size[1], "설정 초기화", reset_event, font_size[1])
save_setting = Button(screen.get_width() // 4 * 2, screen.get_height() // 5 * 4, button_size[0], button_size[1], "설정 저장", save_event, font_size[1])
quit_setting = Button(screen.get_width() // 4 * 3, screen.get_height() // 5 * 4, button_size[0], button_size[1], "설정 나가기", exit_event, font_size[1])
buttons = [color_weakness_button, reset_setting, save_setting, quit_setting]
for i in screen_size_button:
    buttons.append(i)
for i in key_setting_button:
    buttons.append(i)


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(change_screen_size, (screen.get_width() // 7, screen.get_height() // 5))
    screen.blit(change_color_weakness, (screen.get_width() // 7, screen.get_height() // 5 * 2))
    screen.blit(change_key_setting, (screen.get_width() // 7, screen.get_height() // 5 * 3))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for button in buttons:
        button.process()
        screen.blit(button.surface, button.rect)

    pygame.display.flip()
# 나가기
pygame.quit()
