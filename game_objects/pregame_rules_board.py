"""Define rule board class to be blit before a new game.

This module holds a class responsible for blitting a game rules board before
each new game.

Classes:
    GameRulesBoard: Simple board with instructions of how to play.
"""

import os
import pygame
from misc.constants import *


class GameRulesBoard(object):
    """Instruction board explaining the rules of snake, before each game.

    This class holds all of the content required to draw a pregame rules
    board, displaying a black board, the rules of the basic default snake
    game, the game's controls, and a "press any key to continue" caption.
    """

    def __init__(self, window: pygame.Surface, width: int, height: int) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.background = pygame.transform.scale(pygame.Surface.convert(pygame.image.load(
            os.path.join('project_assets', 'backgrounds', 'black_background.png'))), RULES_BOARD_DIMENSIONS)
        self.font_size = RULES_BOARD_TEXT_FONT_SIZE
        self.text_font = pygame.font.Font(ARCADE_FONT_FILE, self.font_size)
        self.text_list = ['Objective: eat as many of the snacks', 'as you can without crashing',
                          'into yourself or the borders', '(Basic rules of Snake)',
                          'UP/LEFT/DOWN/RIGHT ', '- move controls',
                          'ESC ', '- pause menu',
                          'ENTER ', '- select',
                          'press any key to start']
        self.text_color_list = [GAME_TEXT_BLUE, GAME_TEXT_BLUE, GAME_TEXT_BLUE, GAME_TEXT_BLUE, GAME_TEXT_GREEN,
                                GAME_TEXT_WHITE, GAME_TEXT_GREEN, GAME_TEXT_WHITE, GAME_TEXT_GREEN, GAME_TEXT_WHITE,
                                GAME_TEXT_LIGHT_BLUE]
        self.text_pos_list = [(400, 130), (400, 150), (400, 170), (400, 190), (285, 250), (485, 250), (377, 270),
                              (467, 270), (365, 290), (443, 290), (400, 380)]
        self.text_surface_list = [(self.text_font.render(self.text_list[index], True, self.text_color_list[index]))
                                  for index in range(len(self.text_list))]
        self.text_rect_list = [surface.get_rect(center=pos)
                               for surface, pos in zip(self.text_surface_list, self.text_pos_list)]

    def draw(self) -> None:
        """Blit background for board and all rules board text content."""
        self.window.blit(self.background, RULES_BOARD_POS)
        for surface, rect in zip(self.text_surface_list, self.text_rect_list):
            self.window.blit(surface, rect)
