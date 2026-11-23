# main.py
import sys
import pygame
from settings import WIDTH, HEIGHT, FPS, PLAYER_SPEED, SHIFT_COOLDOWN, PALETTES, TILE_SIZE
from levels import LEVELS, Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Phase Shift - Game Off 2026")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20, bold=True)

        self.level_index = 0
        self.load_level(self.level_index)

    def load_level(self, index):
        self.level = Level(LEVELS[index])
        player_size = TILE_SIZE - 12
        self.player = pygame.Rect(
            self.level.player_start[0],
            self.level.player_start[1],
            player_size,
            player_size,
        )
        self.dimension = "LIGHT"
        self.shift_timer = 0.0
        self.flash_alpha = 0

    def shift_dimension(self):
        if self.shift_timer > 0:
            return

        self.dimension = "DARK" if self.dimension == "LIGHT" else "LIGHT"
        self.shift_timer = SHIFT_COOLDOWN
        self.flash_alpha = 140  # Jačina bljeska

        # Provera da li se igrač materijalizovao unutar zida (Telefrag!)
        for wall in self.level.get_active_walls(self.dimension):
            if self.player.colliderect(wall):
                self.load_level(self.level_index)
                return

    def move_player(self, dt):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1

        # Normalizacija dijagonalnog kretanja
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        active_walls = self.level.get_active_walls(self.dimension)

        # Pomeranje i sudari po X osi
        self.player.x += round(dx * PLAYER_SPEED * dt)
        for wall in active_walls:
            if self.player.colliderect(wall):
                if dx > 0:
                    self.player.right = wall.left
                elif dx < 0:
                    self.player.left = wall.right

        # Pomeranje i sudari po Y osi
        self.player.y += round(dy * PLAYER_SPEED * dt)
        for wall in active_walls:
            if self.player.colliderect(wall):
                if dy > 0:
                    self.player.bottom = wall.top
                elif dy < 0:
                    self.player.top = wall.bottom

    def check_interactions(self):
        # Skupljanje ključa (samo ako smo u istoj dimenziji kao ključ)
        if (
            not self.level.key_collected
            and self.level.key_rect
            and self.dimension == self.level.key_dimension
        ):
            if self.player.colliderect(self.level.key_rect):
                self.level.key_collected = True

        # Ulazak u Exit portal
        if self.level.key_collected and self.level.exit_rect:
            if self.player.colliderect(self.level.exit_rect):
                self.level_index = (self.level_index + 1) % len(LEVELS)
                self.load_level(self.level_index)

    def draw_ui_and_effects(self):
        palette = PALETTES[self.dimension]

        # Iscrtavanje igrača
        pygame.draw.rect(self.screen, palette["player"], self.player, border_radius=5)

        # Bljesak pri promeni dimenzije
        if self.flash_alpha > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((*palette["flash"], int(self.flash_alpha)))
            self.screen.blit(flash_surf, (0, 0))

        # HUD tekst na vrhu ekrana
        status_text = (
            f"LVL: {self.level_index + 1}/{len(LEVELS)} | "
            f"DIM: {self.dimension} | "
            f"CORE: {'OK' if self.level.key_collected else 'MISSING'} | "
            f"[SPACE/SHIFT] Phase Shift  [R] Restart"
        )
        text_color = (20, 20, 25) if self.dimension == "LIGHT" else (235, 240, 245)
        text_surf = self.font.render(status_text, True, text_color)
        self.screen.blit(text_surf, (15, 10))

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_LSHIFT, pygame.K_RSHIFT):
                        self.shift_dimension()
                    elif event.key == pygame.K_r:
                        self.load_level(self.level_index)

            if self.shift_timer > 0:
                self.shift_timer = max(0.0, self.shift_timer - dt)
            if self.flash_alpha > 0:
                self.flash_alpha = max(0, self.flash_alpha - 600 * dt)

            self.move_player(dt)
            self.check_interactions()

            self.level.draw(self.screen, self.dimension)
            self.draw_ui_and_effects()
            pygame.display.flip()


if __name__ == "__main__":
    Game().run()