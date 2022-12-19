"""Define ancillary button classes (due to absence of such objects in pygame).

This module holds multiple reusable button classes that serve multiple
generalized and specialized purposes. With the exception of the abstract
Button class, all other button classes are meant to be instantiated in any
pygame program.

Classes:
    Button: Abstract base class not meant to be instantiated!
    TextButton: Generalized text button.
    ApplyButton: Version of the TextButton w/ different button click sfx.
    ArrowButton: Generalized arrow button.
    CutoutArrowButton: Version of the ArrowButton w/ different arrow images.
"""

import os
import pygame
from misc.constants import *


class Button:
    """Abstract base class not meant to be instantiated!

    This class contains all the basic information and content common of all
    button objects. Only meant to be used as an (abstract) parent class for
    other more specific button classes. Common attributes of all button
    objects: window to blit button, position to blit button to, button
    dimensions, bool to keep track of whether a button is being hovered over,
    and a button hover sfx.
    """

    def __init__(self, window: pygame.Surface, pos: tuple[int, int], width: int, height: int) -> None:
        self.window = window
        self.pos = pos
        self.width = width
        self.height = height
        self.hovered = False
        self.button_hover_sfx = pygame.mixer.Sound(os.path.join('project_assets', 'sfx', 'button_hover.wav'))


class TextButton(Button):
    """Generalized text button object that allows some customizability.

    This class contains all the basic information and features present in the
    abstract "Button" class as well as some extra "text button" specific
    features such as: the ability to add text to button and choose whether the
    mouse click sfx is set to the normal version or a "start game sfx" version.
    Meant to be used as is and/or used as a base class for even more specified
    button classes.
    """

    def __init__(self, window: pygame.Surface, pos: tuple[int, int], width: int, height: int, text: str,
                 font_size: int, start_sfx: str = '') -> None:
        Button.__init__(self, window, pos, width, height)
        self.text = text
        self.font_size = font_size
        self.start_sfx = start_sfx
        self.button_click_sfx = pygame.mixer.Sound(os.path.join('project_assets',
                                                                'sfx',
                                                                f'button_click{self.start_sfx}.wav'))
        self.text_color = GAME_TEXT_BLUE
        self.text_font = pygame.font.Font(BUBBLE_FONT_FILE, self.font_size)
        self.text_surface = self.text_font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.pos)
        self.button_image = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets', 'buttons', 'stoneButtonReady.png'))), (self.width, self.height))
        self.button_image_hover = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets', 'buttons', 'stoneButtonHovered.png'))), (self.width, self.height))
        self.button_image_clicked = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets', 'buttons', 'stoneButtonPressed.png'))), (self.width, self.height))
        self.button_rect = self.button_image.get_rect(center=self.pos)

    def is_hovering(self, mouse_pos: tuple[int, int]) -> bool:
        """Return True if mouse is hovering over button."""
        if mouse_pos[0] in range(self.button_rect.left, self.button_rect.right) and \
                mouse_pos[1] in range(self.button_rect.top, self.button_rect.bottom):
            return True

    def draw_clicked(self, sfx_bool: str) -> None:
        """Blit clicked button image and user specified text to screen.

        Uses class attributes and entered args to blit the button with the
        user's specified text to the screen. Also makes a click sfx if game
        sound is turned on.

        Args:
            sfx_bool: Used to determine if button should make a click sfx when
                selected.
        """
        self.window.blit(self.button_image_clicked, self.button_rect)
        self.window.blit(self.text_surface, self.text_rect)
        pygame.display.update()
        if sfx_bool == 'True':
            self.button_click_sfx.play()

    def draw(self, mouse_pos: tuple[int, int], sfx_bool: str) -> None:
        """Blit normal or hovered button image to screen accordingly.

        This method checks if the mouse is hovering over the button or not and
        blits the normal or hovered version of the button, accordingly. Also
        makes hover sfx if game sound is turned on.

        Args:
            mouse_pos: Used to determine if mouse is hovering over button.
            sfx_bool: Used to determine if button should make a hover sfx when
                mouse is hovering over it.
        """
        if self.is_hovering(mouse_pos):
            self.window.blit(self.button_image_hover, self.button_rect)
            self.window.blit(self.text_surface, self.text_rect)
            if self.hovered is False:
                if sfx_bool == 'True':
                    self.button_hover_sfx.play()
                self.hovered = True
        else:
            self.window.blit(self.button_image, self.button_rect)
            self.window.blit(self.text_surface, self.text_rect)
            if self.hovered is True:
                self.hovered = False


class ApplyButton(TextButton):
    """Version of the TextButton class but w/ different button click sfx.

    This class contains all the same information and features present in its
    base class, "TextButton". Meant to be a more specialized version with the
    following differences (for now): different sfx for mouse button click,
    draw_clicked() method is redefined to ignore the click sfx conditional
    (only activated if sfx_bool is true), ...
    """

    def __init__(self, window: pygame.Surface, pos: tuple[int, int], width: int, height: int, text: str, font_size: int,
                 ) -> None:
        super().__init__(window, pos, width, height, text, font_size)
        self.button_click_sfx = pygame.mixer.Sound(os.path.join('project_assets', 'sfx', 'button_apply_changes.wav'))

    def draw_clicked(self) -> None:
        """Blit clicked button instance to screen and make apply changes sfx."""
        self.window.blit(self.button_image_clicked, self.button_rect)
        self.window.blit(self.text_surface, self.text_rect)
        pygame.display.update()
        self.button_click_sfx.play()


class ArrowButton(Button):
    """Generalized arrow button object that allows some customizability.

    This class contains all the basic information and features present in the
    abstract "Button" class as well as some extra "arrow button" specific
    features such as: different button images of a dark arrow in a stone
    textured square, the ability to choose the direction that the arrow is
    pointing, and methods responsible for drawing the different versions of
    the arrow button (normal, hover, and clicked)
    """

    def __init__(self, window: pygame.Surface, pos: tuple[int, int], width: int, height: int, direction: str) -> None:
        Button.__init__(self, window, pos, width, height)
        self.direction = direction
        self.button_click_direction_sfx = pygame.mixer.Sound(
            os.path.join('project_assets', 'sfx', f'button_click_{self.direction}.wav'))
        self.arrow_image = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets',
                         'buttons',
                         f'ArrowButtonReady{self.direction.capitalize()}.png',
                         ))), (self.width, self.height))
        self.arrow_image_hover = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets',
                         'buttons',
                         f'ArrowButtonHovered{self.direction.capitalize()}.png',
                         ))), (self.width, self.height))
        self.arrow_image_clicked = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets',
                         'buttons',
                         f'ArrowButtonPressed{self.direction.capitalize()}.png',
                         ))), (self.width, self.height))
        self.arrow_rect = self.arrow_image.get_rect(center=self.pos)

    def is_hovering(self, mouse_pos: tuple[int, int]) -> bool:
        """Return True if mouse is hovering over button."""
        if mouse_pos[0] in range(self.arrow_rect.left, self.arrow_rect.right) and \
                mouse_pos[1] in range(self.arrow_rect.top, self.arrow_rect.bottom):
            return True

    def draw_clicked(self, sfx_bool: str) -> None:
        """Blit clicked button image to screen and play click sfx."""
        self.window.blit(self.arrow_image_clicked, self.arrow_rect)
        pygame.display.update()
        if sfx_bool == 'True':
            self.button_click_direction_sfx.play()

    def draw(self, mouse_pos: tuple[int, int], sfx_bool: str) -> None:
        """Blit normal or hovered button image to screen accordingly.

        This method checks if the mouse is hovering over the button or not and
        blits the normal or hovered version of the button, accordingly. Also
        makes hover sfx if game sound is turned on.

        Args:
            mouse_pos: Used to determine if mouse is hovering over button.
            sfx_bool: Used to determine if button should make a hover sfx when
                mouse is hovering over it.
        """
        if self.is_hovering(mouse_pos):
            self.window.blit(self.arrow_image_hover, self.arrow_rect)
            if self.hovered is False:
                if sfx_bool == 'True':
                    self.button_hover_sfx.play()
                self.hovered = True
        else:
            self.window.blit(self.arrow_image, self.arrow_rect)
            if self.hovered is True:
                self.hovered = False


class CutoutArrowButton(ArrowButton):
    """Version of the ArrowButton class but w/ different arrow images.

    This class contains all the same information and features present in its
    base class, "ArrowButton". Meant to be a more specialized version with 
    different arrow button images being used (they are arrow buttons instead 
    of arrows in a stone square like before). "Cutout arrow button" also has 
    method for updating pos of button on screen if so desired.
    """

    def __init__(self, window: pygame.Surface, pos: tuple[int, int], width: int, height: int, direction: str) -> None:
        super().__init__(window, pos, width, height, direction)
        self.arrow_image = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets',
                         'buttons',
                         f'ArrowButtonCutoutReady{self.direction.capitalize()}.png',
                         ))), (self.width, self.height))
        self.arrow_image_hover = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets',
                         'buttons',
                         f'ArrowButtonCutoutHovered{self.direction.capitalize()}.png',
                         ))), (self.width, self.height))
        self.arrow_image_clicked = pygame.transform.scale(pygame.Surface.convert_alpha(pygame.image.load(
            os.path.join('project_assets',
                         'buttons',
                         f'ArrowButtonCutoutPressed{self.direction.capitalize()}.png',
                         ))), (self.width, self.height))

    def update_button_pos(self, pos: tuple[int, int]) -> None:
        """Update position of button."""
        self.pos = pos
        self.arrow_rect = self.arrow_image.get_rect(midleft=self.pos)
