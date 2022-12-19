"""Draw high scores screen and check for mouse click events.

This module holds the class responsible for blitting the program's high scores
screen, blitting a scoreboard with pages, blitting buttons to click through
each page, and running an event loop to listen for mouse click events.

Classes:
    HighScoresScreen: Contains high scores screen of program.
"""

import os
import sys
import pygame
from misc.constants import *
from misc.buttons import ArrowButton, TextButton
from misc.saved_data_io_functions import get_score_name_list


class HighScoresScreen(object):
    """Contains all high scores screen content to be blitted to the screen.

    This class contains all the information and content to be blitted to the
    screen as well as a draw method that actually blits everything
    categorized as being in the high score screen. Includes event loop that
    checks for mouse click events. Content in the high scores screen includes:
    the scoreboard (with rank, score, and username columns), a left and right
    arrow to switch between scoreboard screens, and a back button to leave the
    high scores screen event loop and return to the main menu.
    """

    def __init__(self, window: pygame.Surface, width: float, height: float,
                 sfx_bool: str, background: pygame.surface) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.sfx_bool = sfx_bool
        self.background = background
        self.scoreboard = pygame.transform.scale(pygame.Surface.convert(pygame.image.load(
            os.path.join('project_assets', 'backgrounds', 'black_background.png'))), SCORE_BOARD_SIZE)
        self.score_name_list = get_score_name_list()
        self.current_page = 1
        self.page_limit = -(-len(self.score_name_list) // SCORES_PER_PAGE)
        self.caption = 'Snake - High Scores'
        self.text = ''
        self.text_color = GAME_TEXT_LIGHT_BLUE
        self.font = pygame.font.Font(ARCADE_FONT_FILE, SCORE_DATA_FONT_SIZE)
        self.text_pos = (0, 0)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_pos)
        self.running = True

    def run(self) -> None:
        """Run high scores screen event loop.

        Creates arrow buttons to move through each page of the scoreboard, as
        well as a back button to return to the main menu. High scores screen
        event loop is then started. Event loop continuously draws high scores
        screen content to screen and checks for button hover and click events.
        """
        pygame.display.set_caption(self.caption)
        back_button = TextButton(self.window, BACK_BUTTON_POS, TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT, 'BACK',
                                 TEXT_BUTTON_FONT_SIZE)
        prev_button = ArrowButton(self.window, PREV_ARROW_BUTTON_POS, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT, 'left')
        next_button = ArrowButton(self.window, NEXT_ARROW_BUTTON_POS, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT, 'right')

        while self.running:
            mouse_position = pygame.mouse.get_pos()
            event_list = pygame.event.get()

            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONUP:  # Checks if mouse button was clicked.
                    # Checks if cursor was hovering over any buttons when clicked and if so, executes their code.

                    if back_button.is_hovering(mouse_position):
                        back_button.draw_clicked(self.sfx_bool)
                        pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                        self.running = False
                        break
                    elif prev_button.is_hovering(mouse_position) and 1 < self.current_page <= self.page_limit:
                        prev_button.draw_clicked(self.sfx_bool)
                        self.page_changed(direction='prev')
                        pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                    elif next_button.is_hovering(mouse_position) and 1 <= self.current_page < self.page_limit:
                        next_button.draw_clicked(self.sfx_bool)
                        self.page_changed(direction='next')
                        pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                    else:
                        print('nothing was clicked')

                else:
                    pass

            self.draw(mouse_position, back_button, prev_button, next_button)

    def draw(self, mouse_pos: tuple[int, int], button_1: TextButton, button_2: ArrowButton, button_3: ArrowButton,
             ) -> None:
        """Blit all HighScoresScreen content to screen.

        Uses class attributes, internal methods, and entered args to blit the 
        background, a scoreboard background, all of the current page content,
        a back button to return to the main menu, and two arrow buttons used 
        to go through all scoreboard pages available.

        Args:
            mouse_pos: Used to determine which button mouse was hovering over,
                if any.
            button_1: Text button that goes back to main menu.
            button_2: Arrow button that goes to previous page of scoreboard.
            button_3: Arrow button that goes to next page of scoreboard.
        """
        self.window.blit(self.background, BACKGROUND_BLIT_POS)
        self.window.blit(self.scoreboard, SCORE_BOARD_BLIT_POS)
        self.draw_current_page()
        button_1.draw(mouse_pos, self.sfx_bool)
        if self.current_page != 1:
            button_2.draw(mouse_pos, self.sfx_bool)
        if self.current_page != self.page_limit:
            button_3.draw(mouse_pos, self.sfx_bool)
        pygame.display.update()

    def draw_current_page(self) -> None:
        """Organize and blit all data in current scoreboard page.

        This method takes information from attributes that were created in the
        init method and structures them (mostly the score_name_list) into three
        categorical columns (rank, score, name) and eleven rows. The first row
        always being the column labels (RANK, SCORE, NAME), and the other ten
        being the ten rows of (rank, score, name) data allowed on each page.
        """

        # Blits scoreboard column labels on screen.
        self.font = pygame.font.Font(ARCADE_FONT_FILE, SCORE_DATA_LABEL_FONT_SIZE)
        self.text_color = GAME_TEXT_GREEN
        x_pos = 110

        for item in ['RANK', 'SCORE', 'NAME']:
            self.text = item
            self.text_pos = (x_pos, 50)
            self.text_surface = self.font.render(self.text, True, self.text_color)
            if item == 'SCORE':
                self.text_rect = self.text_surface.get_rect(midright=self.text_pos)
                x_pos += 100
            else:
                self.text_rect = self.text_surface.get_rect(midleft=self.text_pos)
                x_pos += 300
            self.window.blit(self.text_surface, self.text_rect)

        # Blits current scoreboard page's data (10 rank, score, name pairs) on screen.
        self.font = pygame.font.Font(ARCADE_FONT_FILE, SCORE_DATA_FONT_SIZE)
        self.text_color = GAME_TEXT_LIGHT_BLUE
        start = (self.current_page - 1) * SCORES_PER_PAGE
        stop = self.current_page * SCORES_PER_PAGE
        rank = start
        y_pos = 90

        for pair in self.score_name_list[start:stop]:
            rank += 1
            score = pair[0]
            name = pair[1].upper()  # (Maybe get rid of .upper() and do type change in init method).
            x_pos = 110

            for item in [rank, score, name]:
                self.text = str(item)
                self.text_pos = (x_pos, y_pos)
                self.text_surface = self.font.render(self.text, True, self.text_color)
                if item == score:
                    self.text_rect = self.text_surface.get_rect(midright=self.text_pos)
                    x_pos += 100
                else:
                    self.text_rect = self.text_surface.get_rect(midleft=self.text_pos)
                    x_pos += 300
                self.window.blit(self.text_surface, self.text_rect)

            y_pos += 30

    def page_changed(self, direction: str) -> None:
        """Change current page in direction specified."""
        if direction == 'prev':
            self.current_page -= 1
        elif direction == 'next':
            self.current_page += 1
        else:
            print('invalid argument entered')
