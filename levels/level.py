import pygame

from constants import TILE_SIZE
from entities.sprite_loader import load_image
from levels.tile import Tile

GROUND_TILE_IMAGE = "Ground/Planet/planetMid.png"
HAZARD_TILE_IMAGE = "Tiles/spikes.png"


class Level:
    """Parses a grid of characters (see levels/data/level_01.py for the
    legend) into tiles and spawn points.

    Only '#' (solid), 'P' (player spawn), and 'E' (exit) are consumed by
    gameplay yet. '^' (hazard), 'D' (drone spawn), 'F' (gravity-flip zone)
    and 'O' (oxygen pickup) are recognized and captured now so later
    milestones (4/5/6) can consume them without touching this parser again.
    """

    def __init__(self, grid, tile_size=TILE_SIZE):
        self.tile_size = tile_size
        self.tiles = []
        self.player_spawn = (0, 0)
        self.exit_rect = None
        self.drone_spawns = []
        self.flip_zone_positions = []
        self.oxygen_pickup_positions = []

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
                elif char == "F":
                    self.flip_zone_positions.append((x, y))
                elif char == "O":
                    self.oxygen_pickup_positions.append((x, y))

    @property
    def solid_tiles(self):
        return [tile for tile in self.tiles if tile.solid]

    @property
    def hazard_tiles(self):
        return [tile for tile in self.tiles if tile.hazard]
