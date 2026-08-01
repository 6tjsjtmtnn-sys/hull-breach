import pygame

from constants import SWEEP_DRONE_FIRE_COOLDOWN, SWEEP_DRONE_FIRE_RANGE, SWEEP_DRONE_SPEED
from entities.entity import Entity
from entities.projectile import Projectile
from entities.sprite_loader import load_image

ANIM_FRAME_DURATION = 0.12
FRAMES = ["Enemies/fly.png", "Enemies/fly_move.png"]


class SweepDrone(Entity):
    """A flying drone that sweeps in a straight line across the screen
    during the boss fight, from one edge to the other, then despawns —
    an extra, unpredictable danger on top of the boss itself. Not part
    of a level's static spawn list (spawned/removed by PlayState over
    time). Ignores gravity/collision and doesn't hunt the player — it
    just flies straight through, taking potshots at the player when in
    range along the way."""

    def __init__(self, x, y, direction):
        super().__init__(x, y, load_image(FRAMES[0]))
        self.direction = direction
        self.velocity = pygame.Vector2(direction * SWEEP_DRONE_SPEED, 0)
        self._anim_timer = 0.0
        self._anim_frame = 0
        # starts on cooldown so it doesn't fire the instant it spawns
        self._fire_cooldown = SWEEP_DRONE_FIRE_COOLDOWN

    def update(self, dt, solid_tiles, player):
        self._fire_cooldown = max(0.0, self._fire_cooldown - dt)
        self.rect.x += round(self.velocity.x * dt)
        self.position.update(self.rect.topleft)
        self._anim_timer += dt
        if self._anim_timer >= ANIM_FRAME_DURATION:
            self._anim_timer = 0.0
            self._anim_frame = (self._anim_frame + 1) % len(FRAMES)
        self.image = load_image(FRAMES[self._anim_frame])

    def try_fire(self, player):
        """Returns a new Projectile aimed at the player if off cooldown
        and in range, otherwise None."""
        if self._fire_cooldown > 0:
            return None
        if self.position.distance_to(player.position) > SWEEP_DRONE_FIRE_RANGE:
            return None

        self._fire_cooldown = SWEEP_DRONE_FIRE_COOLDOWN
        aim = player.position - self.position
        direction = aim.normalize() if aim.length_squared() > 0 else pygame.Vector2(1, 0)
        return Projectile(self.rect.centerx, self.rect.centery, direction)
