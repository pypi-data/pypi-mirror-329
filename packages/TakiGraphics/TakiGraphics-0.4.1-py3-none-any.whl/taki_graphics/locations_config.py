import dataclasses
from typing import Tuple

@dataclasses.dataclass
class LocationParams:
    """
    Data class to store parameters related to a player's location and card display settings.
    """
    rotation: int  # The rotation angle for the cards placed at this location.
    position: Tuple[int, int]  # The (x, y) coordinates for placing the first card.
    offset: int  # The offset to be used when positioning the cards.
    axis: int  # The axis on which the cards are positioned. 0 means the x-axis, 1 means the y-axis.
    text_position: Tuple[int, int]  # The (x, y) coordinates for displaying text, such as player name.
    max_position: int  # The maximum coordinate value for card placement, ensuring cards stay within the screen bounds.
    cards_gap: int  # The gap between consecutive cards when they are displayed.


# Dictionary mapping each Location enum value to its corresponding LocationParams
PLAYER_LOCATION_PARAMS = {
    'DOWN':
        LocationParams(
            rotation=0,
            position=(180, 500),
            offset=70,
            axis=0,
            text_position=(165, 420),
            max_position=660,
            cards_gap=80
        ),
    'UP':
        LocationParams(
            rotation=180,
            position=(250, 100),
            offset=40,
            axis=0,
            text_position=(235, 18),
            max_position=550,
            cards_gap=40
        ),
    'LEFT':
        LocationParams(
            rotation=270,
            position=(55, 160),
            offset=40,
            axis=1,
            text_position=(45, 30),
            max_position=450,
            cards_gap=40
        )
}
