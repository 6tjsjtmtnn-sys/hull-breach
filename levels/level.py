import pygame

from constants import TILE_SIZE
from entities.sprite_loader import load_image
from levels.tile import Tile

GROUND_TILE_IMAGE = "Ground/Planet/planetMid.png"
HAZARD_TILE_IMAGE = "Tiles/spikes.png"
OXYGEN_PICKUP_IMAGE = "Items/gemBlue.png"
GRAVITY_PICKUP_IMAGE = "Items/gemGreen.png"


class Level:
    """Parses a grid of characters (see levels/data/level_01.py for the
    legend) into tiles and spawn points."""

    def __init__(self, grid, tile_size=TILE_SIZE):
        self.tile_size = tile_size
        self.tiles = []
        self.player_spawn = (0, 0)
        self.exit_rect = None
        self.drone_spawns = []

        self.width = max(len(row) for row in grid) * tile_size
        self.height = len(grid) * tile_size

        self._parse(grid)

    def _parse(self, grid):
        for row_index, row in enumerate(grid):
            for col_index, char in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size

                if char == "#":
                    self.tiles.append(Tile(x, y, load_image(GROUND_TILE_IMAGE), solid=True))
                elif char == "^":
                    self.tiles.append(
                        Tile(x, y, load_image(HAZARD_TILE_IMAGE), solid=False, hazard=True)
                    )
                elif char == "P":
                    self.player_spawn = (x, y)
                elif char == "E":
                    self.exit_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                elif char == "D":
                    self.drone_spawns.append((x, y))
                elif char == "O":
                    self.tiles.append(
                        Tile(x, y, load_image(OXYGEN_PICKUP_IMAGE), solid=False, oxygen_pickup=True)
                    )
                elif char == "G":
                    self.tiles.append(
                        Tile(x, y, load_image(GRAVITY_PICKUP_IMAGE), solid=False, gravity_pickup=True)
                    )

    @property
    def solid_tiles(self):
        return [tile for tile in self.tiles if tile.solid]

    @property
    def hazard_tiles(self):
        return [tile for tile in self.tiles if tile.hazard]

    @property
    def oxygen_pickup_tiles(self):
        return [tile for tile in self.tiles if tile.oxygen_pickup]

    @property
    def gravity_pickup_tiles(self):
        return [tile for tile in self.tiles if tile.gravity_pickup]
