import pygame
import math
from mouse import Mouse, MouseState


class Slider:
    def __init__(self, screen, x, y, width, height, value=1):
        self.selected = False
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

        self.circle = (int(self.x + (self.value - self.min) / (self.max - self.min) * self.width), self.y + self.height // 2)

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(self.screen, self.colour, (self.x, self.y + self.height // 2), self.radius)
        pygame.draw.circle(self.screen, self.colour, (self.x + self.width, self.y + self.height // 2), self.radius)

        self.circle = (int(self.x + (self.value - self.min) / (self.max - self.min) * self.width), self.y + self.height // 2)
        pygame.draw.circle(self.screen, self.handleColour, self.circle, self.handleRadius)

    def process(self):
        mouseState = Mouse.getMouseState()
        x, y = Mouse.getMousePos()

        if self.contains(x, y):
            if mouseState == MouseState.CLICK:
                self.selected = True

        if mouseState == MouseState.RELEASE:
            self.selected = False

        if self.selected:
            self.value = self.round((x - self.x) / self.width * self.max + self.min)
            self.value = max(min(self.value, self.max), self.min)

    def contains(self, x, y):
        handleX = int(self.x + (self.value - self.min) / (self.max - self.min) * self.width)
        handleY = self.y + self.height // 2

        if math.sqrt((handleX - x) ** 2 + (handleY - y) ** 2) <= self.handleRadius:
            return True

        return False

    def round(self, value):
        return self.step * round(value / self.step)
