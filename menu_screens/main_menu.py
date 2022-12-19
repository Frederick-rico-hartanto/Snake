"""Draw main menu and check for mouse click events.

This module holds the class responsible for blitting the program's main menu,
all of its button options, and runs an event loop to listen for mouse click
events.

Classes:
    MainMenu: Contains main menu of program.
"""

import os
import pygame
from misc.constants import *
from misc.buttons import TextButton
from game_screens.snake_game_screen import SnakeGameScreen
from menu_screens.high_scores_screen import HighScoresScreen
from menu_screens.game_options_screen import GameOptionsScreen
from misc.saved_data_io_functions import get_file_dict, update_settings_real_time


class MainMenu(object):
    """Contains all main menu content to be blitted to the screen.

    This class contains all the information and content to be blitted to the
    screen as well as a draw method that actually blits everything
    categorized as being in the main menu. Main menu content includes 4 button
    options (start game, high scores, game options, and quit). Each button
    calls each option's corresponding screen class when selected.
    """

    def __init__(self, window: pygame.Surface, width: int, height: int, sfx_bool: str, music_bool: str,
                 background: pygame.Surface) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.sfx_bool = sfx_bool
        self.music_bool = music_bool
        self.background = background
        self.caption = 'Snake - Main Menu'
        self.title = 'SNAKE'
        self.title_color = GAME_TEXT_BLUE
        self.font = pygame.font.Font(BUBBLE_FONT_FILE, MENU_TITLE_FONT_SIZE)
        self.title_pos = (self.width / 2, MENU_TITLE_Y_POS)
        self.title_surface = self.font.render(self.title, True, self.title_color)
        self.title_rect = self.title_surface.get_rect(center=self.title_pos)
        self.menu_music = os.path.join('project_assets', 'music', 'menu_music.ogg')
        self.running = True

    def run(self) -> None:
        """Run main menu event loop.

        Creates menu buttons (start game, high scores, game options, and
        quit), then starts main menu event loop from which other screens and
        their event loops will be called. Event loop continuously draws main
        menu contents to screen and checks for button hovering, until a button
        is selected, then runs each button's corresponding screen code (i.e.
        if high_scores_button is pressed, the button clicked method is called,
        an instance of the HighScoresScreen class is created, and its run
        method is called).
        """
        pygame.display.set_caption(self.caption)
        start_game_button = TextButton(self.window, START_BUTTON_POS, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
                                       START_BUTTON_TEXT, MENU_BUTTONS_FONT_SIZE, start_sfx='_start_game')
        high_scores_button = TextButton(self.window, HIGH_SCORES_BUTTON_POS, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
                                        HIGH_SCORES_BUTTON_TEXT, MENU_BUTTONS_FONT_SIZE)
        game_options_button = TextButton(self.window, GAME_OPTIONS_BUTTON_POS, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
                                         GAME_OPTIONS_BUTTON_TEXT, MENU_BUTTONS_FONT_SIZE)
        quit_button = TextButton(self.window, QUIT_BUTTON_POS, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
                                 QUIT_BUTTON_TEXT, MENU_BUTTONS_FONT_SIZE)

        while self.running:
            mouse_position = pygame.mouse.get_pos()
            event_list = pygame.event.get()

            for event in event_list:
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                elif event.type == pygame.MOUSEBUTTONUP:  # Checks if mouse button was clicked.
                    # Checks if cursor was hovering over any menu buttons when clicked and if so, executes their code.

                    if start_game_button.is_hovering(mouse_position):
                        start_game_button.draw_clicked(self.sfx_bool)
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                        game = SnakeGameScreen(self.window, self.width, self.height, self.sfx_bool, self.music_bool,
                                               self.background)
                        game.run()
                        pygame.display.set_caption(self.caption)
                        pygame.mixer.music.load(self.menu_music)
                        if self.music_bool == 'True':
                            pygame.mixer.music.play(-1)
                    elif high_scores_button.is_hovering(mouse_position):
                        high_scores_button.draw_clicked(self.sfx_bool)
                        pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                        high_scores = HighScoresScreen(self.window, self.width, self.height, self.sfx_bool,
                                                       self.background)
                        high_scores.run()
                        pygame.display.set_caption(self.caption)
                    elif game_options_button.is_hovering(mouse_position):
                        game_options_button.draw_clicked(self.sfx_bool)
                        pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                        game_options = GameOptionsScreen(self.window, self.width, self.height, self.sfx_bool,
                                                         self.music_bool, self.background)
                        game_options.run()
                        pygame.display.set_caption(self.caption)
                        self.sfx_bool, self.music_bool, self.background = \
                            update_settings_real_time(self.width, self.height, get_file_dict('user_preferences'))
                    elif quit_button.is_hovering(mouse_position):
                        pygame.mixer.music.stop()
                        quit_button.draw_clicked(self.sfx_bool)
                        pygame.time.delay(QUIT_BUTTON_CLICK_TIME_DELAY)
                        self.running = False
                        break
                    else:
                        print('nothing was clicked..')

                else:
                    pass

            self.draw(mouse_position, start_game_button, high_scores_button, game_options_button, quit_button)

    def draw(self, mouse_pos: tuple[int, int], button_1: TextButton, button_2: TextButton, button_3: TextButton,
             button_4: TextButton) -> None:
        """Blit all MainMenu content to screen.

        Uses class attributes and entered args to blit a background, the snake
        title, and all of the menu buttons to the screen.

        Args:
            mouse_pos: Used to determine which button the mouse cursor was
                hovering over, if any.
            button_1: One of four menu buttons.
            button_2: One of four menu buttons.
            button_3: One of four menu buttons.
            button_4: One of four menu buttons.
        """
        self.window.blit(self.background, BACKGROUND_BLIT_POS)
        self.window.blit(self.title_surface, self.title_rect)
        for button in [button_1, button_2, button_3, button_4]:
            button.draw(mouse_pos, self.sfx_bool)
        pygame.display.update()
