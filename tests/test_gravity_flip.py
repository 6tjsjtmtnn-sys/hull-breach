import pygame

from entities.player import Player
from levels.collision import check_grounded
from levels.tile import Tile


def make_tile(col, row, size=32):
    image = pygame.Surface((size, size))
    return Tile(col * size, row * size, image, solid=True)


def test_flip_gravity_toggles_sign():
    Player.containers = (pygame.sprite.Group(),)
    player = Player(0, 0)

    assert player.gravity_dir == 1
    player.flip_gravity()
    assert player.gravity_dir == -1
    player.flip_gravity()
    assert player.gravity_dir == 1


def test_ground_check_flips_with_gravity_direction():
    tile_below = make_tile(0, 1)
    tile_above = make_tile(0, -1)
    rect = pygame.Rect(0, 0, 32, 32)

    assert check_grounded(rect, [tile_below], gravity_dir=1) is True
    assert check_grounded(rect, [tile_above], gravity_dir=1) is False

    assert check_grounded(rect, [tile_above], gravity_dir=-1) is True
    assert check_grounded(rect, [tile_below], gravity_dir=-1) is False
