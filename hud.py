import pygame

from constants import GRAVITY_GREEN, HUD_CYAN, SCREEN_WIDTH, WHITE
from entities.sprite_loader import load_image

HEART_SIZE = 24
HEART_MARGIN = 16
HEART_SPACING = 4

BOSS_BAR_WIDTH = 320
BOSS_BAR_HEIGHT = 18
BOSS_BAR_Y = 16
BOSS_BAR_COLOR = (200, 40, 40)

BAR_WIDTH = 220
BAR_HEIGHT = 22
BAR_MARGIN = 16
BACKGROUND_COLOR = (30, 30, 40)
FULL_COLOR = (230, 130, 40)
CRITICAL_COLOR = (200, 40, 40)

GRAVITY_ICON_SIZE = 16
GRAVITY_HUD_Y = BAR_MARGIN + BAR_HEIGHT + 10

EXIT_ARROW_COLOR = (240, 200, 60)
EXIT_ARROW_Y = 90
EXIT_ARROW_MARGIN = 24
EXIT_ARROW_SIZE = 14

LEVEL_INDICATOR_MARGIN = 16

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

    label = _get_font().render("O2", True, WHITE)
    screen.blit(label, (x + 6, y + BAR_HEIGHT // 2 - label.get_height() // 2))


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

    pygame.draw.polygon(screen, GRAVITY_GREEN, diamond)
    pygame.draw.polygon(screen, WHITE, diamond, width=1)

    text = _get_font().render(f"x {charges}  [G]", True, WHITE)
    screen.blit(text, (x + size + 8, y - 3))


def draw_exit_indicator(screen, exit_rect, camera_offset, label="EXIT"):
    """A screen-edge arrow pointing toward the exit whenever it has
    scrolled out of view, so players always know which way to head."""
    exit_screen_x = exit_rect.centerx - camera_offset.x

    if exit_screen_x < 0:
        _draw_exit_arrow(screen, EXIT_ARROW_MARGIN, pointing_left=True, label=label)
    elif exit_screen_x > SCREEN_WIDTH:
        _draw_exit_arrow(screen, SCREEN_WIDTH - EXIT_ARROW_MARGIN, pointing_left=False, label=label)


def _draw_exit_arrow(screen, x, pointing_left, label):
    y = EXIT_ARROW_Y
    size = EXIT_ARROW_SIZE
    if pointing_left:
        points = [(x, y), (x + size, y - size), (x + size, y + size)]
    else:
        points = [(x, y), (x - size, y - size), (x - size, y + size)]

    pygame.draw.polygon(screen, EXIT_ARROW_COLOR, points)

    text = _get_font().render(label, True, EXIT_ARROW_COLOR)
    screen.blit(text, (x - text.get_width() // 2, y + size + 4))


def draw_player_hearts(screen, hearts, max_hearts):
    full = load_image("HUD/hudHeart_full.png")
    empty = load_image("HUD/hudHeart_empty.png")

    for i in range(max_hearts):
        image = full if i < hearts else empty
        image = pygame.transform.smoothscale(image, (HEART_SIZE, HEART_SIZE))
        x = HEART_MARGIN + i * (HEART_SIZE + HEART_SPACING)
        screen.blit(image, (x, HEART_MARGIN))


def draw_level_indicator(screen, level_index, total_levels, label=None):
    text_str = label if label is not None else f"LEVEL {level_index + 1} / {total_levels}"
    text = _get_font().render(text_str, True, HUD_CYAN)
    x = SCREEN_WIDTH - text.get_width() - LEVEL_INDICATOR_MARGIN
    y = LEVEL_INDICATOR_MARGIN

    padding = 6
    backing = pygame.Rect(
        x - padding, y - padding // 2, text.get_width() + padding * 2, text.get_height() + padding
    )
    pygame.draw.rect(screen, BACKGROUND_COLOR, backing)
    screen.blit(text, (x, y))


def draw_boss_health_bar(screen, hp, max_hp):
    ratio = max(0.0, min(1.0, hp / max_hp))
    x = (SCREEN_WIDTH - BOSS_BAR_WIDTH) // 2
    y = BOSS_BAR_Y

    pygame.draw.rect(screen, BACKGROUND_COLOR, (x, y, BOSS_BAR_WIDTH, BOSS_BAR_HEIGHT))
    pygame.draw.rect(screen, BOSS_BAR_COLOR, (x, y, int(BOSS_BAR_WIDTH * ratio), BOSS_BAR_HEIGHT))
    pygame.draw.rect(screen, WHITE, (x, y, BOSS_BAR_WIDTH, BOSS_BAR_HEIGHT), width=2)

    text = _get_font().render("REACTOR SENTINEL", True, WHITE)
    screen.blit(text, (x + BOSS_BAR_WIDTH // 2 - text.get_width() // 2, y + BOSS_BAR_HEIGHT + 4))
