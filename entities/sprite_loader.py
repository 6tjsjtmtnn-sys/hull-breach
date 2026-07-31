from pathlib import Path

import pygame

from constants import TILE_SIZE

SPRITES_DIR = Path(__file__).resolve().parent.parent / "assets" / "sprites" / "PNG"
SOURCE_TILE_PX = 128
SCALE = TILE_SIZE / SOURCE_TILE_PX

_cache = {}


def load_image(relative_path):
    if relative_path not in _cache:
        image = pygame.image.load(SPRITES_DIR / relative_path).convert_alpha()
        width = round(image.get_width() * SCALE)
        height = round(image.get_height() * SCALE)
        _cache[relative_path] = pygame.transform.smoothscale(image, (width, height))
    return _cache[relative_path]


def load_frames(relative_paths):
    return [load_image(path) for path in relative_paths]
