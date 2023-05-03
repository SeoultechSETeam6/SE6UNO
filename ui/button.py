import pygame
from mouse import Mouse, MouseState


class Button:
    """
    클릭할 때 특정 함수를 호출하는 버튼 클래스입니다.\n
    **x, y**: 버튼이 위치할 x, y 좌표 (버튼의 중앙 기준)\n
    **width, height**: 버튼의 가로, 세로\n
    **screen**: 해당 버튼이 그려질 캔버스\n
    **color**: 버튼 색상 (int type hexcode로 입력 권장)\n
    **text**: 버튼의 중앙에 표시할 글\n
    **text_size**: 글자의 크기\n
    **text_color**: 글자의 색상 (int type hexcode로 입력 권장)\n
    **on_click_funtion**: 버튼 클릭 시 일어날 이벤트 메서드
    """
    def __init__(self, x, y, width, height, screen, color=0xffffff, text='Sample', text_size=25, text_color=0x000000, on_click_function=None):
        self.keyboard_selected = False
        self.x = x - width // 2
        self.y = y - height // 2
        self.width = width
        self.height = height
        self.screen = screen
        self.on_click_function = on_click_function
        self.alreadyPressed = False
        self.selected_image = pygame.image.load("../resources/Image/selected_check.png")
        self.selected_image = pygame.transform.scale(self.selected_image, (width * 0.5, width * 0.5))

        self.color = {
            'normal': color,
            'hover': int(color * 0.6),
            'pressed': int(color * 0.3),
        }

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.__text_len = len(text)
        self.text = pygame.font.Font("../resources/maplestory_font.ttf", text_size).render(text, True, text_color)

        self.__mouse_pos = pygame.mouse.get_pos()

    def detect_event(self):
        """
        커서를 감지하고 효과를 연출, 클릭 시 지정한 메서드를 실행하닏 메서드입니다.\n
        화면이 매 프레임마다 업데이트 되므로 버튼이 기능하려면 무한 반복하는 부분에서 메서드를 사용해야합니다.
        :return: None
        """
        # 평상시
        self.__mouse_pos = pygame.mouse.get_pos()
        self.surface.fill(self.color['normal'])

        # 마우스 갖다댈 시
        if self.rect.collidepoint(self.__mouse_pos):
            self.surface.fill(self.color['hover'])

            # 버튼 누를 때
            if self.rect.collidepoint(self.__mouse_pos) and Mouse.getMouseState() == MouseState.CLICK:
                self.surface.fill(self.color['pressed'])
                Mouse.updateMouseState()
                # 클릭 판정을 위해 클릭 된 상태라면 더 이상 이벤트를 발생시키지 않음
                if not self.alreadyPressed and Mouse.getMouseState() == MouseState.DRAG:
                    self.on_click_function()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

    def draw(self):
        """
        버튼을 표시하는 메서드입니다.\n
        화면이 매 프레임마다 업데이트 되므로 버튼이 표시되려면 무한 반복하는 부분에서 메서드를 사용해야합니다.
        :return: None
        """
        if self.__text_len > 0:
            self.surface.blit(self.text, [self.rect.width / 2 - self.text.get_rect().width / 2,
                                          self.rect.height / 2 - self.text.get_rect().height / 2])
        self.screen.blit(self.surface, self.rect)


class ImageButton(Button):
    """
    클릭할 때 특정 함수를 호출하는 버튼 클래스입니다.\n
    **x, y**: 버튼이 위치할 x, y 좌표 (버튼의 중앙 기준)\n
    **width, height**: 버튼의 가로, 세로\n
    **screen**: 해당 버튼이 그려질 캔버스\n
    **img_path**: 이미지의 경로\n
    **color**: 버튼 색상 (int type hexcode로 입력 권장)\n
    **text**: 버튼의 중앙에 표시할 글\n
    **text_size**: 글자의 크기\n
    **text_color**: 글자의 색상 (int type hexcode로 입력 권장)\n
    **on_click_funtion**: 버튼 클릭 시 일어날 이벤트 메서드
    """
    def __init__(self, x, y, width, height, screen, img_path, color=0xffffff, text='', text_size=25, text_color=0x000000, on_click_function=None):
        super().__init__(x, y, width, height, screen, color, text, text_size, text_color, on_click_function)
        self.image = pygame.transform.scale(pygame.image.load(img_path), (width, height))
        self.img_rect = self.image.get_rect()
        self.img_rect.center = (x, y)

    # Override
    def detect_event(self):
        if self.rect.collidepoint(self.__mouse_pos):
            self.surface.set_alpha(75)
        else:
            self.surface.set_alpha(0)
        super().detect_event()

    def draw(self):
        super().draw()
        self.screen.blit(self.image, self.img_rect)


    def old_draw(self):
        # 평상시
        mouse_pos = pygame.mouse.get_pos()
        self.surface.set_alpha(0)

        # 마우스 갖다댈 시
        if self.rect.collidepoint(mouse_pos):
            self.surface.fill(self.color['hover'])
            self.surface.set_alpha(75)

            # 버튼 누를 때
            if self.rect.collidepoint(mouse_pos) and Mouse.getMouseState() == MouseState.CLICK:
                self.surface.fill(self.color['pressed'])
                Mouse.updateMouseState()
                # 클릭 판정을 위해 클릭 된 상태라면 더 이상 이벤트를 발생시키지 않음
                if not self.alreadyPressed and Mouse.getMouseState() == MouseState.DRAG:
                    self.on_click_function()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        if self.__text_len > 0:
            self.surface.blit(self.text, [self.rect.width / 2 - self.text.get_rect().width / 2,
                                          self.rect.height / 2 - self.text.get_rect().height / 2])
        self.screen.blit(self.surface, self.rect)
        self.screen.blit(self.image, self.img_rect)
