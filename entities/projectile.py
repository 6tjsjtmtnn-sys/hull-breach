import pygame

from constants import PROJECTILE_LIFETIME, PROJECTILE_SPEED
from entities.sprite_loader import load_image

IMAGE_PATH = "Tiles/bomb.png"


class Projectile:
    """A simple straight-line shot fired by a FlyingDrone. Not a full
    Entity/Sprite (no gravity, no tile collision) — managed directly by
    PlayState like the particle system, just with a rect for hit
    detection against the player."""

    def __init__(self, x, y, direction):
        self.image = load_image(IMAGE_PATH)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.Vector2(direction) * PROJECTILE_SPEED
        self.age = 0.0

    @property
    def alive(self):
        return self.age < PROJECTILE_LIFETIME

    def update(self, dt):
        self.age += dt
        self.rect.x += round(self.velocity.x * dt)
        self.rect.y += round(self.velocity.y * dt)

    def draw(self, screen, camera_offset):
        screen.blit(self.image, self.rect.topleft - camera_offset)
