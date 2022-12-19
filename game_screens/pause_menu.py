"""Define pause menu pop up "mini screen".

This module holds the class responsible for blitting the in-game's pause menu,
used for pausing the game and changing limited game settings while user is
playing.

Classes:
    PauseMenu: Gives player ability to pause game and access basic settings.
"""

import os
import sys
import pygame
from misc.constants import *


class PauseMenu(object):
    """Allows user ability to pause game and toggle music and sfx on/off.

    This class acts like a mini screen, with its own event handling and loop,
    that gets brought up when game is paused by user. Pause menu includes
    4 menu options: continue (which simply breaks out of pause menu event loop
    and returns to the game), quit (which breaks user out of event loop and
    returns to the main menu, not saving anything), sfx (setting with on and
    off options accessed via left and right arrow keys), and music (setting
    with on/off options accessed via left and right arrow keys).
    """

    def __init__(self, window: pygame.Surface, width: int, height: int, sfx_bool: str, music_bool: str,
                 music_not_begun_yet: bool) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.sfx_bool = sfx_bool
        self.music_bool = music_bool
        self.music_not_begun_yet = music_not_begun_yet
        self.caption = 'Snake - Paused'
        self.background = pygame.transform.scale(pygame.Surface.convert(pygame.image.load(
            os.path.join('project_assets', 'backgrounds', 'black_background.png'))), PAUSE_MENU_DIMENSIONS)
        self.font_size = PAUSE_MENU_FONT_SIZE
        self.text_font = pygame.font.Font(ARCADE_FONT_FILE, self.font_size)
        self.text_list = ['CONTINUE',
                          f'SFX      {"ON" if self.sfx_bool == "True" else "OFF"}',
                          f'MUSIC    {"ON" if self.music_bool == "True" else "OFF"}',
                          'QUIT']
        self.text_pos_list = [(290, 175), (290, 225), (290, 275), (290, 325)]
        self.text_surface_list = [(self.text_font.render(self.text_list[index], True, GAME_TEXT_LIGHT_BLUE))
                                  for index in range(len(self.text_list))]
        self.text_rect_list = [surface.get_rect(midleft=pos)
                               for surface, pos in zip(self.text_surface_list, self.text_pos_list)]
        self.current_index = 0
        self.button_hover_sfx = pygame.mixer.Sound(os.path.join('project_assets', 'sfx', 'button_hover.wav'))
        self.button_click_sfx = pygame.mixer.Sound(os.path.join('project_assets', 'sfx', 'button_click.wav'))
        self.button_game_pause_sfx = pygame.mixer.Sound(os.path.join('project_assets', 'sfx', 'game_pause.wav'))
        self.button_game_unpause_sfx = pygame.mixer.Sound(os.path.join('project_assets', 'sfx', 'game_unpause.wav'))
        self.start_of_pause = pygame.time.get_ticks()
        self.total_time_paused = 0
        self.quit_to_main = False
        self.running = True

    def run(self) -> None:
        """Run pause menu event loop.

        Lowers volume before pause menu event loop is started. Event loop
        continuously draws the four menu options and checks for arrow key down
        events in order to highlight currently "hovered" over option.
        """
        pygame.display.set_caption(self.caption)
        if self.sfx_bool == 'True':
            self.button_game_pause_sfx.play()
        # Decrease volume of music.
        pygame.mixer.music.set_volume(PAUSE_MENU_VOLUME)

        while self.running:
            event_list = pygame.event.get()

            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Checks for esc button press (same function as unpause/continue).
                    if event.key == pygame.K_ESCAPE:
                        if self.sfx_bool == 'True':
                            self.button_game_unpause_sfx.play()
                        self.total_time_paused = pygame.time.get_ticks() - self.start_of_pause
                        self.running = False
                        break
                    # Checks for enter button press.
                    elif event.key == pygame.K_RETURN:
                        # Unpause/continue.
                        if self.text_list[self.current_index].split()[0] == 'CONTINUE':
                            if self.sfx_bool == 'True':
                                self.button_game_unpause_sfx.play()
                            pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                            self.total_time_paused = pygame.time.get_ticks() - self.start_of_pause
                            self.running = False
                            break
                        # Quit and return to main menu.
                        elif self.text_list[self.current_index].split()[0] == 'QUIT':
                            if self.sfx_bool == 'True':
                                self.button_click_sfx.play()
                            pygame.time.delay(BUTTON_CLICK_TIME_DELAY)
                            self.quit_to_main = True
                            self.running = False
                            break
                        else:
                            print('nothing happened..')
                    # Checks for up and down key press.
                    elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                        self.selected_option_update(event.key)
                    # Checks for left and right key press.
                    elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        selected_option = self.text_list[self.current_index].split()[0]
                        if selected_option in ['SFX', 'MUSIC']:
                            self.sfx_music_update(selected_option)
                    else:
                        print('key pressed does nothing')
                else:
                    pass

            self.draw()

    def draw(self) -> None:
        """Blits all pause menu content to screen.

        Uses class attributes, internal methods, and entered args to blit the
        pause menu background, each of the pause menu options (continue, sfx,
        music, and quit), and a highlighted version of whichever menu option
        is being hovered over.
        """
        self.window.blit(self.background, PAUSE_MENU_POS)
        for surface, rect in zip(self.text_surface_list, self.text_rect_list):
            if self.text_surface_list.index(surface) == self.current_index:
                white_surface = (self.text_font.render(self.text_list[self.current_index], True, GAME_TEXT_WHITE))
                white_rect = white_surface.get_rect(midleft=self.text_pos_list[self.current_index])
                self.window.blit(white_surface, white_rect)
            else:
                self.window.blit(surface, rect)
        pygame.display.update()

    def selected_option_update(self, direction: str) -> None:
        """Changes currently selected option depending on direction arg."""
        # Change current index.
        if direction == pygame.K_UP:
            if self.current_index == 0:
                self.current_index = 3
            else:
                self.current_index -= 1
        else:
            if self.current_index == 3:
                self.current_index = 0
            else:
                self.current_index += 1

        # Play hover sfx.
        if self.sfx_bool == 'True':
            self.button_hover_sfx.play()

    def sfx_music_update(self, selected_option: str) -> None:
        """Toggles selected option arg; that is, either music or sfx option."""
        self.button_click_sfx.play()

        if selected_option == 'SFX':
            if self.sfx_bool == 'True':
                self.sfx_bool = 'False'
            else:
                self.sfx_bool = 'True'
        elif selected_option == 'MUSIC':
            # Checks if music wasn't playing before game started in order to start music from beginning.
            if self.music_not_begun_yet and self.music_bool == 'False':
                pygame.time.delay(PAUSE_MENU_MUSIC_START_TIME_DELAY)
                pygame.mixer.music.play()
                self.music_not_begun_yet = False
                self.music_bool = 'True'
            elif self.music_bool == 'True':
                pygame.mixer.music.pause()
                self.music_bool = 'False'
            else:
                pygame.mixer.music.unpause()
                self.music_bool = 'True'
        else:
            print('selected option does not exist')

        # Remakes the surface and rect list comprehensions in order ro reflect sfx and music option toggle on screen.
        self.text_list[1] = f'SFX      {"ON" if self.sfx_bool == "True" else "OFF"}'
        self.text_list[2] = f'MUSIC    {"ON" if self.music_bool == "True" else "OFF"}'
        self.text_surface_list = [(self.text_font.render(self.text_list[index], True, GAME_TEXT_LIGHT_BLUE))
                                  for index in range(len(self.text_list))]
        self.text_rect_list = [surface.get_rect(midleft=pos)
                               for surface, pos in zip(self.text_surface_list, self.text_pos_list)]
