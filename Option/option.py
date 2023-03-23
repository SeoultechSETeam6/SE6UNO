import pygame
from button import Button
import reset_option as reset
import save_option as save

pygame.init()

# 옵션 변경을 위한 변수
font = pygame.font.Font("../Maplestory Bold.ttf", 60)
small_font = pygame.font.Font("../Maplestory Bold.ttf", 25)


# 버튼 클릭시 메소드 구현
def size_1920_event():
    save.display_size = [1920, 1080]


def size_1600_event():
    save.display_size = [1600, 900]


def size_1200_event():
    save.display_size = [1200, 720]


def color_weakness_event():
    if save.color_weakness:
        color_weakness_button.font = small_font.render("ON", True, (0, 0, 0))
        save.color_weakness = False
    else:
        color_weakness_button.font = small_font.render("OFF", True, (0, 0, 0))
        save.color_weakness = True


def key_up_event():
    print("up")


def key_down_event():
    print("down")


def key_left_event():
    print("left")


def key_right_event():
    print("right")


def key_enter_event():
    print("enter")


def reset_event():
    save.display_size = reset.display_size
    save.color_weakness = reset.color_weakness
    save.key_setting = save.key_setting


def save_event():
    print("save")


# 옵션 화면 세팅
screen = pygame.display.set_mode(save.display_size)
pygame.display.set_caption("UNO Game")

change_screen_size = font.render("화면 크기 변경", True, (255, 255, 255))
change_color_weakness = font.render("색약 모드 변경", True, (255, 255, 255))
change_key_setting = font.render("사용 키 설정 변경", True, (255, 255, 255))
screen_size_button = [Button(screen.get_width() // 3 * 2 - screen.get_width() // 8, screen.get_height() // 5, 200, 75, "1920 * 1080", size_1920_event),
                      Button(screen.get_width() // 3 * 2, screen.get_height() // 5, 200, 75, "1600 * 900", size_1600_event),
                      Button(screen.get_width() // 3 * 2 + screen.get_width() // 8, screen.get_height() // 5, 200, 75, "1200 * 720", size_1200_event)]

if save.display_size[0] == 1920:
    screen_size_button[0].fill_colors['normal'] = '#666666'
elif save.display_size[0] == 1600:
    screen_size_button[1].fill_colors['normal'] = '#666666'
else:
    screen_size_button[2].fill_colors['normal'] = '#666666'

if save.color_weakness:
    color_weakness_button = Button(screen.get_width() // 3 * 2, screen.get_height() // 5 * 2, 200, 75, "OFF", color_weakness_event)
else:
    color_weakness_button = Button(screen.get_width() // 3 * 2, screen.get_height() // 5 * 2, 200, 75, "ON", color_weakness_event)
key_setting_button = [Button(screen.get_width() // 3 * 2 - screen.get_width() // 9 * 2, screen.get_height() * 3 // 5, 200, 75, "UP: Up", key_up_event),
                      Button(screen.get_width() // 3 * 2 - screen.get_width() // 9, screen.get_height() * 3 // 5, 200, 75, "DOWN: Down", key_down_event),
                      Button(screen.get_width() // 3 * 2, screen.get_height() * 3 // 5, 200, 75, "LEFT: Left", key_left_event),
                      Button(screen.get_width() // 3 * 2 + screen.get_width() // 9, screen.get_height() * 3 // 5, 200, 75, "RIGHT: Right", key_right_event),
                      Button(screen.get_width() // 3 * 2 + screen.get_width() // 9 * 2, screen.get_height() * 3 // 5, 200, 75, "ENTER: Enter", key_enter_event)]
reset_setting = Button(screen.get_width() // 3, screen.get_height() // 5 * 4, 200, 75, "설정 초기화", reset_event)
save_setting = Button(screen.get_width() // 3 * 2, screen.get_height() // 5 * 4, 200, 75, "설정 저장", save_event)
buttons = [color_weakness_button, reset_setting, save_setting]
for i in screen_size_button:
    buttons.append(i)
for i in key_setting_button:
    buttons.append(i)

screen.fill((0, 0, 0))
screen.blit(change_screen_size, (screen.get_width() // 7, screen.get_height() // 5))
screen.blit(change_color_weakness, (screen.get_width() // 7, screen.get_height() // 5 * 2))
screen.blit(change_key_setting, (screen.get_width() // 7, screen.get_height() // 5 * 3))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for button in buttons:
        button.process()
        screen.blit(button.surface, button.rect)

    pygame.display.flip()
# 나가기
pygame.quit()
