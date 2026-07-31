import pygame

from levels.collision import check_grounded, is_ledge_ahead, resolve_axis_collision
from levels.tile import Tile


def make_tile(col, row, size=32, solid=True, hazard=False):
    image = pygame.Surface((size, size))
    return Tile(col * size, row * size, image, solid=solid, hazard=hazard)


def test_resolve_axis_collision_lands_on_top_of_tile():
    tile = make_tile(0, 5)
    rect = pygame.Rect(0, 5 * 32 - 10, 32, 32)
    velocity = pygame.Vector2(0, 50)

    rect, velocity, hit_positive, hit_negative = resolve_axis_collision(rect, velocity, [tile], "y")

    assert rect.bottom == tile.rect.top
    assert velocity.y == 0
    assert hit_positive is True
    assert hit_negative is False


def test_resolve_axis_collision_blocks_wall_on_the_right():
    tile = make_tile(5, 0)
    rect = pygame.Rect(5 * 32 - 10, 0, 32, 32)
    velocity = pygame.Vector2(80, 0)

    rect, velocity, hit_positive, hit_negative = resolve_axis_collision(rect, velocity, [tile], "x")

    assert rect.right == tile.rect.left
    assert velocity.x == 0
    assert hit_positive is True


def test_resolve_axis_collision_no_overlap_leaves_rect_untouched():
    tile = make_tile(10, 10)
    rect = pygame.Rect(0, 0, 32, 32)
    velocity = pygame.Vector2(10, 10)

    new_rect, new_velocity, hit_positive, hit_negative = resolve_axis_collision(
        rect, velocity, [tile], "x"
    )

    assert new_rect.topleft == (0, 0)
    assert new_velocity.x == 10
    assert hit_positive is False and hit_negative is False


def test_check_grounded_normal_gravity():
    tile = make_tile(0, 1)
    rect = pygame.Rect(0, 0, 32, 32)
    assert check_grounded(rect, [tile], gravity_dir=1) is True
    assert check_grounded(rect, [], gravity_dir=1) is False


def test_check_grounded_flipped_gravity():
    tile = make_tile(0, -1)
    rect = pygame.Rect(0, 0, 32, 32)
    assert check_grounded(rect, [tile], gravity_dir=-1) is True
    assert check_grounded(rect, [], gravity_dir=-1) is False


def test_is_ledge_ahead_true_when_no_ground_past_edge():
    tile = make_tile(0, 1)
    rect = pygame.Rect(0, 0, 32, 32)
    assert is_ledge_ahead(rect, [tile], direction=1, gravity_dir=1, tile_size=32) is True


def test_is_ledge_ahead_false_when_platform_continues():
    tiles = [make_tile(0, 1), make_tile(1, 1)]
    rect = pygame.Rect(0, 0, 32, 32)
    assert is_ledge_ahead(rect, tiles, direction=1, gravity_dir=1, tile_size=32) is False
