# levels.py
import pygame
from settings import TILE_SIZE, PALETTES

# Legenda:
# '#' - Zid u obe dimenzije
# 'L' - Zid samo u LIGHT dimenziji
# 'D' - Zid samo u DARK dimenziji
# 'P' - Početna pozicija igrača
# '1' - Ključ (Data Core) u LIGHT dimenziji
# '2' - Ključ (Data Core) u DARK dimenziji
# 'E' - Izlaz (Exit)

LEVELS = [
    [
        "####################",
        "#P   L        D   2#",
        "#    L   ##   D    #",
        "#    L   ##   D    #",
        "#        ##        #",
        "#   DDDDDDDDDDDD   #",
        "#        ##        #",
        "#   LLLLLLLLLLLL   #",
        "#        ##        #",
        "#    D   ##   L    #",
        "#    D   ##   L    #",
        "#    D        L   E#",
        "#    D   ##   L    #",
        "#        ##        #",
        "####################",
    ],
    [
        "####################",
        "#P #   L   D   #  E#",
        "#  #   L   D   #   #",
        "#  #   L   D   #   #",
        "#  #####   #####   #",
        "#      D   L       #",
        "#  LLLLL   DDDDD   #",
        "#                  #",
        "#  DDDDD   LLLLL   #",
        "#      L   D       #",
        "#  #####   #####   #",
        "#  #   D   L   #   #",
        "#  #   D   L   #   #",
        "# 1#   D   L   #   #",
        "####################",
    ],
]


class Level:
    def __init__(self, level_data):
        self.universal_walls = []
        self.light_walls = []
        self.dark_walls = []
        self.player_start = (TILE_SIZE, TILE_SIZE)
        self.key_rect = None
        self.key_dimension = None
        self.key_collected = False
        self.exit_rect = None

        self._parse_level(level_data)

    def _parse_level(self, level_data):
        for row_idx, row in enumerate(level_data):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

                if cell == "#":
                    self.universal_walls.append(rect)
                elif cell == "L":
                    self.light_walls.append(rect)
                elif cell == "D":
                    self.dark_walls.append(rect)
                elif cell == "P":
                    self.player_start = (x + 6, y + 6)
                elif cell == "1":
                    self.key_rect = pygame.Rect(x + 10, y + 10, TILE_SIZE - 20, TILE_SIZE - 20)
                    self.key_dimension = "LIGHT"
                elif cell == "2":
                    self.key_rect = pygame.Rect(x + 10, y + 10, TILE_SIZE - 20, TILE_SIZE - 20)
                    self.key_dimension = "DARK"
                elif cell == "E":
                    self.exit_rect = rect

    def get_active_walls(self, dimension):
        if dimension == "LIGHT":
            return self.universal_walls + self.light_walls
        return self.universal_walls + self.dark_walls

    def draw(self, surface, dimension):
        palette = PALETTES[dimension]
        surface.fill(palette["bg"])

        # 1. Crtanje silueta (ghost zidova) iz suprotne dimenzije
        ghost_walls = self.dark_walls if dimension == "LIGHT" else self.light_walls
        for wall in ghost_walls:
            pygame.draw.rect(surface, palette["ghost_wall"], wall, width=2, border_radius=4)

        # 2. Crtanje aktivnih dimenzionih zidova
        active_dim_walls = self.light_walls if dimension == "LIGHT" else self.dark_walls
        for wall in active_dim_walls:
            pygame.draw.rect(surface, palette["active_wall"], wall, border_radius=4)

        # 3. Crtanje univerzalnih zidova
        for wall in self.universal_walls:
            pygame.draw.rect(surface, palette["universal_wall"], wall)

        # 4. Crtanje ključa (Data Core) ako nije pokupljen
        if not self.key_collected and self.key_rect:
            if self.key_dimension == dimension:
                pygame.draw.rect(surface, palette["key"], self.key_rect, border_radius=6)
            else:
                # Obrisi ključa ako je u drugoj dimenziji
                pygame.draw.rect(surface, palette["ghost_wall"], self.key_rect, width=2, border_radius=6)

        # 5. Crtanje izlaza (Exit)
        if self.exit_rect:
            exit_color = palette["exit_open"] if self.key_collected else palette["exit_locked"]
            pygame.draw.rect(surface, exit_color, self.exit_rect, border_radius=6)