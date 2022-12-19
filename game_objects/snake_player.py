"""Define game's snake player class.

This module holds a class responsible for blitting the program's snake player
object used in-game by user.

Classes:
    PlayerSnake: Snake object controlled by user in-game.
"""

import os
import pygame
from misc.constants import *
from misc.saved_data_io_functions import get_file_dict


class PlayerSnake(object):
    """Snake used by player eats snacks, grows, and dies among other things.

    This class holds all the code responsible for anything having to do with
    the snake: determining the dimensions and position of the snake head cube,
    what direction it is pointed at any given moment, what "skin" to use,
    increasing the length of the snake, determining where each snake head/body
    cube is at any given moment and moving them accordingly, blitting each
    snake head/body cube to the screen, changing the snake's direction,
    running a die method that stops the snake and has a death "animation",
    resetting the snake (so that the same object can be used again but from
    the start of the game), etc.
    """

    def __init__(self, window: pygame.Surface, head_pos: tuple[int, int], direction: str) -> None:
        self.window = window
        self.head_pos = head_pos
        self.direction = direction
        self.cube_width = SNAKE_CUBE_WIDTH
        self.cube_height = SNAKE_CUBE_HEIGHT
        self.user_preferences_dict = get_file_dict('user_preferences')
        self.snake_skin = self.user_preferences_dict.get('SNAKE SKIN').split('~')[1]
        self.head_cube = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets',
                         'snake_skins',
                         f'{self.snake_skin}head_{self.direction}.png',
                         ))), (self.cube_width, self.cube_height))
        self.body_cube = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets',
                         'snake_skins',
                         f'{self.snake_skin}body_cube.png',
                         ))), (self.cube_width-2, self.cube_height-2))
        self.head_cube_rect = self.head_cube.get_rect(center=self.head_pos)
        self.snake_cube_rect_list = [self.head_cube_rect,
                                     self.body_cube.get_rect(center=(self.head_pos[0],
                                                                     self.head_pos[1]+SNAKE_CUBE_DISPLACEMENT))]
        self.body_length = len(self.snake_cube_rect_list) - 1
        self.head_cube_displacement = (0, 0)
        self.displacement_dict = {'up': (0, -self.cube_height),
                                  'right': (self.cube_width, 0),
                                  'down': (0, self.cube_height),
                                  'left': (-self.cube_width, 0),
                                  }
        self.dead = False

    def draw(self) -> None:
        """Blit all MainMenu content to screen.

        Blit each body cube in snake cube rect list instance attribute then
        blit the head of the snake.
        """
        for body_cube in self.snake_cube_rect_list[1:]:
            self.window.blit(self.body_cube, body_cube)
        self.window.blit(self.head_cube, self.head_cube_rect)

    def move(self) -> None:
        """Update the position of each snake cube in snake_cube_list.

        A list of positions for all the snake cubes is created (from which a
        list of displacement tuples is created for each snake cube). The snake
        head cube is moved and every body cube takes the position of the body
        cube before it, resulting in the snake body cubes moving with the head.
        """
        snake_cube_pos_list = [cube.center for cube in self.snake_cube_rect_list]
        snake_cube_displace_list = [(pos_final[0]-pos_initial[0], pos_final[1]-pos_initial[1])
                                    for pos_final, pos_initial in zip(snake_cube_pos_list, snake_cube_pos_list[1:])]
        self.head_cube_displacement = self.displacement_dict[self.direction]
        self.head_cube_rect.move_ip(self.head_cube_displacement)
        for body_cube, displace in zip(self.snake_cube_rect_list[1:], snake_cube_displace_list):
            body_cube.move_ip(displace)

    def change_direction(self, direction_const: str, direction_dict: dict) -> None:
        """Check key input and change direction of snake accordingly.

        Takes in a key int that corresponds to a particular direction then
        determines the string version of that direction via the inputted dict.
        If the entered direction isn't in the opposite of the snake's current
        direction, then the direction is changed and the snake head image of
        the new direction is loaded.

        Args:
            direction_const: Used to determine what direction string is
                associated with direction_const value.
            direction_dict: Used to determine direction string associated with
                direction_const int and to check if new direction isn't in
                opposite direction of new one.
        """
        new_direction = direction_dict[direction_const]
        if {self.direction, new_direction} not in [{'left', 'right'}, {'up', 'down'}]:
            self.direction = new_direction
            self.head_cube = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
                os.path.join('project_assets',
                             'snake_skins',
                             f'{self.snake_skin}head_{self.direction}.png',
                             ))), (self.cube_width, self.cube_height))

    def increase_length(self) -> None:
        """Increase length of snake and append new body rect to cube list."""
        new_cube_pos = self.snake_cube_rect_list[-1].center
        new_cube = self.body_cube.get_rect(center=new_cube_pos)
        self.snake_cube_rect_list.append(new_cube)

    def die(self) -> None:
        """Kill snake player (end game stuff)."""
        head_cube_inflate_amount = tuple((abs(coord) for coord in reversed(self.displacement_dict[self.direction])))
        self.head_cube_displacement = tuple((-coord for coord in self.displacement_dict[self.direction]))
        self.head_cube_rect.move_ip(self.head_cube_displacement)
        self.head_cube = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets', 'snake_skins', f'{self.snake_skin}head_{self.direction}.png'))),
            (self.cube_width+head_cube_inflate_amount[0], self.cube_height+head_cube_inflate_amount[1]),
        )
        self.head_cube_rect.inflate_ip(head_cube_inflate_amount)
        self.dead = True

    def reset(self) -> None:
        """Reset snake instance to be used in next game.

        Snake player object is reset to all of its original states. Previous
        body cubes are no longer blit to screen, its head position is reset to
        its original starting place, the direction is set to 'up' again, the
        body length attribute is set back to 1, and the dead attribute boolean
        is set back to False.
        """
        self.head_pos = START_BUTTON_TEXT
        self.direction = SNAKE_PLAYER_START_DIRECTION
        self.head_cube = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets', 'snake_skins', f'{self.snake_skin}head_{self.direction}.png'))),
            (self.cube_width, self.cube_height),
        )
        self.body_cube = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets', 'snake_skins', f'{self.snake_skin}body_cube.png'))),
            (self.cube_width-2, self.cube_height-2),
        )
        self.head_cube_rect = self.head_cube.get_rect(center=self.head_pos)
        self.snake_cube_rect_list = [self.head_cube_rect,
                                     self.body_cube.get_rect(center=(self.head_pos[0],
                                                                     self.head_pos[1]+SNAKE_CUBE_DISPLACEMENT))]
        self.body_length = len(self.snake_cube_rect_list) - 1
        self.dead = False
