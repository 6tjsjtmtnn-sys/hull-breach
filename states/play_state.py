import pygame

from constants import BLACK, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from entities.player import Player
from entities.sprite_loader import load_image
from levels.tile import Tile
from states.base_state import State

GROUND_ROW = SCREEN_HEIGHT // TILE_SIZE - 2


def _build_flat_test_level():
    """Milestone 2 placeholder: a hardcoded flat level with two floating
    platforms, just to prove out physics/collision before the real
    data-driven level loader lands in milestone 3."""
    tile_image = load_image("Ground/Planet/planetMid.png")
    tiles = []

    columns = SCREEN_WIDTH // TILE_SIZE + 4
    for col in range(columns):
        tiles.append(Tile(col * TILE_SIZE, GROUND_ROW * TILE_SIZE, tile_image))

    for col in range(6, 9):
        tiles.append(Tile(col * TILE_SIZE, (GROUND_ROW - 3) * TILE_SIZE, tile_image))
    for col in range(14, 18):
        tiles.append(Tile(col * TILE_SIZE, (GROUND_ROW - 5) * TILE_SIZE, tile_image))

    return tiles


class PlayState(State):
    def __init__(self, game):
        super().__init__(game)
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        Player.containers = (self.updatable, self.drawable)

        self.tiles = _build_flat_test_level()
        self.player = Player(TILE_SIZE * 2, TILE_SIZE * 2)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False

    def update(self, dt):
        for entity in self.updatable:
            entity.update(dt, self.tiles)

    def draw(self, screen):
        screen.fill(BLACK)
        camera_offset = pygame.Vector2(0, 0)
        for tile in self.tiles:
            tile.draw(screen, camera_offset)
        for entity in self.drawable:
            entity.draw(screen, camera_offset)
