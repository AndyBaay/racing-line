import copy
from datetime import datetime

import pygame

from ..lib.constants import Color


class Button:
    def __init__(
        self,
        pos,
        width,
        height,
        text,
        text_color=Color.BLACK,
        default_color=Color.WHITE,
        hover_color=Color.LIGHT_GRAY,
        pressed_color=Color.LIGHT_BLUE,
        on_click=None,
    ):
        # defining a font
        smallfont = pygame.font.SysFont("Corbel", 35)
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.text = smallfont.render(text, True, text_color.value)
        self.state = ""  # hover, pressed, or empty string
        self.last_click = datetime(1, 1, 1)
        self.default_color = default_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.on_click = on_click

    def check_for_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.state = "pressed"
            self.last_click = datetime.now()
            self.on_click()
            return True
        else:
            return False

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.state = "hover"
        else:
            self.state = ""

    def draw(self, screen):
        # Keep the highlighted color longer than the actual event for a button press
        if (datetime.now() - self.last_click).total_seconds() < 0.2:
            button_color = self.pressed_color.value
        elif self.state == "hover":
            button_color = self.hover_color.value
        else:
            button_color = self.default_color.value

        pygame.draw.rect(screen, button_color, self.rect)
        screen.blit(self.text, self.rect)
