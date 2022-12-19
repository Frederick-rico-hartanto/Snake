"""Define game grid class that may be chosen as a setting.

Classes:
    GameGrid: White grid of lines that appears in game.
"""

import pygame
from misc.constants import *
from game_objects.game_border_ui import GameBorderUI


class GameGrid(object):
    """Game grid appears in game as a way of showing snake movement distance.

    This class holds all of the content required to draw a grid of white lines
    that appear in game as a way to show the player where exactly the snake is
    going and where snack objects are located.
    """

    def __init__(self, window: pygame.Surface, border_ui: GameBorderUI) -> None:
        self.window = window
        self.border_ui = border_ui
        self.grid_left = self.border_ui.border_image_rect_list[0].right
        self.grid_right = self.border_ui.border_image_rect_list[1].left
        self.grid_top = self.border_ui.border_image_rect_list[2].bottom
        self.grid_bottom = self.border_ui.border_image_rect_list[3].top
        self.vertical_lines_start = self.grid_left + SNAKE_CUBE_DISPLACEMENT
        self.vertical_lines_end = self.grid_right - SNAKE_CUBE_DISPLACEMENT + 1
        self.horizontal_lines_start = self.grid_top + SNAKE_CUBE_DISPLACEMENT
        self.horizontal_lines_end = self.grid_bottom - SNAKE_CUBE_DISPLACEMENT + 1

    def draw(self) -> None:
        """Blits grid of white x-axis and y-axis lines to screen."""
        for x in range(self.vertical_lines_start, self.vertical_lines_end, SNAKE_CUBE_DISPLACEMENT):
            pygame.draw.line(self.window, GAME_COLOR_LIGHT_GREY, (x, self.grid_top), (x, self.grid_bottom))

        for y in range(self.horizontal_lines_start, self.horizontal_lines_end, SNAKE_CUBE_DISPLACEMENT):
            pygame.draw.line(self.window, GAME_COLOR_LIGHT_GREY, (self.grid_left, y), (self.grid_right, y))
