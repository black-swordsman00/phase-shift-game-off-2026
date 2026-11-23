# main.py
import sys
import pygame
from settings import WIDTH, HEIGHT, FPS, PLAYER_SPEED, SHIFT_COOLDOWN, PALETTES, TILE_SIZE
from levels import LEVELS, Level
from sound import SoundManager
from effects import EffectManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Phase Shift - Game Off 2026")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 17, bold=True)
        self.title_font = pygame.font.SysFont("consolas", 48, bold=True)
        self.subtitle_font = pygame.font.SysFont("consolas", 22, bold=True)
        self.sound = SoundManager()
        self.effects = EffectManager()

        self.state = "START"
        self.reset_campaign()

    def reset_campaign(self):
        self.level_index = 0
        self.total_time = 0.0
        self.total_shifts = 0
        self.deaths = 0
        self.load_level(self.level_index)

    def load_level(self, index):
        self.level = Level(LEVELS[index], level_number=index + 1)
        player_size = TILE_SIZE - 12
        self.player = pygame.Rect(
            self.level.player_start[0],
            self.level.player_start[1],
            player_size,
            player_size,
        )
        self.facing = (1, 0)
        self.dimension = "LIGHT"
        self.shift_timer = 0.0
        self.flash_alpha = 0
        self.flash_color = (255, 255, 255)
        self.death_timer = 0.0
        self.trail_timer = 0.0
        self.effects = EffectManager()

    def trigger_death(self):
        if self.death_timer > 0:
            return
        self.deaths += 1
        self.death_timer = 0.32
        self.flash_alpha = 180
        self.flash_color = (235, 40, 60)
        self.sound.play("fail")
        self.effects.add_burst(self.player.centerx, self.player.centery, (235, 50, 70), count=26)

    def shift_dimension(self):
        if self.shift_timer > 0 or self.death_timer > 0:
            return

        self.dimension = "DARK" if self.dimension == "LIGHT" else "LIGHT"
        self.shift_timer = SHIFT_COOLDOWN
        self.flash_alpha = 130
        self.flash_color = PALETTES[self.dimension]["flash"]
        self.total_shifts += 1
        self.sound.play("shift")

        burst_color = (0, 230, 180) if self.dimension == "DARK" else (65, 105, 225)
        self.effects.add_burst(self.player.centerx, self.player.centery, burst_color, count=14, lifetime=0.28)

        # Telefrag provera (ulazak u zid suprotne dimenzije)
        for wall in self.level.get_active_walls(self.dimension):
            if self.player.colliderect(wall):
                self.trigger_death()
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

        if dx != 0 or dy != 0:
            self.facing = (dx, dy)
            self.trail_timer -= dt
            if self.trail_timer <= 0:
                self.effects.add_trail(self.player, PALETTES[self.dimension]["player"])
                self.trail_timer = 0.045

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        active_walls = self.level.get_active_walls(self.dimension)

        self.player.x += round(dx * PLAYER_SPEED * dt)
        for wall in active_walls:
            if self.player.colliderect(wall):
                if dx > 0:
                    self.player.right = wall.left
                elif dx < 0:
                    self.player.left = wall.right

        self.player.y += round(dy * PLAYER_SPEED * dt)
        for wall in active_walls:
            if self.player.colliderect(wall):
                if dy > 0:
                    self.player.bottom = wall.top
                elif dy < 0:
                    self.player.top = wall.bottom

    def check_interactions(self):
        for guard in self.level.guards:
            if guard.dimension == self.dimension:
                if self.player.colliderect(guard.rect) or self.player.colliderect(guard.vision_rect):
                    self.trigger_death()
                    return

        if (
            not self.level.key_collected
            and self.level.key_rect
            and self.dimension == self.level.key_dimension
        ):
            if self.player.colliderect(self.level.key_rect):
                self.level.key_collected = True
                self.sound.play("key")
                self.effects.add_burst(self.level.key_rect.centerx, self.level.key_rect.centery, (255, 215, 0), count=20)

        if self.level.key_collected and self.level.exit_rect:
            if self.player.colliderect(self.level.exit_rect):
                self.sound.play("win")
                if self.level_index + 1 < len(LEVELS):
                    self.level_index += 1
                    self.load_level(self.level_index)
                else:
                    self.state = "VICTORY"

    def draw_player(self, palette):
        if self.death_timer > 0:
            return
        pygame.draw.rect(self.screen, palette["player"], self.player, border_radius=6)

        # Oči igrača koje prate smer kretanja
        cx, cy = self.player.center
        fx, fy = self.facing
        ox = fx * 5
        oy = fy * 5
        if abs(fx) >= abs(fy):
            e1 = (cx + ox, cy - 5)
            e2 = (cx + ox, cy + 5)
        else:
            e1 = (cx - 5, cy + oy)
            e2 = (cx + 5, cy + oy)
        pygame.draw.circle(self.screen, (255, 255, 255), e1, 3)
        pygame.draw.circle(self.screen, (255, 255, 255), e2, 3)

        # Vizuelni Cooldown bar iznad igrača dok se Shift puni
        if self.shift_timer > 0:
            ratio = 1.0 - (self.shift_timer / SHIFT_COOLDOWN)
            bar_w = self.player.width
            bar_h = 4
            bar_x = self.player.left
            bar_y = self.player.top - 8
            pygame.draw.rect(self.screen, (100, 105, 120), (bar_x, bar_y, bar_w, bar_h), border_radius=2)
            pygame.draw.rect(self.screen, (0, 230, 180), (bar_x, bar_y, int(bar_w * ratio), bar_h), border_radius=2)

    def draw_centered_text(self, text, font, color, y_offset):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
        self.screen.blit(surf, rect)

    def draw_start_screen(self):
        self.screen.fill((16, 19, 28))
        self.draw_centered_text("PHASE SHIFT", self.title_font, (0, 230, 180), -120)
        self.draw_centered_text("GitHub Game Off 2026 - Theme: SHIFT", self.subtitle_font, (170, 180, 200), -65)
        self.draw_centered_text("[WASD / Arrows] Move", self.font, (235, 240, 245), 0)
        self.draw_centered_text("[SPACE / SHIFT] Shift Dimension", self.font, (235, 240, 245), 30)
        self.draw_centered_text("Red guards periodically turn around to check behind!", self.font, (235, 90, 90), 70)
        self.draw_centered_text("Collect the yellow Core and reach the green Exit (10 Levels).", self.font, (245, 195, 65), 100)
        self.draw_centered_text("Press SPACE or ENTER to Start", self.subtitle_font, (0, 255, 135), 160)

    def draw_victory_screen(self):
        self.screen.fill((16, 19, 28))
        self.draw_centered_text("ALL 10 SECTORS BREACHED!", self.title_font, (0, 255, 135), -110)
        self.draw_centered_text(f"Total Time: {self.total_time:.1f}s", self.subtitle_font, (235, 240, 245), -30)
        self.draw_centered_text(f"Total Phase Shifts: {self.total_shifts}", self.subtitle_font, (0, 230, 180), 10)
        self.draw_centered_text(f"Restarts / Caught: {self.deaths}", self.subtitle_font, (235, 90, 90), 50)
        self.draw_centered_text("Press R to Play Again", self.subtitle_font, (245, 195, 65), 125)

    def draw_ui_and_effects(self):
        palette = PALETTES[self.dimension]
        self.effects.draw(self.screen)
        self.draw_player(palette)

        if self.flash_alpha > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((*self.flash_color, int(self.flash_alpha)))
            self.screen.blit(flash_surf, (0, 0))

        status_text = (
            f"LVL: {self.level_index + 1}/{len(LEVELS)} | "
            f"DIM: {self.dimension} | "
            f"CORE: {'OK' if self.level.key_collected else 'MISSING'} | "
            f"TIME: {self.total_time:.1f}s | "
            f"SHIFTS: {self.total_shifts} | [R] Reset"
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
                    if self.state == "START":
                        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self.reset_campaign()
                            self.state = "PLAYING"
                    elif self.state == "PLAYING":
                        if event.key in (pygame.K_SPACE, pygame.K_LSHIFT, pygame.K_RSHIFT):
                            self.shift_dimension()
                        elif event.key == pygame.K_r:
                            self.deaths += 1
                            self.load_level(self.level_index)
                    elif self.state == "VICTORY":
                        if event.key == pygame.K_r:
                            self.reset_campaign()
                            self.state = "PLAYING"

            if self.state == "START":
                self.draw_start_screen()
            elif self.state == "PLAYING":
                self.total_time += dt
                if self.shift_timer > 0:
                    self.shift_timer = max(0.0, self.shift_timer - dt)
                if self.flash_alpha > 0:
                    self.flash_alpha = max(0, self.flash_alpha - 600 * dt)

                self.effects.update(dt)

                if self.death_timer > 0:
                    self.death_timer -= dt
                    if self.death_timer <= 0:
                        self.load_level(self.level_index)
                else:
                    self.level.update_guards(dt)
                    self.move_player(dt)
                    self.check_interactions()

                self.level.draw(self.screen, self.dimension)
                self.draw_ui_and_effects()
            elif self.state == "VICTORY":
                self.draw_victory_screen()

            pygame.display.flip()


if __name__ == "__main__":
    Game().run()