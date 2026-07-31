from levels.level import Level


def test_parses_tiles_and_spawn_points():
    grid = [
        "..E.",
        "....",
        ".D..",
        "P#^F",
    ]
    level = Level(grid, tile_size=32)

    assert level.player_spawn == (0, 3 * 32)
    assert level.exit_rect.topleft == (2 * 32, 0)
    assert level.drone_spawns == [(1 * 32, 2 * 32)]

    solid_positions = {tile.rect.topleft for tile in level.solid_tiles}
    assert (1 * 32, 3 * 32) in solid_positions

    hazard_positions = {tile.rect.topleft for tile in level.hazard_tiles}
    assert (2 * 32, 3 * 32) in hazard_positions

    flip_positions = {tile.rect.topleft for tile in level.flip_zone_tiles}
    assert (3 * 32, 3 * 32) in flip_positions

    assert level.width == 4 * 32
    assert level.height == 4 * 32


def test_oxygen_pickup_parsed_and_removable():
    grid = ["O"]
    level = Level(grid, tile_size=32)

    pickups = level.oxygen_pickup_tiles
    assert len(pickups) == 1

    level.tiles.remove(pickups[0])
    assert level.oxygen_pickup_tiles == []
