"""Define game over screen class of program.

This module holds the class responsible for blitting the program's game over
screen, called after snake game end conditions are met.

Classes:
    GameOverScreen: Contains game over screen of program.
"""

import os
import sys
import pygame
from misc.buttons import TextButton
from misc.constants import *
from misc.saved_data_io_functions import save_new_player_score
from misc.text_box import TextBox


class GameOverScreen(object):
    """Contains all game over screen content to be blitted to the screen.

    This class contains all the information and content to be blitted to the
    screen as well as a draw method that actually blits everything
    categorized as being in the game over screen. Includes event loop that
    checks for mouse click events. Content in the game over screen includes:
    a game over title, the user's score, a continue button, and if the user's
    score was over 0, both a "no thanks" button and an input name caption next
    to a text box.
    """

    def __init__(self, window: pygame.Surface, width: int, height: int, sfx_bool: str, music_bool: str,
                 bg_dimensions: tuple[int, int], bg_pos: tuple[int, int], user_score: int) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.sfx_bool = sfx_bool
        self.music_bool = music_bool
        self.bg_dimensions = bg_dimensions
        self.bg_pos = bg_pos
        self.background = pygame.transform.scale(pygame.Surface.convert(pygame.image.load(
            os.path.join('project_assets', 'backgrounds', 'black_background.png'))), self.bg_dimensions)
        self.user_score = user_score
        self.name_input = 'null' if self.user_score == 0 else ''
        self.caption = 'Snake - Game Over!'
        self.game_over_sfx = pygame.mixer.Sound(os.path.join('project_assets', 'sfx', 'game_over.wav'))
        self.click_sfx = pygame.mixer.Sound(os.path.join('project_assets', 'sfx', 'button_click.wav'))
        self.title = 'GAME OVER'
        self.title_font_size = GAME_OVER_TITLE_FONT_SIZE
        self.title_font = pygame.font.Font(ARCADE_FONT_FILE, self.title_font_size)
        self.title_color = GAME_TEXT_BLUE
        self.title_pos = GAME_OVER_TITLE_POS
        self.title_surface = self.title_font.render(self.title, True, self.title_color)
        self.title_rect = self.title_surface.get_rect(center=self.title_pos)
        self.text_list = ['Score:', f'{self.user_score}', 'Enter your name:']
        self.text_font_size = GAME_OVER_TEXT_FONT_SIZE
        self.text_font = pygame.font.Font(ARCADE_FONT_FILE, self.text_font_size)
        self.text_color_list = [GAME_TEXT_GREEN, GAME_TEXT_LIGHT_BLUE, GAME_TEXT_GREEN]
        self.text_pos_list = [(375, 225), (475, 225), (375, 300)]
        self.text_surface_list = [(self.text_font.render(self.text_list[index], True, self.text_color_list[index]))
                                  for index in range(len(self.text_list))]
        self.text_rect_list = [surface.get_rect(midright=pos)
                               for surface, pos in zip(self.text_surface_list, self.text_pos_list)]
        self.score_saved_bool = False
        self.running = True

    def run(self) -> None:
        """Run game over screen event loop.

        Creates no thanks button to skip option to input name and save to high
        scores text file, continue button to go on to post game screen (or if
        user score is over 0, to save inputted name with score to high scores
        text file), and a name input text box to allow user to input a name if
        they wish to save their score. Game over screen event loop is then
        started. Event loop continuously draws game over screen content to
        screen and checks for button hover and click events.
        """
        pygame.time.delay(GAME_OVER_SCREEN_TIME_DELAY)
        if self.sfx_bool == 'True':
            self.game_over_sfx.play()
        pygame.display.set_caption(self.caption)
        no_thanks_button = TextButton(self.window, NO_THANKS_BUTTON_POS, NO_THANKS_BUTTON_WIDTH,
                                      GAME_OVER_BUTTON_HEIGHT, NO_THANKS_BUTTON_TEXT, GAME_OVER_BUTTON_FONT_SIZE)
        continue_button = TextButton(self.window, CONTINUE_BUTTON_POS, CONTINUE_BUTTON_WIDTH, GAME_OVER_BUTTON_HEIGHT,
                                     CONTINUE_BUTTON_TEXT, GAME_OVER_BUTTON_FONT_SIZE)
        name_input_box = TextBox(self.window, INPUT_BOX_POS, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT, GAME_COLOR_STONE_GREY,
                                 INPUT_BOX_FONT_SIZE, GAME_TEXT_LIGHT_BLUE)

        while self.running:
            mouse_position = pygame.mouse.get_pos()
            event_list = pygame.event.get()

            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONUP:  # Checks if mouse button was clicked.
                    # Checks if cursor was hovering over a widget when clicked and if so, executes their code.

                    if no_thanks_button.is_hovering(mouse_position) and self.user_score > 0:
                        no_thanks_button.draw_clicked(self.sfx_bool)
                        pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                        self.running = False
                        break
                    elif continue_button.is_hovering(mouse_position):
                        if 0 < len(self.name_input) <= TEXT_BOX_CHAR_LIMIT:
                            continue_button.draw_clicked(self.sfx_bool)
                            pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                            if self.user_score > 0:
                                save_new_player_score(self.user_score, self.name_input)
                                self.score_saved_bool = True
                            self.running = False
                            break
                        else:
                            print('enter a name to continue')
                    elif name_input_box.is_hovering(mouse_position):
                        if self.sfx_bool == 'True' and not name_input_box.selected:
                            self.click_sfx.play()
                        name_input_box.selected = True
                    else:
                        name_input_box.selected = False
                        print('nothing was clicked..')

                # Checks if any letter keys were pressed while the input box was selected.
                elif event.type == pygame.KEYDOWN and name_input_box.selected:
                    key_pressed = pygame.key.name(event.key)
                    if key_pressed.isalpha() and len(key_pressed) == 1:
                        name_input_box.add_char(key_pressed)
                        self.name_input = name_input_box.text
                    elif event.key == pygame.K_BACKSPACE:
                        name_input_box.remove_char()
                        self.name_input = name_input_box.text
                    else:
                        print('key pressed does nothing')
                else:
                    pass

            self.draw(mouse_position, no_thanks_button, continue_button, name_input_box)

    def draw(self, mouse_pos: tuple[int, int], no_thanks_button: TextButton, continue_button: TextButton,
             name_input_box: TextBox) -> None:
        """Blit all GameOverScreen content to screen.

        Uses class attributes and entered args to blit the background, the
        user's score and a label next to it, the continue button, and if the
        user's score is over 0, an "enter your name" label, a text input box,
        and a "no thanks" button.

        Args:
            mouse_pos: Used to determine which button mouse was hovering over,
                if any.
            no_thanks_button: Text button that goes straight to the post game
                screen without saving score.
            continue_button: Text button that saves user score before going to
                the post game screen.
            name_input_box: Text box to let user enter a name.
        """
        self.window.blit(self.background, self.bg_pos)
        # Draw game over title at top.
        self.window.blit(self.title_surface, self.title_rect)
        # Draw score label and user score.
        for surface, rect in zip(self.text_surface_list[:2], self.text_rect_list[:2]):
            self.window.blit(surface, rect)
        # Draw enter your name label, its text box, and no_thanks_button if user score is more than 0.
        if self.user_score > 0:
            self.window.blit(self.text_surface_list[2], self.text_rect_list[2])
            name_input_box.draw(mouse_pos, self.sfx_bool)
            no_thanks_button.draw(mouse_pos, self.sfx_bool)
        continue_button.draw(mouse_pos, self.sfx_bool)
        pygame.display.update()
