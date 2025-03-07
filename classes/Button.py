from contextlib import suppress

import pygame

pygame.init()
font = pygame.font.Font(None, 24)


class Button:
    """Button class to create a button with text and a callback function."""

    text: str = ""
    x: int = 0
    y: int = 0
    callback = None

    surface = None
    rect = None

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        callback=None,
    ):
        self.text = text
        self.x = x
        self.y = y
        self.callback = callback

        self.surface = font.render(text, True, "white")
        self.rect = self.surface.get_rect(topleft=(x, y))


class ButtonGroup:
    """ButtonGroup class to create and manage multiple buttons."""

    buttons: list = []

    surface = None
    x: int = 16
    y: int = 16

    def __init__(self):
        self.surface = pygame.display.get_surface()

    def add(self, text: str, callback=None):
        """Add a button to the group."""
        self.buttons.append(
            Button(
                text,
                self.x,
                self.y,
                callback,
            )
        )
        self.y += 32

    def draw(self):
        """Draw all buttons to the screen."""
        for button in self.buttons:
            self.surface.blit(button.surface, button.rect)

    def handle_event(self, event):
        """Handle click for all buttons."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos):
                        with suppress(Exception):
                            button.callback()
                        break
