"""Initialize program code, gui, and game splash screen.

This module holds the classes responsible for setting up the snake game
program, running it, and blitting the first screen (SplashScreen) of the
program gui. RootWindow is the game window itself. It has a greeting screen
but then calls MainMenu (MainMenu internally has code that executes when
called).

Classes:
    SplashScreen: Contains splash screen content.
    RootWindow: Contains program initialization code and other important info.
"""

import os
import sys
import pygame
from misc.constants import *
from menu_screens.main_menu import MainMenu
from misc.saved_data_io_functions import update_settings_real_time


class SplashScreen(object):
    """Contains all content to be blitted to the splash screen.

    This class contains all the information and content to be blitted to the
    screen as well as a draw method that actually blits everything
    categorized as being in the splash screen.
    """

    def __init__(self, window: pygame.Surface, width: int, height: int) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.background = pygame.transform.scale(pygame.Surface.convert(pygame.image.load(
            os.path.join('project_assets',
                         'backgrounds',
                         'black_background.png',
                         ))), (self.width, self.height))
        self.text_color = GAME_TEXT_BLUE
        self.title = 'SNAKE'
        self.title_font = pygame.font.Font(BUBBLE_FONT_FILE, SPLASH_TITLE_FONT_SIZE)
        self.title_pos = ((self.width / 2), SPLASH_TITLE_Y_POS)
        self.title_surface = self.title_font.render(self.title, True, self.text_color)
        self.title_rect = self.title_surface.get_rect(center=self.title_pos)
        self.caption1 = '( Press Any Key to Start ... )'
        self.caption1_font = pygame.font.Font(BUBBLE_FONT_FILE, SPLASH_CAPTION1_FONT_SIZE)
        self.caption1_pos = (self.width / 2, SPLASH_CAPTION1_Y_POS)
        self.caption1_surface = self.caption1_font.render(self.caption1, True, self.text_color)
        self.caption1_rect = self.caption1_surface.get_rect(center=self.caption1_pos)

    def draw(self) -> None:
        """Blit SplashScreen content to screen.

        Uses class attributes to blit a black background, the snake title, and
        a subtitle telling the user to press any key to get to the next screen.
        """
        self.window.blit(self.background, BACKGROUND_BLIT_POS)
        self.window.blit(self.title_surface, self.title_rect)
        self.window.blit(self.caption1_surface, self.caption1_rect)
        pygame.display.update()


class RootWindow(object):
    """Contains all initialization and program setup code.

    This class initializes pygame and retrieves a bunch of information to be
    used later in the other screens of the program. Includes main program loop
    in its run method.
    """

    def __init__(self) -> None:
        pygame.init()
        self.width = GAME_WINDOW_WIDTH
        self.height = GAME_WINDOW_HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height))
        self.caption = 'Snake'
        self.menu_music = os.path.join('project_assets', 'music', 'menu_music.ogg')
        self.button_click_sfx = pygame.mixer.Sound(os.path.join('project_assets', 'sfx', 'button_click.wav'))
        self.sfx_bool = ''
        self.music_bool = ''
        self.background = ''
        self.running = True

    def run(self) -> None:
        """Run snake program's main event loop.

        Retrieves multiple saved user preferences then starts up the main
        "outer" event loop of program. Event loop draws SplashScreen instance
        to screen and when a key is pressed, instance of MainMenu is created
        and its run method is called.
        """
        pygame.display.set_caption(self.caption)
        pygame.mixer.music.load(self.menu_music)
        self.sfx_bool, self.music_bool, self.background = update_settings_real_time(self.width, self.height)
        greeting_screen = SplashScreen(self.window, self.width, self.height)

        while self.running:
            greeting_screen.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                    if self.sfx_bool == 'True':
                        self.button_click_sfx.play()
                    main_menu = MainMenu(self.window, self.width, self.height,
                                         self.sfx_bool, self.music_bool, self.background)
                    main_menu.run()
                    self.running = False
                else:
                    pass

        pygame.quit()
        sys.exit()
