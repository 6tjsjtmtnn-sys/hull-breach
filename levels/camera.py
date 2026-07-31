import pygame


class Camera:
    """Follows a target position, clamped so it never scrolls past the
    level edges. Direct-follow (no lerp) is enough for this scope."""

    def __init__(self, screen_width, screen_height, level_width, level_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level_width = level_width
        self.level_height = level_height
        self.offset = pygame.Vector2(0, 0)

    def update(self, target_position):
        max_offset_x = max(0, self.level_width - self.screen_width)
        max_offset_y = max(0, self.level_height - self.screen_height)

        target_x = target_position.x - self.screen_width / 2
        target_y = target_position.y - self.screen_height / 2

        self.offset.x = max(0, min(target_x, max_offset_x))
        self.offset.y = max(0, min(target_y, max_offset_y))
