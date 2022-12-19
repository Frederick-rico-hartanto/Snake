"""Define game options screen, content, and row classes.

This module holds a class responsible for blitting the program's game
options screen and running an event loop to listen for mouse click events,
another class responsible for holding and blitting each game option row, and
another class responsible for blitting and holding all of the content in each
game option row (game option label, all the corresponding options, and left
and right arrow buttons to click through the available options).

Classes:
    GameOptionsRow: Contains all info of a single game option row.
    GameOptionsContent: Contains all content of the game options themselves.
    GameOptionsScreen: Contains game options screen of program.
"""

import sys
import pygame
from misc.constants import *
from misc.buttons import ApplyButton, CutoutArrowButton, TextButton
from misc.saved_data_io_functions import get_file_dict, set_new_user_preferences, update_settings_real_time


class GameOptionRow(object):
    """Contains all info of a single game option row and draws it to screen.

    This class contains all the information and content of a single row which
    includes any game option label entered as an argument, a corresponding
    list of possible options, the currently selected option, and left and
    right buttons to click through the available options. A draw method that
    blits all the content in the row object is also included.
    """

    def __init__(self, window: pygame.Surface, option_label: str, x_pos: int, y_pos: int) -> None:
        self.window = window
        self.option_label = option_label  # Will be the exact key str belonging to the game option.
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.left_button_pos = (x_pos, y_pos)
        self.right_button_pos = (x_pos, y_pos)
        self.option_list = get_file_dict('game_options').get(self.option_label)
        self.set_option = get_file_dict('user_preferences').get(self.option_label)
        self.currently_selected_option = self.set_option
        self.left_button = CutoutArrowButton(self.window, self.left_button_pos, CUTOUT_ARROW_BUTTON_WIDTH,
                                             CUTOUT_ARROW_BUTTON_HEIGHT, 'left')
        self.right_button = CutoutArrowButton(self.window, self.right_button_pos, CUTOUT_ARROW_BUTTON_WIDTH,
                                              CUTOUT_ARROW_BUTTON_HEIGHT, 'right')
        self.left_button_exists = False
        self.right_button_exists = False

    def draw(self, mouse_pos: tuple[int, int], sfx_bool: str) -> None:
        """Blit all GameOptionRow content to screen.

        Uses class attributes and entered args to blit the GameOptionRow's 
        game option label, the currently selected option, and left and right
        arrow buttons to click through the available options.

        Args:
            mouse_pos: Used to determine which button mouse was hovering over,
                if any.
            sfx_bool: A string containing 'True' or 'False' used to determine
                if arrow buttons should activate their hover and click sfx
                when activated.
        """

        # Blit game option label.
        self.x_pos = 70
        label_font = pygame.font.Font(BUBBLE_FONT_FILE, GAME_OPTIONS_LABEL_FONT_SIZE)
        label_pos = (self.x_pos, self.y_pos)
        label_surface = label_font.render(self.option_label, True, GAME_TEXT_BLUE)
        label_rect = label_surface.get_rect(midleft=label_pos)
        self.window.blit(label_surface, label_rect)
        self.x_pos += 300

        # Blit left arrow if currently selected option is > index 0.
        self.left_button_pos = (self.x_pos, self.y_pos)
        if self.currently_selected_option != self.option_list[0]:
            self.left_button.update_button_pos(self.left_button_pos)
            self.left_button.draw(mouse_pos, sfx_bool)
            self.left_button_exists = True
        else:
            self.left_button_exists = False
        self.x_pos += (GAME_OPTIONS_OPTION_SPACER + self.left_button.width)

        # Blit currently selected option.
        option_font = pygame.font.Font(ARCADE_FONT_FILE, GAME_OPTIONS_OPTION_FONT_SIZE)
        option_pos = (self.x_pos, self.y_pos)
        currently_selected_option_clean = (self.currently_selected_option.split('~')[0])
        option_surface = option_font.render(currently_selected_option_clean, True, GAME_TEXT_LIGHT_BLUE)
        option_rect = option_surface.get_rect(midleft=option_pos)
        self.window.blit(option_surface, option_rect)
        self.x_pos += (option_rect.width + GAME_OPTIONS_OPTION_SPACER)

        # Blit right arrow if currently selected option is < index -1.
        self.right_button_pos = (self.x_pos, self.y_pos)
        if self.currently_selected_option != self.option_list[-1]:
            self.right_button.update_button_pos(self.right_button_pos)
            self.right_button.draw(mouse_pos, sfx_bool)
            self.right_button_exists = True
        else:
            self.right_button_exists = False


class GameOptionsContent(object):
    """Acts like a container for all of the game options rows

    This class creates a list of GameOptionRow objects that each hold all of
    the content for each game option, manages all of the rows objects and
    their location on the screen, draws each row object, manages all code
    pertaining to drawing each row object's arrow buttons, and retrieves a
    list of the options currently selected.
    """

    def __init__(self, window: pygame.Surface) -> None:
        self.window = window
        self.x_pos = 100
        self.y_pos = 70
        # Makes a list of row objects that each accept a game option dictionary key.
        self.list_of_rows = [GameOptionRow(window, option_key, self.x_pos, self.y_increment())
                             for option_key in get_file_dict('game_options')]

    def y_increment(self) -> int:
        """Increment y_pos attribute (for spacing each GameOptionRow)."""
        self.y_pos += 45
        return self.y_pos

    def make_new_user_preferences_list(self) -> list[str]:
        """Return list of strings containing each label and selected option.

        Creates a new list of f-strings, each representing one line of the
        user_preferences.txt file. Each line contains a game option label and
        its currently selected option.

        Returns:
            new_pref_list: List of f-strings in same format as each line in
                user_preferences.txt file.
        """
        new_pref_list = []

        for row_object in self.list_of_rows:
            new_pref_list.append(f'{row_object.option_label}: {row_object.currently_selected_option}')

        return new_pref_list

    def arrows_is_hovering(self, mouse_pos: tuple[int, int]) -> bool:
        """Return bool indicating whether any arrows are being hovered over.

        This function iterates through the list of GameOptionRow objects and
        checks if either of the row object's arrow buttons are being hovered
        over.
        """
        is_hovering = False
        for row_object in self.list_of_rows:
            if row_object.left_button_exists or row_object.right_button_exists:
                if row_object.left_button.is_hovering(mouse_pos) or row_object.right_button.is_hovering(mouse_pos):
                    is_hovering = True
                    break
        return is_hovering

    def arrows_draw_clicked(self, mouse_pos: tuple[int, int], sfx_bool: str) -> None:
        """Check if any arrow buttons were clicked and draws them.

        Iterates through option row object list and draws the clicked version
        of any arrow button that was clicked and then changes the object's
        currently_selected_option attribute to the next or previous option
        depending on arrow direction clicked.

        Args:
            mouse_pos: Used to determine which button mouse was hovering over,
                if any.
            sfx_bool: Used to determine if a clicked arrow button should also
                make a click sfx.
        """
        for row_object in self.list_of_rows:
            if row_object.left_button_exists and row_object.left_button.is_hovering(mouse_pos):
                row_object.left_button.draw_clicked(sfx_bool)
                # (Maybe put this in game_option_row object as a method and then call it here).
                row_object.currently_selected_option = \
                    row_object.option_list[(row_object.option_list.index(row_object.currently_selected_option)) - 1]
            elif row_object.right_button_exists and row_object.right_button.is_hovering(mouse_pos):
                row_object.right_button.draw_clicked(sfx_bool)
                # (Maybe put this in game_option_row object as a method and then call it here).
                row_object.currently_selected_option = \
                    row_object.option_list[(row_object.option_list.index(row_object.currently_selected_option)) + 1]
            else:
                pass

    def draw(self, mouse_pos: tuple[int, int], sfx_bool: str) -> None:
        """Call draw method for each game option row in list of rows."""
        for row_object in self.list_of_rows:
            row_object.draw(mouse_pos, sfx_bool)


class GameOptionsScreen(object):
    """Contains all game options screen content to be blitted to the screen.

    This class contains all the information and content to be blitted to the
    screen as well as a draw method that actually blits everything
    categorized as being in the game options screen. Includes event loop that
    checks for mouse click events. Content in the game options screen
    includes: a column of game option labels (sound, music, grid, border
    theme, background, and snake skin), a column of currently selected options
    corresponding to each game option label, left and right arrow buttons that
    allow user to click through all of the available options for each game
    option label, an apply button that takes all of the currently selected
    options and saves them in the game_options.txt file in order to be used in
    other parts of the program, and a back button to leave the game options
    screen event loop and return to the main menu.
    """

    def __init__(self, window: pygame.Surface, width: int, height: int, sfx_bool: str, music_bool: str,
                 background: pygame.Surface) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.sfx_bool = sfx_bool
        self.music_bool = music_bool
        self.background = background
        self.caption = 'Snake - Game Options'
        self.title_color = GAME_TEXT_BLUE
        self.title = 'GAME OPTIONS'
        self.title_font = pygame.font.Font(BUBBLE_FONT_FILE, GAME_OPTIONS_TITLE_FONT_SIZE)
        self.title_pos = GAME_OPTIONS_TITLE_POS
        self.title_surface = self.title_font.render(self.title, True, self.title_color)
        self.title_rect = self.title_surface.get_rect(center=self.title_pos)
        self.running = True

    def run(self) -> None:
        """Run game options screen event loop.

        This method creates back button, apply button, and a 
        GameOptionsContent instance, then starts an event loop to check if 
        either button or any arrow buttons in game_options have been pressed.
        """
        pygame.display.set_caption(self.caption)
        back_button = TextButton(self.window, BACK_BUTTON_POS, TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT,
                                 BACK_BUTTON_TEXT, TEXT_BUTTON_FONT_SIZE)
        apply_button = ApplyButton(self.window, APPLY_BUTTON_POS, TEXT_BUTTON_WIDTH, TEXT_BUTTON_HEIGHT,
                                   APPLY_BUTTON_TEXT, TEXT_BUTTON_FONT_SIZE)
        game_options = GameOptionsContent(self.window)

        while self.running:
            mouse_position = pygame.mouse.get_pos()
            event_list = pygame.event.get()

            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Checks if mouse button was clicked.
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Checks if cursor was hovering over any buttons when clicked and if so, executes its code.

                    if back_button.is_hovering(mouse_position):
                        back_button.draw_clicked(self.sfx_bool)
                        pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                        self.running = False
                        break
                    elif apply_button.is_hovering(mouse_position):
                        apply_button.draw_clicked()
                        pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                        old_user_preferences_dict = get_file_dict('user_preferences')
                        new_user_preferences_list = game_options.make_new_user_preferences_list()
                        set_new_user_preferences(new_user_preferences_list)
                        self.sfx_bool, self.music_bool, self.background = \
                            update_settings_real_time(self.width, self.height, old_user_preferences_dict)
                    elif game_options.arrows_is_hovering(mouse_position):
                        game_options.arrows_draw_clicked(mouse_position, self.sfx_bool)
                        pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                    else:
                        print('nothing was clicked')

                else:
                    pass

            self.draw(mouse_position, back_button, apply_button, game_options)

    def draw(self, mouse_pos: tuple[int, int], button_1: TextButton, button_2: ApplyButton, options: GameOptionsContent,
             ) -> None:
        """Blit all GameOptionsScreen content to screen.

        Uses class attributes and entered args to blit a background, all game
        option rows (which include a game option label, the currently selected
        option, and arrows to click through the available options), a back
        button, an apply button, and a game options title to the screen.

        Args:
            mouse_pos: Used to determine which button mouse was hovering over,
                if any.
            button_1: Text button that goes back to main menu.
            button_2: Apply button that dynamically applies changes to user
                preferences.
            options: Holds all game option rows.
        """
        self.window.blit(self.background, BACKGROUND_BLIT_POS)
        self.window.blit(self.title_surface, self.title_rect)
        for screen_item in [button_1, button_2, options]:
            screen_item.draw(mouse_pos, self.sfx_bool)
        pygame.display.update()
