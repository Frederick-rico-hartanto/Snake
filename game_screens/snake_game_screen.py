"""Define snake game and snake game screen classes of program.

This module holds two classes used for the actual snake game itself - the
program's "main course", if you will. One class is used for organizing all of
the "game screens" in the game_screens package, while the other contains the
game itself.

Classes:
    SnakeGameScreen: Contains snake game screen of program.
    SnakeGame: Contains actual snake game code.
"""

import os
import sys
import pygame
from misc.constants import *
from misc.saved_data_io_functions import get_file_dict
from game_objects.game_border_ui import GameBorderUI
from game_objects.game_grid import GameGrid
from game_objects.pregame_rules_board import GameRulesBoard
from game_objects.snack_items import AppleSnack
from game_objects.snake_player import PlayerSnake
from game_screens.game_over_screen import GameOverScreen
from game_screens.pause_menu import PauseMenu
from game_screens.post_game_screen import PostGameScreen


class SnakeGameScreen(object):
    """Manages all screens/content in game_screens package.

    This class acts like a container for managing all screens used after
    pressing the "start game" button in the main menu. It sets up/loads all
    objects to be used in the snake game itself like: the game clock, the
    background, the game grid, the border ui and all of its data, the snake
    object itself as well as 3 snacks to the screen, and the game rules board
    if this is the user's first game. Also includes an event loop that starts
    the game as soon as any key is pressed, setups up and creates all other
    game screens used after game ends, including the game over screen and the
    post game screen.
    """

    def __init__(self, window: pygame.Surface, width: int, height: int, sfx_bool: str, music_bool: str,
                 background: pygame.Surface) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.sfx_bool = sfx_bool
        self.music_bool = music_bool
        self.grid_bool = get_file_dict('user_preferences').get('GRID').split('~')[1]
        self.first_game = True
        self.play_again = False
        self.score_saved_bool = False
        self.caption = 'Snake'
        self.clock = pygame.time.Clock()
        self.border_ui = GameBorderUI(self.window, self.width, self.height, game_ready_ui=True)
        self.bg_width = (self.width - (self.border_ui.border_left.get_width() * 2))
        self.bg_height = (self.height
                          - (self.border_ui.border_upper.get_height()
                             + self.border_ui.border_lower.get_height()))
        self.bg_dimensions = (self.bg_width, self.bg_height)
        self.background = pygame.transform.scale(background, self.bg_dimensions)
        self.bg_x = self.border_ui.border_left.get_width()
        self.bg_y = self.border_ui.border_upper.get_height()
        self.bg_pos = (self.bg_x, self.bg_y)
        self.grid = GameGrid(self.window, self.border_ui) if self.grid_bool == 'True' else None
        self.instructions_board = GameRulesBoard(self.window, self.width, self.height)
        self.snake_player = PlayerSnake(self.window, SNAKE_PLAYER_START_POS, SNAKE_PLAYER_START_DIRECTION)
        self.apple_list = [AppleSnack(self.window, self.snake_player.snake_cube_rect_list)
                           for _ in range(NUMBER_OF_APPLE_SNACKS)]
        self.running = 1

    def run(self) -> None:
        """Run snake game screen event loop.

        This method contains an event loop that manages all of the screens in
        the game_screens package. It checks if the user wants to start a new
        game or quit and uses information from choices made in previous
        screens to determine what shows up on the subsequent screens.
        """
        pygame.display.set_caption(self.caption)

        while self.running:
            event_list = pygame.event.get()

            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Checks if first game and a key was pressed or if subsequent game and play again button was pressed.
                elif (event.type == pygame.KEYUP and self.first_game) or self.play_again:
                    self.first_game = False
                    # Creates snake game itself and runs.
                    snake = SnakeGame(self.window, self.width, self.height, self.sfx_bool, self.music_bool,
                                      self.grid_bool, self.clock, self.border_ui, self.background, self.bg_pos,
                                      self.grid, self.snake_player, self.apple_list)
                    snake.run()
                    if snake.quit_to_main:  # Used if player quit game from pause menu in SnakeGame class.
                        self.running = 0
                        break
                    self.sfx_bool, self.music_bool = snake.sfx_bool, snake.music_bool
                    # Creates game over screen and runs.
                    game_over = GameOverScreen(self.window, self.width, self.height, self.sfx_bool, self.music_bool,
                                               self.bg_dimensions, self.bg_pos, self.border_ui.user_score)
                    game_over.run()
                    self.score_saved_bool = game_over.score_saved_bool  # If true, post game screen shows scoreboard.
                    # Creates post/pre game screen and runs.
                    self.border_ui.game_ready_ui = False
                    post_game_screen = PostGameScreen(self.window, self.border_ui, self.bg_dimensions, self.bg_pos,
                                                      self.sfx_bool, self.score_saved_bool, game_over.user_score,
                                                      game_over.name_input.lower())
                    post_game_screen.run()
                    self.play_again = post_game_screen.play_again
                    # Returns to main menu if user didn't want to play again, otherwise, resets all game objects.
                    if self.play_again is False:
                        self.running = 0
                        break
                    else:
                        pygame.display.set_caption(self.caption)
                        self.border_ui.reset()
                        self.snake_player.reset()
                        self.apple_list = [AppleSnack(self.window, self.snake_player.snake_cube_rect_list)
                                           for _ in range(NUMBER_OF_APPLE_SNACKS)]
                else:
                    pass

            self.draw()

    def draw(self) -> None:
        """Blit all setup snake game content before game starts.

        This method blits content to be used in-game, before the game starts,
        including: the background, the game grid, the snake player, all
        randomly positioned snack items, the border ui, and an instructions
        board if it is the user's first game.
        """
        self.window.blit(self.background, self.bg_pos)
        if self.grid_bool == 'True':
            self.grid.draw()
        self.snake_player.draw()
        for apple in self.apple_list:
            apple.draw()
        self.border_ui.draw()
        if self.first_game:
            self.instructions_board.draw()
        pygame.display.update()


class SnakeGame(object):
    """Contains content used in the actual snake game itself.

    This class represents the game itself, with its main feature being an
    event loop that checks for user input and changes the screen accordingly.
    """

    def __init__(self, window: pygame.Surface, width: int, height: int, sfx_bool: str, music_bool: str, grid_bool: str,
                 clock: pygame.time.Clock, border_ui: GameBorderUI, background: pygame.Surface,
                 bg_pos: tuple[int, int], grid: GameGrid, snake_player: PlayerSnake, apple_list: list[AppleSnack],
                 ) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.sfx_bool = sfx_bool
        self.music_bool = music_bool
        self.grid_bool = grid_bool
        self.music_not_begun_yet = True
        self.clock = clock
        self.border_ui = border_ui
        self.background = background
        self.bg_pos = bg_pos
        self.grid = grid
        self.snake_player = snake_player
        self.apple_list = apple_list
        self.caption = 'Snake - In Game'
        self.game_music_intro = self.menu_music = os.path.join('project_assets', 'music', 'game_music_intro.ogg')
        self.game_music = self.menu_music = os.path.join('project_assets', 'music', 'game_music.ogg')
        self.snack_points_up_sfx = pygame.mixer.Sound(os.path.join('project_assets', 'sfx', 'snack_points_up.wav'))
        self.snake_crashes_sfx = pygame.mixer.Sound(os.path.join('project_assets', 'sfx', 'snake_crashes.wav'))
        self.start_time = pygame.time.get_ticks()
        self.total_pause_time = 0
        self.quit_to_main = False
        self.running = 1

    def run(self) -> None:
        """Run snake game event loop.

        This method starts the game's music and a timer on the top right of
        the screen, before starting the main game while loop. The game loop
        first checks if any key events have occurred (pause or change snake's
        direction), then calls a move method from snake player instance that
        moves snake for current frame, then checks for collisions between the
        snake player and any borders or snack items (and executes relevant
        code), and then finally draws all current game information to screen.
        """
        pygame.display.set_caption(self.caption)
        pygame.mixer.music.load(self.game_music_intro)
        pygame.mixer.music.queue(self.game_music, loops=-1)
        if self.music_bool == 'True':
            pygame.mixer.music.play()
        arrow_keys_dict = {pygame.K_UP: 'up', pygame.K_RIGHT: 'right', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left'}

        while self.running:
            pygame.time.delay(GAME_LOOP_DELAY)
            self.clock.tick(GAME_LOOP_TICK)
            event_list = pygame.event.get()

            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Checks if game was paused.
                    if event.key == pygame.K_ESCAPE:
                        # Creates pause menu and runs.
                        pause_menu = PauseMenu(self.window, self.width, self.height, self.sfx_bool, self.music_bool,
                                               self.music_not_begun_yet)
                        pause_menu.run()
                        pygame.mixer.music.set_volume(GAME_VOLUME)  # Increase volume of music back to normal.
                        self.total_pause_time += pause_menu.total_time_paused
                        self.sfx_bool, self.music_bool = pause_menu.sfx_bool, pause_menu.music_bool
                        self.music_not_begun_yet = pause_menu.music_not_begun_yet
                        self.quit_to_main = pause_menu.quit_to_main
                        # Returns to main menu immediately if player pressed quit in pause menu.
                        if pause_menu.quit_to_main:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.unload()
                            self.running = 0
                            break
                        pygame.display.set_caption(self.caption)
                    # Checks if any of the arrow keys were pressed.
                    elif event.key in arrow_keys_dict.keys():
                        self.snake_player.change_direction(event.key, arrow_keys_dict)
                    else:
                        print('key pressed does nothing')
                else:
                    pass

            # Move snake for this particular "frame".
            self.snake_player.move()

            # Collision event handling.
            self.end_game_event_handling()
            self.snack_collision_handling()

            self.draw()

    def draw(self) -> None:
        """Blit current frame of snake game content.

        This method blits all content in the game's current frame, to the
        screen. Content includes: the background, a grid (if turned on), the
        current position of the snake, all apple objects in apple_list, and
        the game border ui (border ui timer information is updated before
        doing so).
        """
        self.window.blit(self.background, self.bg_pos)
        if self.grid_bool == 'True':
            self.grid.draw()
        self.snake_player.draw()
        for apple in self.apple_list:
            apple.draw()
        self.border_ui.update_timer(pygame.time.get_ticks(), self.start_time, self.total_pause_time)
        self.border_ui.draw()
        pygame.display.update()

    def end_game_event_handling(self) -> None:
        """Event handling for end game conditions.

        This method checks if the snake object's head rect has collided with
        any of the game border rects or any of the snake object's body cube
        rects. If it has, game end code is executed.
        """
        if list(filter(self.snake_player.head_cube_rect.colliderect,
                       (self.snake_player.snake_cube_rect_list[1:] + self.border_ui.border_image_rect_list))):
            self.snake_player.die()
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            if self.sfx_bool == 'True':
                self.snake_crashes_sfx.play()
            self.running = 0

    def snack_collision_handling(self) -> None:
        """Event handling for snack item collisions.

        This method checks if the snake object's head rect has collided with
        any of the snack items' rects currently blitted to the screen. If it
        has, "snack eaten" code is executed (eaten apple object is removed
        from apple list, a sfx is played, snake increases in length, snacks
        eaten attribute in border ui goes up, and a new apple object is
        created and added to apple list).
        """
        if list(filter((lambda apple_ob: self.snake_player.head_cube_rect.colliderect(apple_ob.apple_rect)),
                       self.apple_list)):

            for apple in self.apple_list:
                if self.snake_player.head_cube_rect.colliderect(apple.apple_rect):
                    self.apple_list.remove(apple)
                    break
            if self.sfx_bool == 'True':
                self.snack_points_up_sfx.play()
            self.snake_player.increase_length()
            self.border_ui.snacks_eaten += 1
            current_item_rect_list = self.snake_player.snake_cube_rect_list + [apple.apple_rect
                                                                               for apple in self.apple_list]
            self.apple_list.append(AppleSnack(self.window, current_item_rect_list))
