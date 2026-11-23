# levels.py
import pygame
from settings import TILE_SIZE, PALETTES
from enemies import Guard

# Legenda:
# '#' - Zid u obe dimenzije
# 'L' - Zid samo u LIGHT dimenziji
# 'D' - Zid samo u DARK dimenziji
# 'P' - Početna pozicija igrača
# '1' - Ključ (Data Core) u LIGHT dimenziji
# '2' - Ključ (Data Core) u DARK dimenziji
# 'G' - Čuvar LIGHT (horizontalno)
# 'S' - Čuvar DARK (horizontalno)
# 'V' - Čuvar LIGHT (vertikalno)
# 'W' - Čuvar DARK (vertikalno)
# 'X' - Pametni čuvar LIGHT (okreće se i proverava leđa)
# 'Z' - Pametni čuvar DARK (okreće se i proverava leđa)
# 'E' - Izlaz (Exit)

LEVELS = [
    # NIVO 1: Osnove prebacivanja dimenzija
    [
        "####################",
        "#P   L        D   2#",
        "#    L   ##   D    #",
        "#    L   ##   D    #",
        "#        ##        #",
        "#   DDDDDDDDDDDD   #",
        "#      G           #",
        "#   LLLLLLLLLLLL   #",
        "#           S      #",
        "#    D   ##   L    #",
        "#    D   ##   L    #",
        "#    D        L   E#",
        "#    D   ##   L    #",
        "#        ##        #",
        "####################",
    ],
    # NIVO 2: Ukrštanje patrola
    [
        "####################",
        "#P #   L   D   #  E#",
        "#  #   L   D   #   #",
        "#  #   L   D   #   #",
        "#  #####   #####   #",
        "#      D   L  G    #",
        "#  LLLLL   DDDDD   #",
        "#    S             #",
        "#  DDDDD   LLLLL   #",
        "#      L   D  G    #",
        "#  #####   #####   #",
        "#  #   D   L   #   #",
        "#  #   D   L   #   #",
        "# 1#   D   L   #   #",
        "####################",
    ],
    # NIVO 3: Vertikalni lavirint
    [
        "####################",
        "#P  L   D   L   D 2#",
        "#   L V D W L V D  #",
        "#   L   D   L   D  #",
        "#   L   D   L   D  #",
        "#   #   #   #   #  #",
        "#                  #",
        "#  ###  #####  ### #",
        "#                  #",
        "#   #   #   #   #  #",
        "#   D   L   D   L  #",
        "#   D W L V D W L  #",
        "#   D   L   D   L  #",
        "#   D   L   D   L E#",
        "####################",
    ],
    # NIVO 4: Centralni trezor
    [
        "####################",
        "#P       ##       E#",
        "#  LLLL  ##  DDDD  #",
        "#  L  L      D  D  #",
        "#  L  L  G   D  D  #",
        "#  LLLL      DDDD  #",
        "#        ##        #",
        "#   V   #1 #   W   #",
        "#        #         #",
        "#  DDDD      LLLL  #",
        "#  D  D  S   L  L  #",
        "#  D  D      L  L  #",
        "#  DDDD  ##  LLLL  #",
        "#        ##        #",
        "####################",
    ],
    # NIVO 5: Upoznavanje sa pametnim čuvarima (X / Z)
    [
        "####################",
        "#P      L   D     E#",
        "#  ###  L   D  ### #",
        "#  #    L   D    # #",
        "#  #  X       Z  # #",
        "#  #####     ##### #",
        "#      D     L     #",
        "#  LLL D  1  L DDD #",
        "#      D     L     #",
        "#  #####     ##### #",
        "#  #  Z       X  # #",
        "#  #    D   L    # #",
        "#  ###  D   L  ### #",
        "#       D   L      #",
        "####################",
    ],
    # NIVO 6: Dvostruki mostovi (opasnost od telefrag-a)
    [
        "####################",
        "#P L D L D L D L  2#",
        "#  L D L D L D L   #",
        "#  # # # # # # #   #",
        "#      G   S       #",
        "#  # # # # # # #   #",
        "#  D L D L D L D   #",
        "#  D L D L D L D   #",
        "#  # # # # # # #   #",
        "#      Z   X       #",
        "#  # # # # # # #   #",
        "#  L D L D L D L   #",
        "#  L D L D L D L  E#",
        "#                  #",
        "####################",
    ],
    # NIVO 7: Rotirajući prsten
    [
        "####################",
        "#P        V       E#",
        "#  ##############  #",
        "#  #   L    D   #  #",
        "#  #   L  X D   #  #",
        "#  #   LLLLLL   #  #",
        "#W #            # V#",
        "#  #   DDDDDD   #  #",
        "#  #   D  Z L   #  #",
        "#  #   D 1  L   #  #",
        "#  ########### ##  #",
        "#         W        #",
        "#  LLLLLLLLLLLLLL  #",
        "#  DDDDDDDDDDDDDD  #",
        "####################",
    ],
    # NIVO 8: Brzi koridori (usklađivanje tajminga)
    [
        "####################",
        "#P  L   X   D   Z 2#",
        "#   L  ###  D  ### #",
        "#   L   #   D   #  #",
        "#   #####   #####  #",
        "#       W   V      #",
        "#  DDDDD     LLLLL #",
        "#  D   D  S  L   L #",
        "#  DDDDD     LLLLL #",
        "#       V   W      #",
        "#   #####   #####  #",
        "#   D   #   L   #  #",
        "#   D  ###  L  ### #",
        "#   D   Z   L   X E#",
        "####################",
    ],
    # NIVO 9: Šahovnica dimenzija
    [
        "####################",
        "#P L D L D L D L D #",
        "#  D L D L D L D L #",
        "#  L D L X D L D L #",
        "#  D L D L D Z L D #",
        "#  # # # # # # # # #",
        "#    G         S   #",
        "#  # # # # # # # # #",
        "#  L D L Z D L D L #",
        "#  D L D L D X L D #",
        "#  L D L D L D L D #",
        "#  D L D 1 D L D L #",
        "#  # # # # # # # # #",
        "#                 E#",
        "####################",
    ],
    # NIVO 10: Jezgro sistema (Finalni izazov)
    [
        "####################",
        "#P  L    X    D   E#",
        "#   L  #####  D    #",
        "#  V   D   L   W   #",
        "#  #####   #####   #",
        "#  Z     S     X   #",
        "#  #  LLLLLLL  #   #",
        "#  #  L  2  L  #   #",
        "#  #  LLL DLL  #   #",
        "#  X     G     Z   #",
        "#  #####   #####   #",
        "#  W   L   D   V   #",
        "#   D  #####  L    #",
        "#   D    Z    L    #",
        "####################",
    ],
]


class Level:
    def __init__(self, level_data, level_number=1):
        self.universal_walls = []
        self.light_walls = []
        self.dark_walls = []
        self.guards = []
        self.player_start = (TILE_SIZE, TILE_SIZE)
        self.key_rect = None
        self.key_dimension = None
        self.key_collected = False
        self.exit_rect = None
        self.speed_mult = 1.0 + (level_number - 1) * 0.04  # Blago ubrzanje čuvara po nivou

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
                elif cell == "G":
                    self.guards.append(Guard(x, y, "LIGHT", direction=(1, 0), speed_mult=self.speed_mult))
                elif cell == "S":
                    self.guards.append(Guard(x, y, "DARK", direction=(-1, 0), speed_mult=self.speed_mult))
                elif cell == "V":
                    self.guards.append(Guard(x, y, "LIGHT", direction=(0, 1), speed_mult=self.speed_mult))
                elif cell == "W":
                    self.guards.append(Guard(x, y, "DARK", direction=(0, -1), speed_mult=self.speed_mult))
                elif cell == "X":
                    self.guards.append(Guard(x, y, "LIGHT", direction=(1, 0), smart=True, speed_mult=self.speed_mult * 1.15))
                elif cell == "Z":
                    self.guards.append(Guard(x, y, "DARK", direction=(-1, 0), smart=True, speed_mult=self.speed_mult * 1.15))
                elif cell == "E":
                    self.exit_rect = rect

    def get_active_walls(self, dimension):
        if dimension == "LIGHT":
            return self.universal_walls + self.light_walls
        return self.universal_walls + self.dark_walls

    def update_guards(self, dt):
        for guard in self.guards:
            guard.update(dt, self.get_active_walls(guard.dimension))

    def draw(self, surface, dimension):
        palette = PALETTES[dimension]
        surface.fill(palette["bg"])

        ghost_walls = self.dark_walls if dimension == "LIGHT" else self.light_walls
        for wall in ghost_walls:
            pygame.draw.rect(surface, palette["ghost_wall"], wall, width=2, border_radius=4)

        active_dim_walls = self.light_walls if dimension == "LIGHT" else self.dark_walls
        for wall in active_dim_walls:
            pygame.draw.rect(surface, palette["active_wall"], wall, border_radius=4)

        for wall in self.universal_walls:
            pygame.draw.rect(surface, palette["universal_wall"], wall)

        if not self.key_collected and self.key_rect:
            if self.key_dimension == dimension:
                pygame.draw.rect(surface, palette["key"], self.key_rect, border_radius=6)
            else:
                pygame.draw.rect(surface, palette["ghost_wall"], self.key_rect, width=2, border_radius=6)

        if self.exit_rect:
            exit_color = palette["exit_open"] if self.key_collected else palette["exit_locked"]
            pygame.draw.rect(surface, exit_color, self.exit_rect, border_radius=6)

        for guard in self.guards:
            guard.draw(surface, dimension)