import pygame
from mouse import Mouse, MouseState


class Button:
    """
    클릭할 때 한 번만 이벤트를 발생시키는 버튼 클래스입니다.\n
    **x, y**: 버튼이 위치할 x, y 좌표 (중앙 기준)\n
    **width, height**: 버튼의 가로, 세로\n
    **button_text**: 버튼에 적힐 글자\n
    **on_click_funtion**: 버튼 클릭 시 일어날 이벤트 메서드
    """
    def __init__(self, x, y, width, height, text='Sample', on_click_function=None, font_size=25, keyboard_selected=False):
        self.keyboard_selected = keyboard_selected
        self.x = x - width // 2
        self.y = y - height // 2
        self.width = width
        self.height = height
        self.on_click_function = on_click_function
        self.alreadyPressed = False
        self.font = pygame.font.Font("./resources/maplestory_font.ttf", font_size)
        self.selected_image = pygame.image.load("./resources/Image/selected_check.png")
        self.selected_image = pygame.transform.scale(self.selected_image, (font_size * 1.5, font_size * 1.5))

        self.fill_colors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = self.font.render(text, True, (0, 0, 0))

    def process(self):
        """
        커서를 감지하여 버튼을 갖다대거나 클릭을 인식하고 이벤트를 발생시키는 메서드입니다.\n
        화면이 업데이트 매 초 업데이트 되므로 버튼이 기능하려면 무한 반복하는 부분에서 메서드를 사용해야합니다.
        :return: None
        """
        # 평상시
        mouse_pos = pygame.mouse.get_pos()
        self.surface.fill(self.fill_colors['normal'])

        # 마우스 갖다댈 시
        if self.rect.collidepoint(mouse_pos):
            self.surface.fill(self.fill_colors['hover'])

            # 버튼 누를 때
            if self.rect.collidepoint(mouse_pos) and Mouse.getMouseState() == MouseState.CLICK:
                self.surface.fill(self.fill_colors['pressed'])
                Mouse.updateMouseState()
                # 클릭 판정을 위해 클릭 된 상태라면 더 이상 이벤트를 발생시키지 않음
                if not self.alreadyPressed and Mouse.getMouseState() == MouseState.DRAG:
                    self.on_click_function()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.surface.blit(self.font, [
            self.rect.width / 2 - self.font.get_rect().width / 2,
            self.rect.height / 2 - self.font.get_rect().height / 2
        ])

class ButtonWithImg(Button):
    """
    클릭할 때 한 번만 이벤트를 발생시키는 버튼 클래스입니다.\n
    **x, y**: 버튼이 위치할 x, y 좌표 (중앙 기준)\n
    **width, height**: 버튼의 가로, 세로\n
    **img_path**: 이미지의 경로\n
    **on_click_funtion**: 버튼 클릭 시 일어날 이벤트 메서드
    """
    def __init__(self, x, y, width, height, img_path, on_click_function=None, selected=False):
        super().__init__(x, y, width, height, "", on_click_function, 0, selected)
        self.img_path = img_path
        self.image = pygame.transform.scale(pygame.image.load(img_path), (width, height))

        self.img_rect = self.image.get_rect()
        self.img_rect.center = (x, y)

    # Override
    def process(self):
        # 평상시
        mouse_pos = pygame.mouse.get_pos()
        self.surface.set_alpha(0)

        # 마우스 갖다댈 시
        if self.rect.collidepoint(mouse_pos) or self.selected:
            self.surface.fill(self.fill_colors['hover'])
            self.surface.set_alpha(75)

            # 버튼 누를 때
            if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.surface.fill(self.fill_colors['pressed'])

                # 클릭 판정을 위해 클릭 된 상태라면 더 이상 이벤트를 발생시키지 않음
                if not self.alreadyPressed:
                    self.on_click_function()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False
