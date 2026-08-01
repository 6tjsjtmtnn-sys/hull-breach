import random

import pygame

import hud
import music
import sound
from constants import (
    BLACK,
    BOSS_HP,
    GRAVITY_CHARGE_AMOUNT,
    HAZARD_DAMAGE,
    HEART_PICKUP_MAX_DISTANCE,
    HEART_PICKUP_MAX_SPAWN_DELAY,
    HEART_PICKUP_MIN_DISTANCE,
    HEART_PICKUP_MIN_SPAWN_DELAY,
    MAX_OXYGEN,
    OXYGEN_DRAIN_RATE_BASE,
    OXYGEN_DRAIN_RATE_INCREMENT,
    OXYGEN_PICKUP_AMOUNT,
    PLAYER_HEARTS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STATION_BLUE,
    STOMP_BOUNCE,
    STOMP_TOLERANCE,
    SWEEP_DRONE_MAX_SPAWN_DELAY,
    SWEEP_DRONE_MIN_SPAWN_DELAY,
    TILE_SIZE,
    WARNING_ORANGE,
    WHITE,
)
from entities.boss import Boss
from entities.drone import Drone
from entities.flying_drone import FlyingDrone
from entities.heart_pickup import HeartPickup
from entities.particle import Particle
from entities.player import Player
from entities.projectile import Projectile
from entities.sweep_drone import SweepDrone
from levels.camera import Camera
from levels.level import Level
from levels.registry import LEVELS
from states.base_state import State
from states.game_over_state import GameOverState
from states.pause_state import PauseState

BACKGROUND_TOP = (16, 20, 34)
THRUSTER_SPAWN_CHANCE = 0.6
DRONE_SPARK_SPAWN_CHANCE = 0.05
STEAM_SPAWN_CHANCE = 0.06


def _build_background():
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for y in range(SCREEN_HEIGHT):
        t = y / SCREEN_HEIGHT
        color = tuple(round(a + (b - a) * t) for a, b in zip(BACKGROUND_TOP, BLACK))
        pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
    return surface


class PlayState(State):
    def __init__(self, game, level_index=0, gravity_charges=0):
        super().__init__(game)
        self.level_index = level_index
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        Player.containers = (self.updatable, self.drawable)
        Drone.containers = (self.updatable, self.drawable)
        FlyingDrone.containers = (self.updatable, self.drawable)
        Boss.containers = (self.updatable, self.drawable)
        SweepDrone.containers = (self.updatable, self.drawable)

        self.level = Level(LEVELS[level_index])
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, self.level.width, self.level.height)
        self.background = _build_background()

        spawn_x, spawn_y = self.level.player_spawn
        self.player = Player(spawn_x, spawn_y)
        self.enemies = [Drone(x, y) for x, y in self.level.drone_spawns] + [
            FlyingDrone(x, y) for x, y in self.level.flying_drone_spawns
        ]

        self.is_boss_level = self.level.boss_spawn is not None
        self.boss = Boss(*self.level.boss_spawn) if self.is_boss_level else None
        self.hearts = PLAYER_HEARTS
        self.heart_pickup = None
        self.heart_pickup_timer = random.uniform(HEART_PICKUP_MIN_SPAWN_DELAY, HEART_PICKUP_MAX_SPAWN_DELAY)
        self.sweep_drones = []
        self.sweep_drone_timer = random.uniform(SWEEP_DRONE_MIN_SPAWN_DELAY, SWEEP_DRONE_MAX_SPAWN_DELAY)

        self.oxygen = MAX_OXYGEN
        self.oxygen_drain_rate = OXYGEN_DRAIN_RATE_BASE + level_index * OXYGEN_DRAIN_RATE_INCREMENT
        self.gravity_charges = gravity_charges
        self.particles = []
        self.projectiles = []

        music.play_boss() if self.is_boss_level else music.play_gameplay()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
            self.next_state = PauseState(self.game, self)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            # Returning to normal gravity is always free — only flipping
            # away from it costs a charge. Otherwise running out of
            # charges while flipped (e.g. up at the ceiling) would stall
            # a level with no way back down.
            if self.player.gravity_dir < 0:
                self.player.flip_gravity()
                sound.play_flip()
            elif self.gravity_charges > 0:
                self.gravity_charges -= 1
                self.player.flip_gravity()
                sound.play_flip()
        elif event.type == pygame.KEYDOWN and pygame.K_0 <= event.key <= pygame.K_9:
            # DEV/TEST ONLY: number keys jump straight to that level (1-9,
            # 0 = level 10) for testing without replaying from the start.
            # Remove before shipping if not wanted as a real feature.
            digit = event.key - pygame.K_0
            target_index = 9 if digit == 0 else digit - 1
            if target_index < len(LEVELS):
                self.next_state = PlayState(
                    self.game, level_index=target_index, gravity_charges=self.gravity_charges
                )

    def update(self, dt):
        for entity in self.updatable:
            if isinstance(entity, Player):
                entity.update(dt, self.level.solid_tiles)
            else:
                entity.update(dt, self.level.solid_tiles, self.player)

        self.camera.update(self.player.position)
        self._check_hazards()
        self._check_boss_contact()
        self._check_pickups()
        self._update_particles(dt)
        self._update_projectiles(dt)

        if self.is_boss_level:
            self._update_heart_pickup(dt)
            self._update_sweep_drones(dt)
            if self.hearts <= 0:
                self.next_state = GameOverState(
                    self.game,
                    won=False,
                    title="REACTOR BREACH",
                    subtitle="The sentinel overwhelmed you.",
                )
            return

        self.oxygen = max(0.0, self.oxygen - self.oxygen_drain_rate * dt)
        if self.oxygen <= 0:
            self.next_state = GameOverState(self.game, won=False)
            return

        if self.level.exit_rect and self.player.rect.colliderect(self.level.exit_rect):
            if self.level_index + 1 < len(LEVELS):
                sound.play_success()
                self.next_state = PlayState(
                    self.game,
                    level_index=self.level_index + 1,
                    gravity_charges=self.gravity_charges,
                )
            else:
                self.next_state = GameOverState(self.game, won=True)

    def _apply_hit_damage(self):
        if self.is_boss_level:
            self.hearts -= 1
        else:
            self.oxygen = max(0.0, self.oxygen - HAZARD_DAMAGE)

    def _check_hazards(self):
        for enemy in list(self.enemies):
            if not self.player.rect.colliderect(enemy.rect):
                continue
            if self._is_stomp(enemy):
                self._defeat_enemy(enemy)
            elif self.player.take_hit(enemy.rect.centerx):
                self._apply_hit_damage()

        for hazard in self.level.hazard_tiles:
            if self.player.rect.colliderect(hazard.rect):
                if self.player.take_hit(hazard.rect.centerx):
                    self._apply_hit_damage()

    def _check_boss_contact(self):
        if self.boss is None or not self.player.rect.colliderect(self.boss.rect):
            return

        if self._is_stomp(self.boss):
            self.player.velocity.y = -STOMP_BOUNCE * self.player.gravity_dir
            sound.play_boss_hit()
            defeated = self.boss.take_hit()
            if defeated:
                self.boss.kill()
                self.boss = None
                self.next_state = GameOverState(
                    self.game,
                    won=True,
                    subtitle="You disabled the Reactor Sentinel and escaped.",
                )
        elif self.player.take_hit(self.boss.rect.centerx):
            self._apply_hit_damage()

    def _is_stomp(self, enemy):
        """Landing on an enemy from the gravity-relative 'above' side while
        falling into it defeats it instead of hurting the player."""
        player = self.player
        if player.gravity_dir > 0:
            falling = player.velocity.y > 0
            leading_edge = player.rect.bottom
            return falling and leading_edge <= enemy.rect.centery + STOMP_TOLERANCE
        else:
            falling = player.velocity.y < 0
            leading_edge = player.rect.top
            return falling and leading_edge >= enemy.rect.centery - STOMP_TOLERANCE

    def _defeat_enemy(self, enemy):
        self.enemies.remove(enemy)
        enemy.kill()
        self.player.velocity.y = -STOMP_BOUNCE * self.player.gravity_dir
        sound.play_defeat()
        for _ in range(10):
            vel = pygame.Vector2(random.uniform(-80, 80), random.uniform(-80, 80))
            self.particles.append(
                Particle(enemy.rect.centerx, enemy.rect.centery, vel, WARNING_ORANGE, lifetime=0.4, radius=3)
            )

    def _check_pickups(self):
        for pickup in self.level.oxygen_pickup_tiles:
            if self.player.rect.colliderect(pickup.rect):
                self.oxygen = min(MAX_OXYGEN, self.oxygen + OXYGEN_PICKUP_AMOUNT)
                self.level.tiles.remove(pickup)
                sound.play_pickup()

        for pickup in self.level.gravity_pickup_tiles:
            if self.player.rect.colliderect(pickup.rect):
                self.gravity_charges += GRAVITY_CHARGE_AMOUNT
                self.level.tiles.remove(pickup)
                sound.play_pickup()

    def _update_heart_pickup(self, dt):
        """Boss fight has no oxygen drain, so hearts are otherwise
        permanent damage — this bonus heart is the only way to recover
        one, appearing at a random spot every so often and disappearing
        again if it isn't reached in time."""
        if self.heart_pickup is not None:
            self.heart_pickup.update(dt)
            if self.player.rect.colliderect(self.heart_pickup.rect):
                self.hearts = min(PLAYER_HEARTS, self.hearts + 1)
                sound.play_pickup()
                self.heart_pickup = None
                self.heart_pickup_timer = random.uniform(HEART_PICKUP_MIN_SPAWN_DELAY, HEART_PICKUP_MAX_SPAWN_DELAY)
            elif not self.heart_pickup.alive:
                self.heart_pickup = None
                self.heart_pickup_timer = random.uniform(HEART_PICKUP_MIN_SPAWN_DELAY, HEART_PICKUP_MAX_SPAWN_DELAY)
            return

        self.heart_pickup_timer -= dt
        if self.heart_pickup_timer <= 0:
            if self.hearts < PLAYER_HEARTS:
                self._spawn_heart_pickup()
            else:
                self.heart_pickup_timer = random.uniform(HEART_PICKUP_MIN_SPAWN_DELAY, HEART_PICKUP_MAX_SPAWN_DELAY)

    def _spawn_heart_pickup(self):
        # Spawn near wherever the player currently is, not a random point
        # in the whole arena — with only HEART_PICKUP_LIFETIME seconds
        # before it disappears and a boss to dodge at the same time, a
        # pickup on the far side of the level would be effectively
        # unreachable.
        _, spawn_y = self.level.player_spawn
        margin = TILE_SIZE * 2
        offset = random.uniform(HEART_PICKUP_MIN_DISTANCE, HEART_PICKUP_MAX_DISTANCE)
        offset *= random.choice((-1, 1))
        x = self.player.rect.centerx + offset
        x = max(margin, min(self.level.width - margin, x))
        self.heart_pickup = HeartPickup(x, spawn_y)

    def _update_sweep_drones(self, dt):
        """Every so often, a flying drone sweeps straight across the
        screen from one edge to the other during the boss fight — extra,
        unpredictable danger on top of the boss itself. Reuses the same
        stomp/hurt handling as any other enemy via self.enemies; this
        just manages spawning and despawning once it's crossed off the
        opposite edge of the camera's current view."""
        margin = TILE_SIZE * 2
        view_left = self.camera.offset.x - margin
        view_right = self.camera.offset.x + SCREEN_WIDTH + margin

        for drone in list(self.sweep_drones):
            if drone not in self.enemies:
                # already defeated by a stomp elsewhere this frame
                self.sweep_drones.remove(drone)
                continue
            exited = (drone.direction > 0 and drone.rect.x > view_right) or (
                drone.direction < 0 and drone.rect.x < view_left
            )
            if exited:
                self.sweep_drones.remove(drone)
                self.enemies.remove(drone)
                drone.kill()

        self.sweep_drone_timer -= dt
        if self.sweep_drone_timer <= 0:
            self._spawn_sweep_drone()
            self.sweep_drone_timer = random.uniform(SWEEP_DRONE_MIN_SPAWN_DELAY, SWEEP_DRONE_MAX_SPAWN_DELAY)

    def _spawn_sweep_drone(self):
        margin = TILE_SIZE * 2
        direction = random.choice((-1, 1))
        if direction > 0:
            x = self.camera.offset.x - margin
        else:
            x = self.camera.offset.x + SCREEN_WIDTH + margin
        y = random.uniform(TILE_SIZE * 2, self.level.height - TILE_SIZE * 4)
        drone = SweepDrone(x, y, direction)
        self.sweep_drones.append(drone)
        self.enemies.append(drone)

    def _update_projectiles(self, dt):
        for enemy in self.enemies:
            if isinstance(enemy, FlyingDrone):
                projectile = enemy.try_fire(self.player)
                if projectile is not None:
                    self.projectiles.append(projectile)
                    sound.play_shoot()

        if self.boss is not None:
            projectile = self.boss.try_fire(self.player)
            if projectile is not None:
                self.projectiles.append(projectile)
                sound.play_shoot()

        for projectile in self.projectiles:
            projectile.update(dt)

        for projectile in list(self.projectiles):
            if projectile.rect.colliderect(self.player.rect):
                if self.player.take_hit(projectile.rect.centerx):
                    self._apply_hit_damage()
                self.projectiles.remove(projectile)

        self.projectiles = [
            p for p in self.projectiles if p.alive and self.level.width > p.rect.x > -p.rect.width
        ]

    def _update_particles(self, dt):
        if not self.player.on_ground or self.player.velocity.x != 0:
            if random.random() < THRUSTER_SPAWN_CHANCE:
                vel = pygame.Vector2(
                    -self.player.velocity.x * 0.15 + random.uniform(-15, 15),
                    random.uniform(-20, 20),
                )
                spawn_y = self.player.rect.bottom if self.player.gravity_dir > 0 else self.player.rect.top
                self.particles.append(
                    Particle(self.player.rect.centerx, spawn_y, vel, STATION_BLUE, lifetime=0.35, radius=3)
                )

        for enemy in self.enemies:
            if random.random() < DRONE_SPARK_SPAWN_CHANCE:
                vel = pygame.Vector2(random.uniform(-30, 30), random.uniform(-30, 30))
                self.particles.append(
                    Particle(enemy.rect.centerx, enemy.rect.centery, vel, WARNING_ORANGE, lifetime=0.3, radius=2)
                )

        for hazard in self.level.hazard_tiles:
            if random.random() < STEAM_SPAWN_CHANCE:
                vel = pygame.Vector2(random.uniform(-10, 10), random.uniform(-45, -20))
                self.particles.append(
                    Particle(hazard.rect.centerx, hazard.rect.top, vel, WHITE, lifetime=0.6, radius=4)
                )

        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for tile in self.level.tiles:
            tile.draw(screen, self.camera.offset)
        for entity in self.drawable:
            entity.draw(screen, self.camera.offset)
        for particle in self.particles:
            particle.draw(screen, self.camera.offset)
        for projectile in self.projectiles:
            projectile.draw(screen, self.camera.offset)
        if self.heart_pickup is not None:
            self.heart_pickup.draw(screen, self.camera.offset)

        if self.is_boss_level:
            hud.draw_player_hearts(screen, self.hearts, PLAYER_HEARTS)
            if self.boss is not None:
                hud.draw_boss_health_bar(screen, self.boss.hp, BOSS_HP)
        else:
            hud.draw_oxygen_bar(screen, self.oxygen, MAX_OXYGEN)

        hud.draw_gravity_charges(screen, self.gravity_charges)
        if self.level.exit_rect:
            hud.draw_exit_indicator(screen, self.level.exit_rect, self.camera.offset, self.level.exit_label)

        label = "REACTOR CORE" if self.is_boss_level else None
        hud.draw_level_indicator(screen, self.level_index, len(LEVELS), label=label)
