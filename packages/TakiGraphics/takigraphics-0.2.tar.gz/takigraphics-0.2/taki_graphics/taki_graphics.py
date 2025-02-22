import sys
from typing import List, Optional

import pygame
from pygame import QUIT, MOUSEBUTTONDOWN, K_0, KEYDOWN, K_SPACE

from taki_graphics import render
from taki_graphics.config import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_NAME, HIDDEN_CARD_NAME
from taki_graphics.utils import position_cards, is_positioned, get_new_card_coordinates
from taki_graphics.locations_config import PLAYER_LOCATION_PARAMS, LocationParams


class TakiGraphics:
    """
    The graphical interface for the Taki game, responsible for rendering the game
    to the screen using Pygame. This includes displaying cards, players, and other
    graphical elements.
    """

    ground_position = (430, 300)
    deck_position = (350, 300)
    card_size = (400, 300)

    def __init__(self):
        """
        Initializes the TakiGraphics class, setting up the screen, graphical elements,
        player locations, and other necessary game assets.
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ground_graphic = pygame.sprite.RenderPlain()
        self.deck_graphic = self._create_deck()
        self.popup_colors_group = self._create_colors_popup()

        self.players_to_sprites = {}
        self.players_to_locations = {}

        pygame.init()
        self._setup_window()
        pygame.display.update()

    def print_cards(self, cards: List[str], location: str, name: str,
                    is_hidden: bool = False) -> None:
        """
        Displays a player's cards on the screen.

        :param cards: List of card names to display.
        :param location: The player's location on the screen [UP, DOWN, LEFT].
        :param name: The player's name.
        :param is_hidden: If True, the cards will be hidden.
        """
        player_location_params = PLAYER_LOCATION_PARAMS.get(location)
        if not location:
            raise ValueError(f"The location {location} is invalid. Accepted values are: UP, DOWN, LEFT.")
        graphic_cards = self._create_cards(cards, is_hidden, player_location_params)
        sprites_group = self._get_sprites_group(graphic_cards, player_location_params)
        sprites_group.draw(self.screen)

        self.players_to_sprites[name] = sprites_group
        self.players_to_locations[name] = player_location_params

        if name:
            self._display_text(player_location_params, name)

        self._print_window()

    def print_ground_card(self, card: str) -> None:
        """
        Displays a card on the ground (center of the screen).

        :param card: The name of the card to display.
        """
        graphic_card = render.Card(card, self.ground_position)
        self.ground_graphic.add(graphic_card)
        self.ground_graphic.draw(self.screen)
        pygame.display.update()


    def select_card(self, name: str) -> Optional[str]:
        """
        Allows a player to select a card using the mouse.

        :param name: The player's name.
        :return: The name of the selected card, or None if no card was selected.
        """
        while True:
            for event in pygame.event.get():  # Event listener loop is O(1), but the whole thing here is O(n^2)
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for sprite in self.players_to_sprites[name]:
                        if sprite.get_rect().collidepoint(mouse_pos):
                            return sprite.name
                    for sprite in self.deck_graphic:
                        if sprite.get_rect().collidepoint(mouse_pos):
                            return


    def remove_card_for_player(self, card: str, name: str) -> None:
        """
        Removes a card from the player's field.

        :param card: The name of the card to remove.
        :param name: The player's name.
        """
        sprites_group = self.players_to_sprites[name]
        locations = self.players_to_locations[name]

        sprite_to_remove = [sprite for sprite in sprites_group if sprite.name in (card, HIDDEN_CARD_NAME)][0]
        if sprite_to_remove.name == HIDDEN_CARD_NAME:
            pygame.time.wait(700)

        sprites_group.remove(sprite_to_remove)
        for temp in sprites_group:
            temp.move(sprite_to_remove.getposition(), locations)

        sprites_group.draw(self.screen)
        self._print_window()

    def add_card_for_user(self, card: str, name: str, is_hidden: bool = False) -> None:
        """
        Adds a card to the player's field.

        :param card: The name of the card to add.
        :param name: The player's name.
        :param is_hidden: If True, the card will be hidden.
        """
        sprites_group = self.players_to_sprites[name]
        player_location_params = self.players_to_locations[name]

        if is_hidden:
            pygame.time.wait(700)
            graphic_card = render.Card(HIDDEN_CARD_NAME, self.card_size)
            graphic_card.rotation(player_location_params.rotation)
        else:
            if not isinstance(card, str):
                raise TypeError(f"Expected Type str, recieve: {type(card)}")
            graphic_card = render.Card(card, self.card_size)

        last_card_pos = sprites_group.sprites()[-1].getposition()
        x, y = get_new_card_coordinates(last_card_pos, player_location_params)

        graphic_card.setposition(x, y)
        sprites_group.add(graphic_card)
        self._print_window()

    def print_winner(self, name: str):
        pygame.draw.rect(self.screen, (173, 216, 230), pygame.Rect(200, 200, 400, 200))
        pygame.draw.rect(self.screen, (191, 239, 255), pygame.Rect(210, 210, 380, 180))

        message_color = (0, 0, 139)
        font = pygame.font.SysFont(FONT_NAME, 50)

        text_position = (230, 220)
        result_message = font.render(f"{name}  Win!", K_0, message_color)
        self.screen.blit(result_message, text_position)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    return True

    def select_color_popup(self) -> str:
        """
        Displays a color selection popup and allows the player to select a color.

        :return: The selected color.
        """
        self.popup_colors_group.draw(self.screen)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for sprite in self.popup_colors_group.sprites()[::-1]:
                        if sprite.get_rect().collidepoint(mouse_pos):
                            chosen_color = sprite.get_name()
                            self.print_ground_card(chosen_color)
                            self._print_window()
                            return chosen_color

    def _setup_window(self) -> None:
        """
        Sets up the window background
        """
        background = pygame.image.load(f'{render.assets_dir}/background.png')  # Draw background
        self.screen.blit(background, (-100, -70))
        self.deck_graphic.draw(self.screen)

    def _print_window(self) -> None:
        """
        Renders the main game window, displaying the deck, ground, and all player cards,
        along with any relevant text.
        """
        self._setup_window()
        self.ground_graphic.draw(self.screen)

        for name, sprites in self.players_to_sprites.items():
            sprites.draw(self.screen)
            players_to_locations = self.players_to_locations[name]
            self._display_text(players_to_locations, name)

        pygame.display.update()

    @staticmethod
    def _create_colors_popup() -> pygame.sprite.RenderPlain:
        """
        Creates the popup for selecting colors.

        :return: A pygame sprite group containing the color selection popups.
        """
        red = render.Popup('RED', (306, 320))
        yellow = render.Popup('YELLOW', (368, 320))
        green = render.Popup('GREEN', (432, 320))
        blue = render.Popup('BLUE', (494, 320))
        colors = [red, yellow, green, blue]
        return pygame.sprite.RenderPlain(*colors)

    def _create_cards(self, cards: List[str], is_hidden: bool, sprite_config: LocationParams) -> List[render.Card]:
        """
        Creates graphical card objects and applies rotation to them based on the sprite configuration.

        :param cards: List of card names.
        :param is_hidden: If True, the cards will be hidden.
        :param sprite_config: The player's sprite configuration, including rotation.
        :return: A list of graphical card objects.
         """
        graphic_cards = list()
        for card_name in cards:
            if is_hidden:
                graphic_card = render.Card(HIDDEN_CARD_NAME, self.card_size)
            else:
                graphic_card = render.Card(card_name, self.card_size)
            graphic_card.rotation(sprite_config.rotation)
            graphic_cards.append(graphic_card)
        return graphic_cards

    def _get_sprites_group(self, graphic_cards: List[render.Card], locations: LocationParams) -> \
            pygame.sprite.RenderPlain:
        """
        Creates a sprite group for the cards and positions them according to the player's location.

        :param graphic_cards: List of graphical card objects.
        :param locations: The player's location configuration.
        :return: A pygame sprite group containing the positioned cards.
        """
        booting = True
        sprites_group = None
        while booting:
            sprites = position_cards(graphic_cards, locations)
            sprites_group = pygame.sprite.RenderPlain(*sprites)
            booting = not is_positioned(sprites_group, locations, len(sprites_group))
            pygame.display.update()

        last_card_pos = locations.position
        for sprite in sprites_group.sprites()[1:]:
            x, y = get_new_card_coordinates(last_card_pos, locations)
            sprite.setposition(x, y)
            last_card_pos = (x, y)

        return sprites_group

    def _display_text(self, sprite_config: LocationParams, text: str) -> None:
        """
        Displays text on the screen at a specific location.

        :param sprite_config: The location configuration of the player.
        :param text: The text to display.
        """
        font = pygame.font.SysFont(FONT_NAME, 30)
        text = font.render(text, K_0, (0,0,0))
        self.screen.blit(text, sprite_config.text_position)

    def _create_deck(self) -> pygame.sprite.RenderPlain:
        """
        Creates the deck with a hidden card at the specified deck position.
        :return: A pygame sprite group containing the deck.
        """
        deck = render.Card(HIDDEN_CARD_NAME, self.deck_position)
        return pygame.sprite.RenderPlain(deck)
