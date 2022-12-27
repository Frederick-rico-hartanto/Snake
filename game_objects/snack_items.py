"""Define game's snake player object.

This module holds a basic powerup apple snack as well as an abstract base
class to be used for future varieties of other game items/powerups.

Classes:
    Item: Abstract base class not meant to be instantiated!
    AppleSnack: Basic game powerup, simply giving 100 points.
"""

import os
import pygame
import random
from misc.constants import *


class Item(object):
    """Abstract base class not meant to be instantiated!

    This class contains all the basic information and content common of all
    game item objects. Only meant to be used as an (abstract) parent class for
    other more specific item classes. Common attributes of all game item
    objects: window to blit item, list of rect items already on screen (used
    to ensure new item isn't blit behind or on top of anything already on the
    screen), method to find a pos that isn't occupied, and a random position
    to blit item to.
    """

    def __init__(self, window: pygame.Surface, item_rect_list: list[pygame.Rect]) -> None:
        self.window = window
        self.item_rect_list = item_rect_list
        self.x = 0
        self.y = 0
        self.pos = self.random_pos()

    def random_pos(self) -> tuple[int, int]:
        """Return a random (x, y) coordinate tuple.

        Uses the item_rect_list attribute to find an (x, y) coordinate not
        currently occupied by any rect and returns it.

        Returns:
            self.x, self.y: A tuple representing a random x, y coordinate.
        """
        item_rect_x_list = [rect.centerx for rect in self.item_rect_list]
        item_rect_y_list = [rect.centery for rect in self.item_rect_list]

        while True:
            self.x = random.randrange(40, 761, SNAKE_CUBE_DISPLACEMENT)
            if self.x not in item_rect_x_list:
                break
        while True:
            self.y = random.randrange(70, 471, SNAKE_CUBE_DISPLACEMENT)
            if self.y not in item_rect_y_list:
                break
        return self.x, self.y


class AppleSnack(Item):
    """Apple snack version of Item class that gives 100 points for each eaten.

    This class creates an apple object with a random position and blits it to
    the screen when draw method is called. Apple snack represents the basic
    "powerup", simply giving 100 points and disappearing from the screen when
    eaten by snake.
    """

    def __init__(self, window: pygame.Surface, item_rect_list: list[pygame.Rect]) -> None:
        super().__init__(window, item_rect_list)
        self.width = ITEM_APPLE_SNACK_WIDTH
        self.height = ITEM_APPLE_SNACK_HEIGHT
        self.apple_image = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets', 'items', 'round_apple.png'))), (self.width, self.height))
        self.apple_rect = self.apple_image.get_rect(center=self.pos)

    def draw(self) -> None:
        """Blit apple snack item to screen."""
        self.window.blit(self.apple_image, self.apple_rect)
