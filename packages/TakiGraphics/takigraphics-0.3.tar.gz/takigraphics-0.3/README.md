# TakiGraphics - Graphical Interface for Taki Game

`TakiGraphics` is a Python class designed to provide a graphical user interface (GUI) for the Taki card game using the Pygame library. It handles the rendering of cards, player locations, and other game elements, allowing the game to be visually played on a screen.

## Features

- **Card Display**: Displays cards for each player and for the ground (center of the screen).
- **Card Interaction**: Allows players to select cards by clicking on them with the mouse.
- **Player Locations**: Cards are displayed according to different player locations such as UP, DOWN, LEFT.
- **Color Selection Popup**: Allows players to select colors (RED, YELLOW, GREEN, BLUE) during gameplay.
- **Automatic Positioning**: Cards are positioned automatically depending on the player's location and previous card positions.

## Requirements

- Python 3.6 or higher
- Pygame library

You can install Pygame using pip:
```bash
pip install pygame