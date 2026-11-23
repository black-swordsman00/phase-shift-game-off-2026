# enemies.py
import random
import pygame
from settings import TILE_SIZE, PALETTES

BASE_GUARD_SPEED = 125
VISION_LENGTH = TILE_SIZE * 3 + 15


class Guard:
    def __init__(self, x, y, dimension, direction=(1, 0), smart=False, speed_mult=1.0):
        size = TILE_SIZE - 12
        self.rect = pygame.Rect(x + 6, y + 6, size, size)
        self.dimension = dimension
        self.dx, self.dy = direction
        self.vision_rect = pygame.Rect(0, 0, 0, 0)
        self.smart = smart
        self.speed = BASE_GUARD_SPEED * speed_mult

        # Tajmer za okretanje i proveru okoline (kod pametnih čuvara)
        self.scan_timer = random.uniform(1.8, 3.0)
        self.pause_timer = 0.0

    def update(self, dt, active_walls):
        if self.pause_timer > 0:
            self.pause_timer -= dt
            self._update_vision(active_walls)
            return

        if self.smart:
            self.scan_timer -= dt
            if self.scan_timer <= 0:
                self.dx *= -1
                self.dy *= -1
                self.pause_timer = 0.35
                self.scan_timer = random.uniform(2.0, 3.2)
                self._update_vision(active_walls)
                return

        self.rect.x += round(self.dx * self.speed * dt)
        self.rect.y += round(self.dy * self.speed * dt)

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
        if self.dx > 0:
            vision = pygame.Rect(self.rect.right, self.rect.y - 4, VISION_LENGTH, self.rect.height + 8)
        elif self.dx < 0:
            vision = pygame.Rect(self.rect.left - VISION_LENGTH, self.rect.y - 4, VISION_LENGTH, self.rect.height + 8)
        elif self.dy > 0:
            vision = pygame.Rect(self.rect.x - 4, self.rect.bottom, self.rect.width + 8, VISION_LENGTH)
        else:
            vision = pygame.Rect(self.rect.x - 4, self.rect.top - VISION_LENGTH, self.rect.width + 8, VISION_LENGTH)

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

    def _draw_eyes(self, surface):
        cx, cy = self.rect.center
        offset_x = self.dx * 6
        offset_y = self.dy * 6

        if self.dx != 0:
            eye1 = (cx + offset_x, cy - 5)
            eye2 = (cx + offset_x, cy + 5)
        else:
            eye1 = (cx - 5, cy + offset_y)
            eye2 = (cx + 5, cy + offset_y)

        pygame.draw.circle(surface, (255, 255, 255), eye1, 3)
        pygame.draw.circle(surface, (255, 255, 255), eye2, 3)

    def draw(self, surface, current_dimension):
        palette = PALETTES[current_dimension]

        if current_dimension == self.dimension:
            if self.vision_rect.width > 0 and self.vision_rect.height > 0:
                vision_surf = pygame.Surface((self.vision_rect.width, self.vision_rect.height), pygame.SRCALPHA)
                alpha = 105 if self.smart else 80
                vision_surf.fill((255, 90, 20, alpha))
                surface.blit(vision_surf, self.vision_rect.topleft)

            body_color = (220, 40, 40) if self.smart else (235, 115, 20)
            pygame.draw.rect(surface, body_color, self.rect, border_radius=6)
            self._draw_eyes(surface)
        else:
            pygame.draw.rect(surface, palette["ghost_wall"], self.rect, width=2, border_radius=6)