# settings.py

TILE_SIZE = 40
GRID_WIDTH = 20
GRID_HEIGHT = 15

WIDTH = GRID_WIDTH * TILE_SIZE   # 800 px
HEIGHT = GRID_HEIGHT * TILE_SIZE # 600 px
FPS = 60

PLAYER_SPEED = 240  # piksela u sekundi
SHIFT_COOLDOWN = 0.35  # sekundi između dve promene dimenzije

# Palete boja za obe dimenzije
PALETTES = {
    "LIGHT": {
        "bg": (238, 240, 245),
        "universal_wall": (35, 38, 46),
        "active_wall": (65, 105, 225),     # Kraljevsko plava
        "ghost_wall": (210, 215, 225),      # Jedva vidljiva silueta Dark zidova
        "player": (220, 45, 65),
        "key": (245, 165, 0),
        "exit_locked": (170, 175, 185),
        "exit_open": (30, 190, 95),
        "flash": (255, 255, 255),
    },
    "DARK": {
        "bg": (16, 19, 28),
        "universal_wall": (45, 50, 68),
        "active_wall": (0, 230, 180),       # Neonska tirkizna
        "ghost_wall": (28, 33, 48),         # Jedva vidljiva silueta Light zidova
        "player": (255, 70, 110),
        "key": (255, 215, 0),
        "exit_locked": (60, 65, 80),
        "exit_open": (0, 255, 135),
        "flash": (0, 230, 180),
    },
}