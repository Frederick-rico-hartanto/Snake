"""Define ancillary TextBox class (due to absence of such an object in pygame).

This module holds a reusable text box class that serves all the functions of a
basic text box widget: accept user input, save it, return error messages, draw
on screen, etc.

Classes:
    TextBox: Object that serves all the functions of a basic text box object.
"""

import os
import pygame
from misc.constants import *


class TextBox(object):
    """Selectable text box that accepts and saves user input up to 12 chars.

    This class is a reusable text box object constructor for pygame (due to
    the absence of any builtin text box objects in pygame). User has full
    control of the text box's dimensions, position, color, text_color, and
    font size. Note: Character limit is 12.
    """

    def __init__(self, window: pygame.Surface, textbox_pos: tuple[int, int], textbox_width: int, textbox_height: int,
                 textbox_color: tuple[int, int, int], font_size: int, text_color: tuple[int, int, int], text: str = '',
                 ) -> None:
        self.window = window
        self.textbox_pos = textbox_pos
        self.textbox_width = textbox_width
        self.textbox_height = textbox_height
        self.textbox_color = textbox_color
        self.font_size = font_size
        self.text_color = text_color
        self.text = text
        self.textbox_rect = pygame.Rect(0, 0, self.textbox_width, self.textbox_height)
        self.textbox_rect.midleft = self.textbox_pos
        self.textbox_outline_offset = 4
        self.textbox_rect_outline = pygame.Rect(0,
                                                0,
                                                (self.textbox_width + self.textbox_outline_offset*2),
                                                (self.textbox_height + self.textbox_outline_offset*2),
                                                )
        self.textbox_rect_outline.midleft = ((self.textbox_pos[0]-self.textbox_outline_offset), self.textbox_pos[1])
        self.text_font = pygame.font.Font(ARCADE_FONT_FILE, self.font_size)
        self.text_surface = self.text_font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(midleft=((self.textbox_pos[0]+self.textbox_outline_offset),
                                                             self.textbox_pos[1]))
        self.button_hover_sfx = pygame.mixer.Sound(os.path.join('project_assets', 'sfx', 'button_hover.wav'))
        self.hovered = False
        self.selected = True

    def draw(self, mouse_pos: tuple[int, int], sfx_bool: str) -> None:
        """Blit text box and text to screen.

        Uses class attributes and entered args to blit the text box, any
        entered text, and a "highlight" box behind the text box if text box's
        "selected" boolean attribute is True.

        Args:
            mouse_pos: Used to determine if cursor was hovering over text box
                when clicked.
            sfx_bool: Used to determine whether text box should make a click
                sfx when selected.
        """
        self.draw_textbox(mouse_pos, sfx_bool)
        self.window.blit(self.text_surface, self.text_rect)

    def is_hovering(self, mouse_pos: tuple[int, int]) -> bool:
        """Check if mouse is hovering over text box."""
        if self.textbox_rect.collidepoint(mouse_pos):
            return True

    def draw_textbox(self, mouse_pos: tuple[int, int], sfx_bool: str) -> None:
        """Determine if highlighted and blit text box and highlight to screen.

        This method uses class attributes and entered args to determine if
        text box is being hovered over or is selected: method blits a blue
        "highlight" rect around the text box if it is selected, a white one if
        it is being hovered over, plays a hover sfx, and blits the actual text
        box as well, regardless.

        Args:
            mouse_pos: Used to determine if cursor was hovering over text box.
            sfx_bool: Used to determine whether text box should make a hover
                sfx when hovered over.
        """
        if self.selected:
            pygame.draw.rect(self.window, GAME_TEXT_LIGHT_BLUE, self.textbox_rect_outline)
        elif self.is_hovering(mouse_pos):
            pygame.draw.rect(self.window, GAME_TEXT_WHITE, self.textbox_rect_outline)
            if self.hovered is False:
                self.hovered = True
                if sfx_bool == 'True':
                    self.button_hover_sfx.play()
        else:
            if self.hovered is True:
                self.hovered = False

        pygame.draw.rect(self.window, self.textbox_color, self.textbox_rect)

    def add_char(self, input_char: str) -> None:
        """Adds input_char to self.text unless self.text is > 12 chars."""
        if len(self.text) < TEXT_BOX_CHAR_LIMIT:
            self.text += input_char.upper()
            self.text_surface = self.text_font.render(self.text, True, self.text_color)
        else:
            print('char limit 12')

    def remove_char(self) -> None:
        """Removes last char from self.text and updates self.text_surface."""
        self.text = self.text[:-1]
        self.text_surface = self.text_font.render(self.text, True, self.text_color)
