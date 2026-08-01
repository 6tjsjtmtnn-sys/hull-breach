import pygame

from constants import SWEEP_DRONE_SPEED
from entities.entity import Entity
from entities.sprite_loader import load_image

ANIM_FRAME_DURATION = 0.12
FRAMES = ["Enemies/fly.png", "Enemies/fly_move.png"]


class SweepDrone(Entity):
    """A flying drone that sweeps in a straight line across the screen
    during the boss fight, from one edge to the other, then despawns —
    an extra, unpredictable danger on top of the boss itself. Not part
    of a level's static spawn list (spawned/removed by PlayState over
    time). Ignores gravity, collision, and the player's position
    entirely; it's not hunting, just flying through."""

    def __init__(self, x, y, direction):
        super().__init__(x, y, load_image(FRAMES[0]))
        self.direction = direction
        self.velocity = pygame.Vector2(direction * SWEEP_DRONE_SPEED, 0)
        self._anim_timer = 0.0
        self._anim_frame = 0

    def update(self, dt, solid_tiles, player):
        self.rect.x += round(self.velocity.x * dt)
        self.position.update(self.rect.topleft)
        self._anim_timer += dt
        if self._anim_timer >= ANIM_FRAME_DURATION:
            self._anim_timer = 0.0
            self._anim_frame = (self._anim_frame + 1) % len(FRAMES)
        self.image = load_image(FRAMES[self._anim_frame])
