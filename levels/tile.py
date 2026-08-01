import pygame

from constants import WARNING_ORANGE

_font = None


def _get_font():
    global _font
    if _font is None:
        _font = pygame.font.SysFont(None, 20)
    return _font


class Tile:
    def __init__(
        self,
        x,
        y,
        image,
        solid=True,
        hazard=False,
        oxygen_pickup=False,
        gravity_pickup=False,
        exit_marker=False,
        label=None,
    ):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
        self.solid = solid
        self.hazard = hazard
        self.oxygen_pickup = oxygen_pickup
        self.gravity_pickup = gravity_pickup
        self.exit_marker = exit_marker
        self.label = label

    def draw(self, screen, camera_offset):
        pos = self.rect.topleft - camera_offset
        screen.blit(self.image, pos)
        if self.label:
            text = _get_font().render(self.label, True, WARNING_ORANGE)
            text_pos = (pos[0] + self.rect.width // 2 - text.get_width() // 2, pos[1] - text.get_height() - 2)
            screen.blit(text, text_pos)
