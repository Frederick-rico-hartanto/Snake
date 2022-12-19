"""Define game's score board class.

This module holds a class responsible for blitting a score board object to the
screen.

Classes:
    ScoreBoard: Scoreboard object of page containing user's score and name row.
"""

import os
import pygame
from misc.constants import *
from misc.saved_data_io_functions import get_score_name_list, get_page_of_user_row


class ScoreBoard(object):
    """Scoreboard showing page containing user's rank row for previous game.

    This class holds all the code responsible for creating a score board
    page containing the user's (rank, score, name) pair row. The page contains
    10 rows of (rank, score, name) data with one of them being the row of the
    user's entered data.
    """

    def __init__(self, window: pygame.Surface, user_score: int, user_name: str) -> None:
        self.window = window
        self.user_score = user_score
        self.user_name = user_name
        self.score_name_list = get_score_name_list()
        self.user_row_page, self.user_row_index = get_page_of_user_row(self.score_name_list,
                                                                       self.user_score,
                                                                       self.user_name)

        # Scoreboard column label attributes.
        self.label_color = GAME_TEXT_GREEN
        self.label_font = pygame.font.Font(ARCADE_FONT_FILE, SCORE_DATA_LABEL_FONT_SIZE)
        self.label_text_list = ['RANK', 'SCORE', 'NAME']
        self.label_pos_list = [(120, 80), (420, 80), (500, 80)]
        self.label_surface_list = [(self.label_font.render(label, True, self.label_color))
                                   for label in self.label_text_list]
        self.label_rect_list = [surface.get_rect(midright=pos) if self.label_pos_list.index(pos) == 1
                                else surface.get_rect(midleft=pos)
                                for surface, pos in zip(self.label_surface_list, self.label_pos_list)]

        # Scoreboard data attributes.
        self.data_color = GAME_TEXT_LIGHT_BLUE
        self.data_font = pygame.font.Font(ARCADE_FONT_FILE, SCORE_DATA_FONT_SIZE)
        self.data_pos_list, self.data_surface_list, self.data_rect_list = self.set_column_surface_rect_lists()

        # Highlighted user row attributes.
        self.user_row_highlight_rect, self.user_row_surface_list, self.user_row_rect_list \
            = self.set_user_row_surface_rect_lists()

    def draw(self) -> None:
        """Draw all score board column labels and rows.

        This method draws all ScoreBoard content to the window
        by calling the methods that draw the (rank, score, name)
        column labels and all the data that goes in each of
        those columns for the page that the user's
        (rank, score, name) data is on.
        """
        self.draw_labels()
        self.draw_data()

    def draw_labels(self) -> None:
        """Blits scoreboard column labels on screen."""
        for surface, rect in zip(self.label_surface_list, self.label_rect_list):
            self.window.blit(surface, rect)

    def draw_data(self) -> None:
        """Blits all scoreboard data and user row with highlight."""

        # Blits current scoreboard page data on screen.
        for surface, rect in zip(self.data_surface_list, self.data_rect_list):
            self.window.blit(surface, rect)
        # Blits highlighted user row.
        pygame.draw.rect(self.window, GAME_TEXT_LIGHT_BLUE, self.user_row_highlight_rect)
        for surface, rect in zip(self.user_row_surface_list, self.user_row_rect_list):
            self.window.blit(surface, rect)

    def set_column_surface_rect_lists(self) -> (list[tuple[int, int]], list[pygame.Surface], list[pygame.Rect]):
        """Create and return lists for page data pos, surfaces, and rects.

        This method acts like a constructor that is called when a ScoreBoard
        object is instantiated. It uses attribute data and other decided upon
        constants to create a list containing a surface for each item in each
        row (rank, score, name), a list containing the positions desired for
        each surface, and a list containing rect objects (created from the
        surface and pos lists) that will actually be blit to the screen via a
        different method.
        """

        # Create nested list of pos tuples for page data then flatten.
        nested_pos_list = [[(x, y) for x in [120, 420, 500]] for y in range(120, 401, 28)]
        pos_list = [pos for row in nested_pos_list for pos in row]

        # Create nested list of surfaces for page data then flatten.
        nested_surface_list = [[self.data_font.render(str(item).upper(), True, self.data_color)
                                for item in row] for row in self.user_row_page]
        surface_list = [surface for row in nested_surface_list for surface in row]

        # Create list of surface rects for page data, making sure middle column of page data is aligned properly.
        rect_list = [surface.get_rect(midright=pos) if pos[0] == 420 else surface.get_rect(midleft=pos)
                     for surface, pos in zip(surface_list, pos_list)]

        return pos_list, surface_list, rect_list

    def set_user_row_surface_rect_lists(self) -> (pygame.Rect, list[pygame.Surface], list[pygame.Rect]):
        """Return a highlight rect and lists of surfaces and rects for user's row.

        This method acts like a constructor that is called when a ScoreBoard
        object is instantiated. It creates and returns a "highlight" rect, a
        list of surfaces, and a list of rects representing each item in the
        user's row.
        """
        # Creates pos, surface, and rect lists for user row.
        # (There are 3 items in each row and data_rect_list includes all items in all rows on screen,
        # so we need to slice the list to just pull the items in our "user row").
        user_row_pos_list = [rect.center
                             for rect in self.data_rect_list[(self.user_row_index*3):((self.user_row_index*3) + 3)]]
        user_row_surface_list = [self.data_font.render(str(item).upper(), True, GAME_COLOR_BLACK)
                                 for item in self.user_row_page[self.user_row_index]]
        user_row_rect_list = [surface.get_rect(center=pos)
                              for surface, pos in zip(user_row_surface_list, user_row_pos_list)]

        # Creates highlight rect for user row and positions it.
        # (Algorithm for getting width and height arguments:
        # width = right_border x_coord of name_rect (w/ 12 char limit)
        #           - left_border x_coord of rank_rect + extra spacing
        # height = height of rank rect + extra spacing)
        highlight_rect = pygame.Rect(0,
                                     0,
                                     ((680 - user_row_rect_list[0].left) + 20),
                                     (user_row_rect_list[0].height + 10),
                                     )
        highlight_rect.midleft = ((user_row_rect_list[0].left - 10), user_row_rect_list[0].centery - 1)

        return highlight_rect, user_row_surface_list, user_row_rect_list
