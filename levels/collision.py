import pygame


def resolve_axis_collision(rect, velocity, solid_tiles, axis):
    """Clamp `rect` out of any overlapping solid tile along a single axis.

    Must be called once for the x-axis move and once for the y-axis move
    (never a combined diagonal move) to avoid tunneling through corners.

    Returns (rect, velocity, hit_positive, hit_negative), where "positive"
    means a tile was hit while moving in the increasing x/y direction.
    """
    hit_positive = False
    hit_negative = False

    for tile in solid_tiles:
        if not rect.colliderect(tile.rect):
            continue

        if axis == "x":
            if velocity.x > 0:
                rect.right = tile.rect.left
                hit_positive = True
            elif velocity.x < 0:
                rect.left = tile.rect.right
                hit_negative = True
            velocity.x = 0
        else:
            if velocity.y > 0:
                rect.bottom = tile.rect.top
                hit_positive = True
            elif velocity.y < 0:
                rect.top = tile.rect.bottom
                hit_negative = True
            velocity.y = 0

    return rect, velocity, hit_positive, hit_negative


def check_grounded(rect, solid_tiles, gravity_dir, probe_distance=1):
    """Is there solid ground immediately adjacent in the direction gravity
    pulls? Checked via a small probe rect rather than reusing this frame's
    movement-collision result, since a resting rect sitting exactly flush
    against a tile edge doesn't register as an overlap every frame (pixel
    rounding on tiny residual gravity velocity), which otherwise makes
    on_ground flicker false intermittently while standing still.
    """
    probe = rect.copy()
    probe.y += probe_distance if gravity_dir > 0 else -probe_distance
    return any(
        probe.colliderect(tile.rect) for tile in solid_tiles if tile.solid
    )


def is_ledge_ahead(rect, solid_tiles, direction, gravity_dir, tile_size):
    """No ground just past the leading edge in `direction`? Used by patrol
    AI so it turns around at a platform's edge instead of walking off."""
    probe_x = rect.right if direction > 0 else rect.left - tile_size
    probe_y = rect.bottom if gravity_dir > 0 else rect.top - 4
    probe = pygame.Rect(probe_x, probe_y, tile_size, 4)
    return not any(
        probe.colliderect(tile.rect) for tile in solid_tiles if tile.solid
    )
