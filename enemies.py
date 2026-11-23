# enemies.py
import pygame
from settings import TILE_SIZE, PALETTES

GUARD_SPEED = 110
VISION_LENGTH = TILE_SIZE * 3


class Guard:
    def __init__(self, x, y, dimension, direction=(1, 0)):
        size = TILE_SIZE - 12
        self.rect = pygame.Rect(x + 6, y + 6, size, size)
        self.dimension = dimension
        self.dx, self.dy = direction
        self.vision_rect = pygame.Rect(0, 0, 0, 0)

    def update(self, dt, active_walls):
        # Pomeranje čuvara
        self.rect.x += round(self.dx * GUARD_SPEED * dt)
        self.rect.y += round(self.dy * GUARD_SPEED * dt)

        # Okretanje kada udari u zid
        for wall in active_walls:
            if self.rect.colliderect(wall):
                if self.dx > 0:
                    self.rect.right = wall.left
                elif self.dx < 0:
                    self.rect.left = wall.right
                elif self.dy > 0:
                    self.rect.bottom = wall.top
                elif self.dy < 0:
                    self.rect.top = wall.bottom

                self.dx *= -1
                self.dy *= -1
                break

        self._update_vision(active_walls)

    def _update_vision(self, active_walls):
        # Kreiranje snopa pogleda u smeru kretanja
        if self.dx > 0:
            vision = pygame.Rect(self.rect.right, self.rect.y - 4, VISION_LENGTH, self.rect.height + 8)
        elif self.dx < 0:
            vision = pygame.Rect(self.rect.left - VISION_LENGTH, self.rect.y - 4, VISION_LENGTH, self.rect.height + 8)
        elif self.dy > 0:
            vision = pygame.Rect(self.rect.x - 4, self.rect.bottom, self.rect.width + 8, VISION_LENGTH)
        else:
            vision = pygame.Rect(self.rect.x - 4, self.rect.top - VISION_LENGTH, self.rect.width + 8, VISION_LENGTH)

        # Sečenje vidnog polja ako ispred čuvara postoji zid
        for wall in active_walls:
            if vision.colliderect(wall):
                if self.dx > 0:
                    vision.width = max(0, wall.left - self.rect.right)
                elif self.dx < 0:
                    diff = wall.right - vision.left
                    vision.left = wall.right
                    vision.width = max(0, vision.width - diff)
                elif self.dy > 0:
                    vision.height = max(0, wall.top - self.rect.bottom)
                elif self.dy < 0:
                    diff = wall.bottom - vision.top
                    vision.top = wall.bottom
                    vision.height = max(0, vision.height - diff)

        self.vision_rect = vision

    def draw(self, surface, current_dimension):
        palette = PALETTES[current_dimension]

        if current_dimension == self.dimension:
            # Poluprovidni snop vidnog polja
            if self.vision_rect.width > 0 and self.vision_rect.height > 0:
                vision_surf = pygame.Surface((self.vision_rect.width, self.vision_rect.height), pygame.SRCALPHA)
                vision_surf.fill((255, 140, 0, 85))
                surface.blit(vision_surf, self.vision_rect.topleft)

            # Telo aktivnog čuvara
            pygame.draw.rect(surface, (235, 110, 20), self.rect, border_radius=6)
        else:
            # Silueta čuvara iz druge dimenzije
            pygame.draw.rect(surface, palette["ghost_wall"], self.rect, width=2, border_radius=6)