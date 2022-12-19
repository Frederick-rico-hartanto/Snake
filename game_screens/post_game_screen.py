"""Define post game screen class of program.

This module holds the class responsible for blitting the program's post game
screen. The screen include two versions shown under different circumstances.

Classes:
    PostGameScreen: Contains post game screen of program.
"""

import os
import sys
import pygame
from misc.constants import *
from game_objects.score_board import ScoreBoard
from misc.buttons import TextButton


class PostGameScreen(object):
    """Contains all post game screen content to be blitted to the screen.

    This class contains all the information and content to be blitted to the
    screen as well as a draw method that actually blits everything
    categorized as being in the post game screen. Includes event loop that
    checks for mouse click events. Content in the post game screen includes:
    the background, the border ui (empty until new game is started), main menu
    button to return to the main menu, and a play again button to reset and
    start a new game. Depending on if a score was saved from the last game, a
    scoreboard showing the page of the user's (rank, score, name) row along
    with a "high scores" title label above it, is blit to the screen. If no
    score was saved, the post game screen is displayed as a simple black
    background with the "snake" title in large font size.
    """

    def __init__(self, window: pygame.Surface, border_ui, bg_dimensions: tuple, bg_pos: tuple, sfx_bool: str,
                 score_saved: bool, user_score: int, user_name: str) -> None:
        self.window = window
        self.border_ui = border_ui
        self.bg_dimensions = bg_dimensions
        self.bg_pos = bg_pos
        self.sfx_bool = sfx_bool
        self.score_saved = score_saved
        self.user_score = user_score
        self.user_name = user_name
        self.background = pygame.transform.scale(pygame.Surface.convert(pygame.image.load(
            os.path.join('project_assets', 'backgrounds', 'black_background.png'))), self.bg_dimensions)
        self.play_again = False
        self.caption = 'Snake - Scoreboard' if self.score_saved else 'Snake - Pre-Game Screen'

        self.title = 'SNAKE'
        self.title_font_size = POST_GAME_TITLE_FONT_SIZE
        self.title_font = pygame.font.Font(BUBBLE_FONT_FILE, self.title_font_size)
        self.title_color = GAME_TEXT_BLUE
        self.title_pos = POST_GAME_TITLE_POS
        self.title_surface = self.title_font.render(self.title, True, self.title_color)
        self.title_rect = self.title_surface.get_rect(center=self.title_pos)

        self.highscores_title = 'HIGH SCORES'
        self.highscores_title_font_size = POST_GAME_SCORES_TITLE_FONT_SIZE
        self.highscores_title_font = pygame.font.Font(ARCADE_FONT_FILE, self.highscores_title_font_size)
        self.highscores_title_color = GAME_TEXT_BLUE
        self.highscores_title_pos = POST_GAME_SCORES_TITLE_POS
        self.highscores_title_surface = self.highscores_title_font.render(self.highscores_title,
                                                                          True,
                                                                          self.highscores_title_color)
        self.highscores_title_rect = self.highscores_title_surface.get_rect(center=self.highscores_title_pos)

        self.score_board = ScoreBoard(self.window, self.user_score, self.user_name) if self.score_saved else None
        self.running = True

    def run(self) -> None:
        """Run post game screen event loop.

        Creates main menu button to return to the main menu, as well as a play
        again button to start a new game. Post game screen event loop is then
        started. Event loop continuously draws post game screen content to
        screen and checks for button hover and click events.
        """
        pygame.display.set_caption(self.caption)
        main_menu_button = TextButton(self.window, MAIN_MENU_BUTTON_POS, MAIN_MENU_BUTTON_WIDTH,
                                      POST_GAME_BUTTON_HEIGHT, MAIN_MENU_BUTTON_TEXT, POST_GAME_BUTTON_FONT_SIZE)
        play_again_button = TextButton(self.window, PLAY_AGAIN_BUTTON_POS, PLAY_AGAIN_BUTTON_WIDTH,
                                       POST_GAME_BUTTON_HEIGHT, PLAY_AGAIN_BUTTON_TEXT, POST_GAME_BUTTON_FONT_SIZE,
                                       start_sfx='_start_game')

        while self.running:
            mouse_position = pygame.mouse.get_pos()
            event_list = pygame.event.get()

            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONUP:  # Checks if mouse button was clicked.
                    # Checks if cursor was hovering over a button when clicked and if so, executes their code.

                    if main_menu_button.is_hovering(mouse_position):
                        main_menu_button.draw_clicked(self.sfx_bool)
                        pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                        self.running = False
                        break
                    elif play_again_button.is_hovering(mouse_position):
                        play_again_button.draw_clicked(self.sfx_bool)
                        pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                        self.play_again = True
                        self.running = False
                        break
                    else:
                        print('nothing was clicked..')

            self.draw(mouse_position, main_menu_button, play_again_button)

    def draw(self, mouse_pos: tuple[int, int], main_menu_button: TextButton, play_again_button: TextButton) -> None:
        """Blit all PostGameScreen content to screen.

        Uses class attributes and entered args to blit the background, the
        empty border ui, a main menu button to return to the main menu, a play
        again button to start a new game, and depending on if the previous
        game's score was saved, a highscores title and scoreboard. If the
        score was not saved, a large font snake title is displayed.

        Args:
            mouse_pos: Used to determine which button mouse was hovering over,
                if any.
            main_menu_button: Text button that goes back to main menu.
            play_again_button: Text button that starts new game.
        """
        self.window.blit(self.background, self.bg_pos)
        self.border_ui.draw()
        if self.score_saved:
            self.window.blit(self.highscores_title_surface, self.highscores_title_rect)
            self.score_board.draw()
        else:
            self.window.blit(self.title_surface, self.title_rect)
        main_menu_button.draw(mouse_pos, self.sfx_bool)
        play_again_button.draw(mouse_pos, self.sfx_bool)
        pygame.display.update()
