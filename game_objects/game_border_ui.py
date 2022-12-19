"""Define game border ui class.

This module holds a class responsible for blitting the game border ui, which
keeps track of in-game information like snacks eaten, time, and user score.

Classes:
    GameBorderUI: Holds game border and ui information.
"""

import os
import pygame
from math import trunc
from misc.constants import *
from misc.saved_data_io_functions import get_file_dict, get_score_name_list


class GameBorderUI(object):
    """Game border and ui to hold useful in-game information.

    This class holds a border made of 4 rect objects, which are used to check
    for collisions between the snake and the borders of the game. This class
    also acts as a container for all in-game information present on the border
    ui, blitting it to the screen and/or saving it until it is needed later.
    """

    def __init__(self, window: pygame.Surface, width: int, height: int, game_ready_ui: bool = False) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.game_ready_ui = game_ready_ui
        self.selected_border_theme = get_file_dict('user_preferences').get('BORDER THEME').split('~')[1]
        self.border_left = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets',
                         'border_themes',
                         f'{self.selected_border_theme}left.png',
                         ))), (GAME_BORDER_LEFT, self.height))
        self.border_right = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets',
                         'border_themes',
                         f'{self.selected_border_theme}right.png',
                         ))), (GAME_BORDER_RIGHT, self.height))
        self.border_upper = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets',
                         'border_themes',
                         f'{self.selected_border_theme}upper.png',
                         ))), (self.width, GAME_BORDER_UPPER))
        self.border_lower = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets',
                         'border_themes',
                         f'{self.selected_border_theme}lower.png',
                         ))), (self.width, GAME_BORDER_LOWER))
        self.border_image_list = [self.border_left, self.border_right, self.border_upper, self.border_lower]
        self.border_image_pos_list = [BACKGROUND_BLIT_POS, (self.width-GAME_BORDER_RIGHT, 0),
                                      BACKGROUND_BLIT_POS, (0, self.height-GAME_BORDER_LOWER)]
        self.border_image_rect_list = [border.get_rect(topleft=pos)
                                       for border, pos in zip(self.border_image_list, self.border_image_pos_list)]
        self.high_score = get_score_name_list()[0][0]
        self.user_score = 0
        self.snacks_eaten = 0
        self.game_runtime = '00:00'
        self.font_size = GAME_UI_FONT_SIZE
        self.text_font = pygame.font.Font(ARCADE_FONT_FILE, self.font_size)
        self.text_list = ['HIGH SCORE', f'{self.high_score}',
                          'YOUR SCORE', f'{self.snacks_eaten * GAME_UI_SCORE_MULTIPLIER}',
                          'SNACKS', f'{self.snacks_eaten}',
                          'TIME', f'{self.game_runtime}']
        self.text_color_list = [GAME_TEXT_LIGHT_BLUE, GAME_TEXT_WHITE, GAME_TEXT_LIGHT_BLUE, GAME_TEXT_WHITE,
                                GAME_TEXT_LIGHT_BLUE, GAME_TEXT_WHITE, GAME_TEXT_LIGHT_BLUE, GAME_TEXT_WHITE]
        self.text_pos_list = [(120, 18), (255, 18), (120, 42), (255, 42), (400, 33), (485, 33), (595, 33), (680, 33)]
        self.text_surface_list = [(self.text_font.render(self.text_list[index], True, self.text_color_list[index]))
                                  for index in range(len(self.text_list))]
        self.text_rect_list = [surface.get_rect(center=pos)
                               for surface, pos in zip(self.text_surface_list, self.text_pos_list)]
        self.text_bg_pos_list = [(255, 18, 105), (255, 42, 105), (485, 33, 60), (680, 33, 90)]  # (x, y, width)

    def draw(self) -> None:
        """Blit all border images and game ui info to screen."""
        # Draw border images.
        for border, rect in zip(self.border_image_list, self.border_image_rect_list):
            self.window.blit(border, rect)
        if self.game_ready_ui is True:
            # Draw black rectangles behind numbers on ui.
            for pos in self.text_bg_pos_list:
                black_rect = pygame.Rect(0, 0, pos[2], GAME_UI_TEXT_BG_HEIGHT)
                black_rect.center = (pos[0], pos[1])
                pygame.draw.rect(self.window, GAME_COLOR_BLACK, black_rect)
            self.update_ui_info()
            # Draw all text and number surfaces on top of border ui.
            for surface, rect in zip(self.text_surface_list, self.text_rect_list):
                self.window.blit(surface, rect)

    def update_ui_info(self) -> None:
        """Update what is displayed on screen with current ui info.

        This method rewrites the string text list with current ui info and
        then remakes the surface and rect lists in order for updated info to
        show up.
        """
        self.user_score = self.snacks_eaten * GAME_UI_SCORE_MULTIPLIER
        self.text_list[1] = f'{self.high_score}'
        self.text_list[3] = f'{self.user_score}'
        self.text_list[5] = f'{self.snacks_eaten}'
        self.text_list[7] = f'{self.game_runtime}'
        # Remake the surface and rect list comprehensions in order for updated info to show up.
        self.text_surface_list = [(self.text_font.render(self.text_list[index], True, self.text_color_list[index]))
                                  for index in range(len(self.text_list))]
        self.text_rect_list = [surface.get_rect(center=pos)
                               for surface, pos in zip(self.text_surface_list, self.text_pos_list)]

    def update_timer(self, current_time: int, start_time: int, paused_time: int) -> None:
        """Update time displayed on border ui timer.

        This method takes the time that the game was started, the current
        time, and total time spent in pause menu and calculates the game's
        current runtime in minutes and seconds, then updates the game_runtime
        attribute.

        Args:
            current_time: Current time in milliseconds.
            start_time: Start time of current game in milliseconds.
            paused_time: Total time that current game has been paused in
                milliseconds.
        """
        time_ms_format = current_time - start_time - paused_time
        time_s_format = time_ms_format / 1000

        minutes = time_s_format / 60
        minutes_tens_place = trunc(minutes / 10)
        minutes_ones_place = trunc(minutes % 10)

        seconds = time_s_format % 60
        seconds_tens_place = trunc(seconds / 10)
        seconds_ones_place = trunc(seconds % 10)

        self.game_runtime = f'{minutes_tens_place}{minutes_ones_place}:{seconds_tens_place}{seconds_ones_place}'

    def reset(self) -> None:
        """Reset all game border ui information to be used in next game."""
        self.game_ready_ui = True
        self.high_score = get_score_name_list()[0][0]
        self.user_score = 0
        self.snacks_eaten = 0
        self.game_runtime = '00:00'
