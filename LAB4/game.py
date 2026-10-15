import math
import random

import pygame

WIDTH, HEIGHT = 800, 560
FPS = 60
BG = (30, 35, 25)
MAGAZINE_CAPACITY = 12
RELOAD_DURATION = 2.0
PLAYER_MAX_HP = 3
INVULNERABILITY_DURATION = 1.0
BARREL_COUNT = 4
BARREL_EXPLOSION_RADIUS = 115


class Zombie:
    SPEED = 1.5
    SIZE = 30
    MAX_HP = 3
    COLOR = (60, 140, 60)

    def __init__(self, x, y):
        self.size = self.SIZE
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.x = float(x)
        self.y = float(y)
        self.speed = self.SPEED
        self.color = self.COLOR
        self.hp = self.MAX_HP
        self.wobble = random.uniform(0, 6.28)
        self.frame = 0

    def update(self, player_pos):
        px, py = player_pos
        cx, cy = self.rect.center
        dx, dy = px - cx, py - cy
        distance = math.hypot(dx, dy)
        if distance:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed
            self.rect.topleft = (round(self.x), round(self.y))
        self.frame += 1

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def draw(self, screen):
        wobble_y = int(math.sin(self.frame * 0.2) * 3)
        draw_rect = self.rect.move(0, wobble_y)
        pygame.draw.rect(screen, self.color, draw_rect, border_radius=5)
        eye_y = draw_rect.y + self.size // 3
        eye_radius = max(2, self.size // 8)
        for eye_x in (draw_rect.x + self.size // 4, draw_rect.x + 3 * self.size // 4):
            pygame.draw.circle(screen, (200, 40, 40), (eye_x, eye_y), eye_radius)


class FastZombie(Zombie):
    SPEED = 2.8
    SIZE = 22
    MAX_HP = 1
    COLOR = (210, 150, 45)


class TankZombie(Zombie):
    SPEED = 0.8
    SIZE = 42
    MAX_HP = 6
    COLOR = (125, 75, 60)


class Bullet:
    SPEED = 10
    SIZE = 8

    def __init__(self, x, y, target_pos):
        tx, ty = target_pos
        dx, dy = tx - x, ty - y
        distance = math.hypot(dx, dy)
        self.x = float(x)
        self.y = float(y)
        self.vx = dx / distance * self.SPEED
        self.vy = dy / distance * self.SPEED
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)
        self._sync_rect()

    def _sync_rect(self):
        self.rect.center = (round(self.x), round(self.y))

    def update(self, width, height):
        self.x += self.vx
        self.y += self.vy
        self._sync_rect()
        return -self.SIZE <= self.x <= width + self.SIZE and -self.SIZE <= self.y <= height + self.SIZE


class Barrel:
    SIZE = 36

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.SIZE, self.SIZE)
        self.exploded = False

    def explode(self):
        if self.exploded:
            return False
        self.exploded = True
        return True

    def draw(self, screen):
        pygame.draw.rect(screen, (145, 73, 35), self.rect, border_radius=6)
        pygame.draw.rect(screen, (220, 170, 70), (self.rect.x + 4, self.rect.y + 8, self.SIZE - 8, 5))
        pygame.draw.rect(screen, (220, 170, 70), (self.rect.x + 4, self.rect.y + 23, self.SIZE - 8, 5))
        pygame.draw.circle(screen, (245, 210, 95), self.rect.center, 5)


class Explosion:
    DURATION = 0.4

    def __init__(self, center, start_time):
        self.center = center
        self.start_time = start_time

    def is_active(self, now):
        return now - self.start_time < self.DURATION

    def draw(self, screen, now):
        progress = min(1.0, max(0.0, (now - self.start_time) / self.DURATION))
        radius = max(3, int(BARREL_EXPLOSION_RADIUS * progress))
        pygame.draw.circle(screen, (255, 135, 35), self.center, radius, 4)


def spawn_zombie(width, height, player_rect, margin=120, zombie_type=Zombie, obstacles=None):
    size = zombie_type.SIZE
    safe_player_area = player_rect.inflate(margin, margin)
    obstacles = obstacles or []

    for _ in range(200):
        x = random.randint(0, width - size)
        y = random.randint(0, height - size)
        rect = pygame.Rect(x, y, size, size)
        if rect.colliderect(safe_player_area):
            continue
        if any(rect.colliderect(obstacle.inflate(8, 8)) for obstacle in obstacles):
            continue
        return zombie_type(x, y)

    fallback_positions = (
        (0, 0),
        (width - size, 0),
        (0, height - size),
        (width - size, height - size),
    )
    for x, y in fallback_positions:
        rect = pygame.Rect(x, y, size, size)
        if not rect.colliderect(safe_player_area) and not any(
            rect.colliderect(obstacle.inflate(8, 8)) for obstacle in obstacles
        ):
            return zombie_type(x, y)
    return zombie_type(fallback_positions[0][0], fallback_positions[0][1])


SPEED = 4


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (60, 160, 220)
        self.bullets = []
        self.shoot_cooldown = 0
        self.hp = PLAYER_MAX_HP
        self.invulnerable_until = 0.0
        self.ammo = MAGAZINE_CAPACITY
        self.reload_end_time = None

    @property
    def is_reloading(self):
        return self.reload_end_time is not None

    def move(self, keys, width, height):
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = SPEED
        self.rect.x = max(0, min(width - self.rect.width, self.rect.x + dx))
        self.rect.y = max(0, min(height - self.rect.height, self.rect.y + dy))
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self, target_pos):
        if self.is_reloading or self.ammo <= 0 or self.shoot_cooldown > 0:
            return False
        cx, cy = self.rect.center
        if target_pos == (cx, cy):
            return False
        self.bullets.append(Bullet(cx, cy, target_pos))
        self.ammo -= 1
        self.shoot_cooldown = 15
        return True

    def start_reload(self, now):
        if self.is_reloading or self.ammo >= MAGAZINE_CAPACITY:
            return False
        self.reload_end_time = now + RELOAD_DURATION
        return True

    def take_damage(self, now):
        if now < self.invulnerable_until:
            return False
        self.hp = max(0, self.hp - 1)
        self.invulnerable_until = now + INVULNERABILITY_DURATION
        return True

    def update(self, now, width, height):
        if self.reload_end_time is not None and now >= self.reload_end_time:
            self.ammo = MAGAZINE_CAPACITY
            self.reload_end_time = None
        self.bullets = [bullet for bullet in self.bullets if bullet.update(width, height)]

    def draw(self, screen, now):
        if now < self.invulnerable_until and int(now * 10) % 2 == 0:
            return
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        for bullet in self.bullets:
            pygame.draw.circle(screen, (255, 220, 60), bullet.rect.center, bullet.SIZE // 2)


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zombie Escape")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20)
        self.small_font = pygame.font.SysFont("monospace", 15)
        self.big_font = pygame.font.SysFont("monospace", 44, bold=True)
        self.reset()

    def reset(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        barrel_positions = ((100, 100), (664, 100), (100, 424), (664, 424))
        self.barrels = [Barrel(x, y) for x, y in barrel_positions]
        self.explosions = []
        self.zombies = []
        self.score = 0
        self.kill_bonus = 0
        self.wave = 1
        self.kills = 0
        self.kills_to_next = 8
        self.game_over = False
        self.start_time = pygame.time.get_ticks() / 1000
        self._spawn_zombies(4)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if self.game_over:
                    self.reset()
                else:
                    self.player.start_reload(pygame.time.get_ticks() / 1000)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
                self.player.shoot(event.pos)
        return True

    def _register_kill(self, zombie):
        if zombie in self.zombies:
            self.zombies.remove(zombie)
            self.kills += 1
            self.kill_bonus += 10

    def _spawn_zombies(self, count):
        zombie_types = [Zombie]
        if self.wave >= 2:
            zombie_types.append(FastZombie)
        if self.wave >= 3:
            zombie_types.append(TankZombie)
        wave_types = random.sample(zombie_types, min(count, len(zombie_types)))
        wave_types.extend(random.choice(zombie_types) for _ in range(count - len(wave_types)))
        random.shuffle(wave_types)
        obstacles = [barrel.rect for barrel in self.barrels]
        for zombie_type in wave_types:
            self.zombies.append(
                spawn_zombie(
                    WIDTH,
                    HEIGHT,
                    self.player.rect,
                    zombie_type=zombie_type,
                    obstacles=obstacles,
                )
            )

    def _explode_barrel(self, barrel, now):
        if not barrel.explode():
            return
        self.barrels.remove(barrel)
        self.explosions.append(Explosion(barrel.rect.center, now))
        for zombie in self.zombies[:]:
            distance = math.hypot(
                zombie.rect.centerx - barrel.rect.centerx,
                zombie.rect.centery - barrel.rect.centery,
            )
            if distance <= BARREL_EXPLOSION_RADIUS:
                self._register_kill(zombie)

    def _handle_bullet_collisions(self, now):
        for bullet in self.player.bullets[:]:
            hit_barrel = next((barrel for barrel in self.barrels if bullet.rect.colliderect(barrel.rect)), None)
            if hit_barrel is not None:
                self.player.bullets.remove(bullet)
                self._explode_barrel(hit_barrel, now)
                continue

            for zombie in self.zombies[:]:
                if bullet.rect.colliderect(zombie.rect):
                    self.player.bullets.remove(bullet)
                    if zombie.hit():
                        self._register_kill(zombie)
                    break

    def _advance_waves(self):
        if self.kills >= self.kills_to_next:
            self.kills = 0
            self.wave += 1
            self.kills_to_next = 8 + self.wave * 2
            self._spawn_zombies(self.wave + 3)
        elif not self.zombies:
            remaining_kills = self.kills_to_next - self.kills
            self._spawn_zombies(min(4, remaining_kills))

    def update(self):
        if self.game_over:
            return
        now = pygame.time.get_ticks() / 1000
        keys = pygame.key.get_pressed()
        self.player.move(keys, WIDTH, HEIGHT)
        self.player.update(now, WIDTH, HEIGHT)

        for zombie in self.zombies:
            zombie.update(self.player.rect.center)

        self._handle_bullet_collisions(now)

        for zombie in self.zombies:
            if zombie.rect.colliderect(self.player.rect) and self.player.take_damage(now):
                if self.player.hp <= 0:
                    self.game_over = True
                break

        self.explosions = [explosion for explosion in self.explosions if explosion.is_active(now)]
        self._advance_waves()
        self.score = int(now - self.start_time) + self.kill_bonus

    def draw(self):
        now = pygame.time.get_ticks() / 1000
        self.screen.fill(BG)
        for x in range(0, WIDTH, 60):
            pygame.draw.line(self.screen, (40, 45, 35), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 60):
            pygame.draw.line(self.screen, (40, 45, 35), (0, y), (WIDTH, y), 1)

        for explosion in self.explosions:
            explosion.draw(self.screen, now)
        for barrel in self.barrels:
            barrel.draw(self.screen)
        for zombie in self.zombies:
            zombie.draw(self.screen)
        self.player.draw(self.screen, now)

        pygame.draw.rect(self.screen, (15, 20, 15), pygame.Rect(0, 0, WIDTH, 64))
        if self.player.reload_end_time is not None:
            reload_remaining = max(0.0, self.player.reload_end_time - now)
            ammo_text = f"Reloading: {reload_remaining:.1f}s"
        else:
            ammo_text = f"Ammo: {self.player.ammo}/{MAGAZINE_CAPACITY}"
        hud = self.font.render(
            f"HP: {self.player.hp}/{PLAYER_MAX_HP}   {ammo_text}   "
            f"Wave: {self.wave}   Score: {self.score}   Kills: {self.kills}/{self.kills_to_next}",
            True,
            (160, 220, 120),
        )
        controls = self.small_font.render(
            "Move: WASD/Arrows   Shoot: Left Click   Reload: R   Restart: R after game over",
            True,
            (210, 210, 190),
        )
        self.screen.blit(hud, (8, 7))
        self.screen.blit(controls, (8, 39))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))
            title = self.big_font.render("DEVOURED!", True, (180, 40, 40))
            details = self.font.render(
                f"Wave {self.wave} | Score {self.score} | Press R to restart",
                True,
                (220, 220, 220),
            )
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 40))
            self.screen.blit(details, (WIDTH // 2 - details.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    engine = GameEngine()
    engine.run()
