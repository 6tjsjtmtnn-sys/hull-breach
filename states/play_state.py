import pygame

import hud
from constants import BLACK, HAZARD_DAMAGE, MAX_OXYGEN, OXYGEN_DRAIN_RATE, OXYGEN_PICKUP_AMOUNT, SCREEN_HEIGHT, SCREEN_WIDTH
from entities.drone import Drone
from entities.player import Player
from levels.camera import Camera
from levels.data.level_01 import LEVEL
from levels.level import Level
from states.base_state import State
from states.game_over_state import GameOverState


class PlayState(State):
    def __init__(self, game):
        super().__init__(game)
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        Player.containers = (self.updatable, self.drawable)
        Drone.containers = (self.updatable, self.drawable)

        self.level = Level(LEVEL)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, self.level.width, self.level.height)

        spawn_x, spawn_y = self.level.player_spawn
        self.player = Player(spawn_x, spawn_y)
        self.drones = [Drone(x, y) for x, y in self.level.drone_spawns]
        self._touching_flip_zone = False
        self.oxygen = MAX_OXYGEN

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False

    def update(self, dt):
        for entity in self.updatable:
            if isinstance(entity, Player):
                entity.update(dt, self.level.solid_tiles)
            else:
                entity.update(dt, self.level.solid_tiles, self.player)

        self.camera.update(self.player.position)
        self._check_hazards()
        self._check_flip_zones()
        self._check_pickups()

        self.oxygen = max(0.0, self.oxygen - OXYGEN_DRAIN_RATE * dt)
        if self.oxygen <= 0:
            self.next_state = GameOverState(self.game, won=False)
            return

        if self.level.exit_rect and self.player.rect.colliderect(self.level.exit_rect):
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

    def _check_flip_zones(self):
        touching = any(
            self.player.rect.colliderect(zone.rect) for zone in self.level.flip_zone_tiles
        )
        if touching and not self._touching_flip_zone:
            self.player.flip_gravity()
        self._touching_flip_zone = touching

    def _check_pickups(self):
        for pickup in self.level.oxygen_pickup_tiles:
            if self.player.rect.colliderect(pickup.rect):
                self.oxygen = min(MAX_OXYGEN, self.oxygen + OXYGEN_PICKUP_AMOUNT)
                self.level.tiles.remove(pickup)

    def draw(self, screen):
        screen.fill(BLACK)
        for tile in self.level.tiles:
            tile.draw(screen, self.camera.offset)
        for entity in self.drawable:
            entity.draw(screen, self.camera.offset)
        hud.draw_oxygen_bar(screen, self.oxygen, MAX_OXYGEN)
