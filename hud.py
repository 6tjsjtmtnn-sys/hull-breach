import pygame

from constants import GRAVITY_PURPLE, WHITE

BAR_WIDTH = 220
BAR_HEIGHT = 22
BAR_MARGIN = 16
BACKGROUND_COLOR = (30, 30, 40)
FULL_COLOR = (230, 130, 40)
CRITICAL_COLOR = (200, 40, 40)

GRAVITY_ICON_SIZE = 16
GRAVITY_HUD_Y = BAR_MARGIN + BAR_HEIGHT + 10

_font = None


def _get_font():
    global _font
    if _font is None:
        _font = pygame.font.SysFont(None, 24)
    return _font


def draw_oxygen_bar(screen, oxygen, max_oxygen):
    ratio = max(0.0, min(1.0, oxygen / max_oxygen))
    x, y = BAR_MARGIN, BAR_MARGIN

    pygame.draw.rect(screen, BACKGROUND_COLOR, (x, y, BAR_WIDTH, BAR_HEIGHT))
    pygame.draw.rect(screen, _color_for_ratio(ratio), (x, y, int(BAR_WIDTH * ratio), BAR_HEIGHT))
    pygame.draw.rect(screen, WHITE, (x, y, BAR_WIDTH, BAR_HEIGHT), width=2)


def _color_for_ratio(ratio):
    if ratio > 0.5:
        return FULL_COLOR
    t = 1 - (ratio / 0.5)
    return tuple(int(a + (b - a) * t) for a, b in zip(FULL_COLOR, CRITICAL_COLOR))


def draw_gravity_charges(screen, charges):
    x, y = BAR_MARGIN, GRAVITY_HUD_Y
    size = GRAVITY_ICON_SIZE
    cx = x + size // 2
    cy = y + size // 2
    diamond = [(cx, y), (x + size, cy), (cx, y + size), (x, cy)]

    pygame.draw.polygon(screen, GRAVITY_PURPLE, diamond)
    pygame.draw.polygon(screen, WHITE, diamond, width=1)

    text = _get_font().render(f"x {charges}  [G]", True, WHITE)
    screen.blit(text, (x + size + 8, y - 3))
