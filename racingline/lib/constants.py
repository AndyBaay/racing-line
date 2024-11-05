from enum import Enum

# Settings
FPS = 60
GRID_SQUARE_SIZE = 16
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 300


class Color(Enum):
    RED = (200, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_GREEN = (0, 204, 0)
    DARK_GREEN = (0, 153, 0)
    LIGHT_BLUE = (102, 178, 255)
    LIGHT_GRAY = (224, 224, 224)
    DARK_GRAY = (64, 64, 64)
    GRAY = (192, 192, 192)
    BLACK = (0, 0, 0)
