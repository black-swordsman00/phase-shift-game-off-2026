# effects.py
import random
import pygame


class Particle:
    def __init__(self, x, y, color, speed_range=(40, 180), lifetime=0.35, size=4):
        self.x = float(x)
        self.y = float(y)
        angle = random.uniform(0, 6.28318)
        speed = random.uniform(*speed_range)
        self.vx = speed * pygame.math.Vector2(1, 0).rotate_rad(angle).x
        self.vy = speed * pygame.math.Vector2(1, 0).rotate_rad(angle).y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt

    def draw(self, surface):
        if self.lifetime <= 0:
            return
        alpha = max(0, int(255 * (self.lifetime / self.max_lifetime)))
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
        surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))


class EffectManager:
    def __init__(self):
        self.particles = []
        self.trail = []  # (Rect, color, alpha)

    def add_burst(self, x, y, color, count=18, speed_range=(60, 220), lifetime=0.4):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, speed_range, lifetime))

    def add_trail(self, rect, color):
        self.trail.append([rect.copy(), color, 110.0])

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.lifetime > 0]

        for t in self.trail:
            t[2] -= 420.0 * dt
        self.trail = [t for t in self.trail if t[2] > 0]

    def draw(self, surface):
        for rect, color, alpha in self.trail:
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (*color, max(0, int(alpha))), (0, 0, rect.width, rect.height), border_radius=4)
            surface.blit(s, rect.topleft)

        for p in self.particles:
            p.draw(surface)