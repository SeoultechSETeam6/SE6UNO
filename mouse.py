from enum import Enum
import pygame


class MouseState(Enum):
    HOVER = 0
    CLICK = 1
    RIGHT_CLICK = 2
    DRAG = 3
    RIGHT_DRAG = 4  # Not sure when this is ever used but added anyway for completeness
    RELEASE = 5
    RIGHT_RELEASE = 6


class Mouse:

    _mouseState = MouseState.HOVER

    @staticmethod
    def updateMouseState():
        leftPressed = pygame.mouse.get_pressed()[0]
        rightPressed = pygame.mouse.get_pressed()[2]

        if leftPressed:
            if Mouse._mouseState == MouseState.CLICK or Mouse._mouseState == MouseState.DRAG:
                Mouse._mouseState = MouseState.DRAG
            else:
                Mouse._mouseState = MouseState.CLICK

        elif rightPressed:
            if Mouse._mouseState == MouseState.RIGHT_CLICK or Mouse._mouseState == MouseState.RIGHT_DRAG:
                Mouse._mouseState = MouseState.RIGHT_DRAG
            else:
                Mouse._mouseState = MouseState.RIGHT_CLICK
        else:
            # If previously was held down, call the release
            if Mouse._mouseState == MouseState.CLICK or Mouse._mouseState == MouseState.DRAG:
                Mouse._mouseState = MouseState.RELEASE

            elif Mouse._mouseState == MouseState.RIGHT_CLICK or Mouse._mouseState == MouseState.RIGHT_DRAG:
                Mouse._mouseState = MouseState.RIGHT_RELEASE

            else:
                Mouse._mouseState = MouseState.HOVER

    @staticmethod
    def getMouseState() -> MouseState:
        return Mouse._mouseState

    @staticmethod
    def resetMouseState():
        _mouseState = MouseState.HOVER

    @staticmethod
    def getMousePos() -> (int, int):
        return pygame.mouse.get_pos()
