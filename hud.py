import pygame

from constants import WHITE

BAR_WIDTH = 220
BAR_HEIGHT = 22
BAR_MARGIN = 16
BACKGROUND_COLOR = (30, 30, 40)
FULL_COLOR = (230, 130, 40)
CRITICAL_COLOR = (200, 40, 40)


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
