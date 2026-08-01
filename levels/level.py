import pygame

from constants import TILE_SIZE
from entities.sprite_loader import load_image
from levels.tile import Tile

GROUND_TILE_IMAGE = "Ground/Planet/planetMid.png"
HAZARD_TILE_IMAGE = "Tiles/spikes.png"
OXYGEN_PICKUP_IMAGE = "Items/gemBlue.png"
GRAVITY_PICKUP_IMAGE = "Items/gemGreen.png"
EXIT_IMAGE = "Tiles/signExit.png"
BLANK_SIGN_IMAGE = "Tiles/sign.png"

_ceiling_hazard_image = None


def _load_ceiling_hazard_image():
    """The spike sprite points up (floor placement) — flip it once and
    cache it for ceiling spikes, which hang down instead."""
    global _ceiling_hazard_image
    if _ceiling_hazard_image is None:
        _ceiling_hazard_image = pygame.transform.flip(load_image(HAZARD_TILE_IMAGE), False, True)
    return _ceiling_hazard_image


class Level:
    """Parses a grid of characters (see levels/data/level_01.py for the
    legend) into tiles and spawn points. 'X' is the same as 'E' but
    labeled "BOSS FIGHT" instead of "EXIT" — used on the level right
    before a boss encounter."""

    def __init__(self, grid, tile_size=TILE_SIZE):
        self.tile_size = tile_size
        self.tiles = []
        self.player_spawn = (0, 0)
        self.exit_rect = None
        self.exit_label = "EXIT"
        self.drone_spawns = []
        self.flying_drone_spawns = []
        self.boss_spawn = None

        self.width = max(len(row) for row in grid) * tile_size
        self.height = len(grid) * tile_size

        self._parse(grid)

    def _exit_trigger_rect(self, x):
        """A full-height sensor column at the exit sign's x, not just its
        own 32px tile — a jump or bounce that carries a player over the
        single-tile-tall sign at speed could otherwise sail past it
        without ever overlapping its rect, stranding them against the
        level boundary with no way back (hit this in testing more than
        once)."""
        return pygame.Rect(x, 0, self.tile_size, self.height)

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
                elif char == "v":
                    self.tiles.append(
                        Tile(x, y, _load_ceiling_hazard_image(), solid=False, hazard=True)
                    )
                elif char == "P":
                    self.player_spawn = (x, y)
                elif char == "E":
                    exit_tile = Tile(x, y, load_image(EXIT_IMAGE), solid=False, exit_marker=True)
                    self.tiles.append(exit_tile)
                    self.exit_rect = self._exit_trigger_rect(x)
                elif char == "X":
                    exit_tile = Tile(
                        x, y, load_image(BLANK_SIGN_IMAGE), solid=False, exit_marker=True, label="BOSS FIGHT"
                    )
                    self.tiles.append(exit_tile)
                    self.exit_rect = self._exit_trigger_rect(x)
                    self.exit_label = "BOSS FIGHT"
                elif char == "D":
                    self.drone_spawns.append((x, y))
                elif char == "F":
                    self.flying_drone_spawns.append((x, y))
                elif char == "B":
                    self.boss_spawn = (x, y)
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
