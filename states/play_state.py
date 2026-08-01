import random

import pygame

import hud
import music
import sound
from constants import (
    BLACK,
    GRAVITY_CHARGE_AMOUNT,
    HAZARD_DAMAGE,
    MAX_OXYGEN,
    OXYGEN_DRAIN_RATE,
    OXYGEN_PICKUP_AMOUNT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STATION_BLUE,
    WARNING_ORANGE,
    WHITE,
)
from entities.drone import Drone
from entities.particle import Particle
from entities.player import Player
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

        self.level = Level(LEVELS[level_index])
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, self.level.width, self.level.height)
        self.background = _build_background()

        spawn_x, spawn_y = self.level.player_spawn
        self.player = Player(spawn_x, spawn_y)
        self.drones = [Drone(x, y) for x, y in self.level.drone_spawns]
        self.oxygen = MAX_OXYGEN
        self.gravity_charges = gravity_charges
        self.particles = []

        music.play_gameplay()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
            self.next_state = PauseState(self.game, self)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            if self.gravity_charges > 0:
                self.gravity_charges -= 1
                self.player.flip_gravity()
                sound.play_flip()

    def update(self, dt):
        for entity in self.updatable:
            if isinstance(entity, Player):
                entity.update(dt, self.level.solid_tiles)
            else:
                entity.update(dt, self.level.solid_tiles, self.player)

        self.camera.update(self.player.position)
        self._check_hazards()
        self._check_pickups()
        self._update_particles(dt)

        self.oxygen = max(0.0, self.oxygen - OXYGEN_DRAIN_RATE * dt)
        if self.oxygen <= 0:
            self.next_state = GameOverState(self.game, won=False)
            return

        if self.level.exit_rect and self.player.rect.colliderect(self.level.exit_rect):
            sound.play_success()
            if self.level_index + 1 < len(LEVELS):
                self.next_state = PlayState(
                    self.game,
                    level_index=self.level_index + 1,
                    gravity_charges=self.gravity_charges,
                )
            else:
                self.next_state = GameOverState(self.game, won=True)

    def _check_hazards(self):
        for drone in self.drones:
            if self.player.rect.colliderect(drone.rect):
                if self.player.take_hit(drone.rect.centerx):
                    self.oxygen = max(0.0, self.oxygen - HAZARD_DAMAGE)

        for hazard in self.level.hazard_tiles:
            if self.player.rect.colliderect(hazard.rect):
                if self.player.take_hit(hazard.rect.centerx):
                    self.oxygen = max(0.0, self.oxygen - HAZARD_DAMAGE)

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

        for drone in self.drones:
            if random.random() < DRONE_SPARK_SPAWN_CHANCE:
                vel = pygame.Vector2(random.uniform(-30, 30), random.uniform(-30, 30))
                self.particles.append(
                    Particle(drone.rect.centerx, drone.rect.centery, vel, WARNING_ORANGE, lifetime=0.3, radius=2)
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
        hud.draw_oxygen_bar(screen, self.oxygen, MAX_OXYGEN)
        hud.draw_gravity_charges(screen, self.gravity_charges)
        if self.level.exit_rect:
            hud.draw_exit_indicator(screen, self.level.exit_rect, self.camera.offset)
