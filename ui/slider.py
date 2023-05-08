import pygame
import math
from controller.mouse_controller import Mouse, MouseState


class Slider:
    def __init__(self, screen, x, y, width, height, value=1, image_size=25):
        self.selected = False
        self.keyboard_selected = False
        self.screen = screen
        self.x = x - width // 2
        self.y = y + height // 1.5
        self.width = width
        self.height = height

        self.min = 0
        self.max = 1
        self.step = 0.01

        self.colour = (150, 150, 150)
        self.handleColour = (255, 255, 255)

        self.borderThickness = 3
        self.borderColour = (0, 0, 0)

        self.value = value

        self.radius = self.height // 2
        self.handleRadius = int(self.height / 1.3)

        self.selected_image = pygame.image.load("../resources/Image/selected_check.png")
        self.selected_image = pygame.transform.scale(self.selected_image, (image_size * 1.5, image_size * 1.5))

        self.circle = (int(self.x + (self.value - self.min) / (self.max - self.min) * self.width), self.y + self.height // 2)
        self.rect = pygame.Rect(self.x - image_size * 2, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(self.screen, self.colour, (self.x, self.y + self.height // 2), self.radius)
        pygame.draw.circle(self.screen, self.colour, (self.x + self.width, self.y + self.height // 2), self.radius)

        self.circle = (int(self.x + (self.value - self.min) / (self.max - self.min) * self.width), self.y + self.height // 2)
        pygame.draw.circle(self.screen, self.handleColour, self.circle, self.handleRadius)

    def detect_event(self):
        mouseState = Mouse.getMouseState()
        x, y = Mouse.getMousePos()

        if self.contains(x, y):
            if mouseState == MouseState.CLICK:
                self.selected = True

        if mouseState == MouseState.RELEASE:
            self.selected = False

        if self.selected:
            self.handleColour = '#666666'
            self.value = self.round((x - self.x) / self.width * self.max + self.min)
            self.value = max(min(self.value, self.max), self.min)
        else:
            self.handleColour = (255, 255, 255)

    def contains(self, x, y):
        handleX = int(self.x + (self.value - self.min) / (self.max - self.min) * self.width)
        handleY = self.y + self.height // 2

        if math.sqrt((handleX - x) ** 2 + (handleY - y) ** 2) <= self.handleRadius:
            return True

        return False

    def round(self, value):
        return self.step * round(value / self.step)
