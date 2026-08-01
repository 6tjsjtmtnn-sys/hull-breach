import pygame

from constants import HEART_PICKUP_LIFETIME, HEART_PICKUP_SIZE
from entities.sprite_loader import load_image

IMAGE_PATH = "HUD/hudHeart_full.png"
WARNING_THRESHOLD = 2.0
BLINK_PERIOD = 0.15


class HeartPickup:
    """A bonus heart that appears at a random spot during the boss fight —
    the one place hearts can't otherwise be replenished — and vanishes
    again if the player doesn't reach it in time. Not a full Entity/Sprite
    (no gravity, no tile collision), same lightweight pattern as
    Projectile: managed directly by PlayState, just position + rect."""

    def __init__(self, x, y):
        image = load_image(IMAGE_PATH)
        self.image = pygame.transform.smoothscale(image, (HEART_PICKUP_SIZE, HEART_PICKUP_SIZE))
        self.rect = self.image.get_rect(center=(x, y))
        self.age = 0.0

    @property
    def alive(self):
        return self.age < HEART_PICKUP_LIFETIME

    @property
    def time_remaining(self):
        return max(0.0, HEART_PICKUP_LIFETIME - self.age)

    def update(self, dt):
        self.age += dt

    def draw(self, screen, camera_offset):
        if self.time_remaining < WARNING_THRESHOLD:
            if int(self.age / BLINK_PERIOD) % 2 == 0:
                return
        screen.blit(self.image, self.rect.topleft - camera_offset)
