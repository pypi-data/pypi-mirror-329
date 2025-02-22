from typing import Tuple, List

import pygame

from taki_graphics.locations_config import LocationParams
from taki_graphics.render import BaseSprite


def position_cards(card_group: List[BaseSprite], locations: LocationParams) -> List[BaseSprite]:
    """
    Positions a group of cards based on the specified location parameters.

    :@param card_group: The list of cards to position.
    :@param locations: The location parameters that define the initial position,
    offset, and axis for positioning.

    @return: A list of positioned cards.
    """
    positioned_cards = []

    for i, card in enumerate(card_group):
        position = list(locations.position)
        position[locations.axis] += locations.offset * i

        card.update(tuple(position))
        positioned_cards.append(card)
    return positioned_cards


def is_positioned(group: pygame.sprite.RenderPlain, locations: LocationParams, count: int) -> bool:
    """
    Checks if the last card in a group is positioned correctly based on the given location parameters.

    :@param group: The group of sprite objects (cards).
    :@param locations: The location parameters containing the rules for positioning cards.
    :@param count: The number of cards that should have been positioned.

    :@return True if the last card is correctly positioned, False otherwise.
    """
    last_card = group.sprites()[-1].getposition()
    expected_position = list(locations.position)
    expected_position[locations.axis] += locations.offset * (count - 1)
    return last_card == tuple(expected_position)


def get_new_card_coordinates(last_card_pos: Tuple[int, int], player_location_params: LocationParams) -> \
        Tuple[int, int]:
    """
    Calculates the new coordinates for the next card based on the previous card's position and player configuration.

    :param last_card_pos: The position of the last card.
    :param player_location_params: The player's location configuration.
    :return: The new coordinates for the next card.
    """
    last_x, last_y = last_card_pos
    first_x, first_y = player_location_params.position
    if player_location_params.axis:
        if last_y >= player_location_params.max_position:
            return first_x + player_location_params.cards_gap, first_y
        else:
            return last_x, last_y + player_location_params.cards_gap
    else:
        if last_x >= player_location_params.max_position:
            return first_x, last_y + player_location_params.cards_gap
        else:
            return last_x + player_location_params.offset, last_y
