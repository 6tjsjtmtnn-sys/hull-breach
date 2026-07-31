import pygame

from constants import BLACK, SCREEN_HEIGHT, SCREEN_WIDTH
from entities.drone import Drone
from entities.player import Player
from levels.camera import Camera
from levels.data.level_01 import LEVEL
from levels.level import Level
from states.base_state import State


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

        # Placeholder until the real win state lands in milestone 6/8.
        if self.level.exit_rect and self.player.rect.colliderect(self.level.exit_rect):
            print("Level complete!")

    def _check_hazards(self):
        for drone in self.drones:
            if self.player.rect.colliderect(drone.rect):
                self.player.take_hit(drone.rect.centerx)

        for hazard in self.level.hazard_tiles:
            if self.player.rect.colliderect(hazard.rect):
                self.player.take_hit(hazard.rect.centerx)

    def draw(self, screen):
        screen.fill(BLACK)
        for tile in self.level.tiles:
            tile.draw(screen, self.camera.offset)
        for entity in self.drawable:
            entity.draw(screen, self.camera.offset)
