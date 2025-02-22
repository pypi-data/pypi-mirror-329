import os
from typing import Tuple

import pygame

module_path = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(module_path, 'assets')

class BaseSprite(pygame.sprite.Sprite):
    """
    A base class for common sprite functionalities.

    This class serves as a foundation for creating sprites, handling their
    image, position, and basic methods such as setting and getting positions
    and names. It also handles the basic functionality for rendering an image
    to a specific location.
    """

    def __init__(self, name: str, position: Tuple[int, int], image_scale: Tuple[int, int] = None):
        """
        Initializes the sprite with a given name, position, and optional image scaling.

        :@param name: The name of the sprite to load its image.
        :@param position: The (x, y) position of the sprite.
        :@param image_scale: The size to scale the sprite's image. Defaults to None.
        """
        super().__init__()
        self.name = name
        self.image = pygame.image.load(os.path.join(assets_dir, f'{name}.png'))
        if image_scale:
            self.image = pygame.transform.scale(self.image, image_scale)
        self.position = position
        self.rect = self.image.get_rect(center=position)

    def update_position(self, new_position):
        self.position = new_position
        self.rect.center = new_position

    def get_name(self) -> str:
        """
        :@return the name of the sprite.
        """
        return self.name

    def get_rect(self) -> pygame.Rect:
        """
        :@return the rectangle area of the sprite.
        """
        return self.rect

    def getposition(self) -> Tuple[int, int]:
        """
        :@return the current position of the sprite.
        """
        return self.position

    def setposition(self, x: int, y: int):
        """
        Sets the position of the sprite and updates its rectangle for rendering.

        :@param x: The new x-coordinate of the sprite.
        :@param y: The new y-coordinate of the sprite.
        """
        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


class Card(BaseSprite):
    """
    A class representing a card, derived from the BaseSprite class.

    This class adds functionality specific to a card, such as handling
    movement, rotation, and updating its position towards a destination.
    """

    def __init__(self, name: str, position: Tuple[int, int]):
        """
        Initializes the card with a name, position, and a default image scale.

        :@param name: The name of the card.
        :@param position: The initial (x, y) position of the card.
        """
        super().__init__(name, position, image_scale=(80, 100))
        self.orig_pos = position
        self.user_rotation = 30

    def update(self, dest_loc: Tuple[int, int]):
        """
        Moves the card towards a destination location.

        The card will gradually move to the destination by calculating the
        direction and updating its position incrementally.

        :@param dest_loc: The target (x, y) coordinates for the card to move towards.
        """
        x, y = self.position
        vx, vy = (dest_loc[0] - x, dest_loc[1] - y)
        vx, vy = (x / (x ** 2 + y ** 2) ** 0.5, y / (x ** 2 + y ** 2) ** 0.5)

        speed = 5

        x = x + speed * vx
        y = y + speed * vy

        if x >= dest_loc[0]:
            x = dest_loc[0]
        if y >= dest_loc[1]:
            y = dest_loc[1]

        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def rotation(self, rotate: int):
        """
        Rotates the card by a specified angle.

        The card's image is rotated by the given angle and its rectangle is
        updated accordingly.

        :@param rotate: The angle (in degrees) by which the card should be rotated.
        """
        self.image = pygame.transform.rotate(self.image, rotate)
        self.rect = self.image.get_rect(center=self.position)

    def move(self, compare_pos: Tuple[int, int], locations):
        """
        Moves the card relative to a given position, considering specific location rules.

        The card is moved based on the axis and position rules from the `locations` object.
        It can move either vertically or horizontally depending on the axis.

        :@param compare_pos: The (x, y) position to compare the current position with.
        :@param locations: The location parameters object containing rules for positioning.
        """
        x, y = self.position
        i_x, i_y = compare_pos

        if locations.axis:
            if x == i_x and y > i_y + locations.offset - 10:
                y -= locations.offset
            elif x > i_x:
                if y <= locations.position[1]:
                    y = locations.max_position
                    x = x - locations.cards_gap
                else:
                    y -= locations.offset
        else:
            if x > i_x + locations.offset - 10 and y == i_y:
                x -= locations.offset
            elif y > i_y:
                if x <= locations.position[0]:
                    x = locations.max_position
                    y -= locations.cards_gap
                else:
                    x -= locations.offset

        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


class Popup(BaseSprite):
    """
    A class representing a popup (for colors, options, etc.), derived from the BaseSprite class.

    Inherits from `BaseSprite` and allows displaying a popup with a specific name and position.
    """

    def __init__(self, name: str, position: Tuple[int, int]):
        """
        Initializes the popup with a name and position.

        :@param name: The name of the popup.
        :@param position: The (x, y) position of the popup.
        """
        super().__init__(name, position)
