import pygame

from constants import (
    FLYING_DRONE_FIRE_COOLDOWN,
    FLYING_DRONE_FIRE_RANGE,
    FLYING_DRONE_PATROL_RANGE,
    FLYING_DRONE_SPEED,
)
from entities.entity import Entity
from entities.projectile import Projectile
from entities.sprite_loader import load_image

ANIM_FRAME_DURATION = 0.12
FRAMES = ["Enemies/fly.png", "Enemies/fly_move.png"]


class FlyingDrone(Entity):
    """A sentry that flies a fixed back-and-forth patrol near the ceiling.
    Ignores gravity entirely — it just oscillates horizontally around its
    spawn point, no ground/ledge collision needed. Also takes potshots at
    the player with a straight-line projectile when in range."""

    def __init__(self, x, y):
        super().__init__(x, y, load_image(FRAMES[0]))
        self.origin_x = x
        self.direction = 1
        self._anim_timer = 0.0
        self._anim_frame = 0
        # starts on cooldown so it doesn't fire the instant a level loads
        self._fire_cooldown = FLYING_DRONE_FIRE_COOLDOWN

    def update(self, dt, solid_tiles, player):
        self._fire_cooldown = max(0.0, self._fire_cooldown - dt)

        self.velocity.x = self.direction * FLYING_DRONE_SPEED
        self.rect.x += round(self.velocity.x * dt)

        if self.rect.x <= self.origin_x - FLYING_DRONE_PATROL_RANGE:
            self.direction = 1
        elif self.rect.x >= self.origin_x + FLYING_DRONE_PATROL_RANGE:
            self.direction = -1

        self.position.update(self.rect.topleft)
        self._update_animation(dt)

    def try_fire(self, player):
        """Returns a new Projectile aimed at the player if off cooldown
        and in range, otherwise None."""
        if self._fire_cooldown > 0:
            return None
        if self.position.distance_to(player.position) > FLYING_DRONE_FIRE_RANGE:
            return None

        self._fire_cooldown = FLYING_DRONE_FIRE_COOLDOWN
        aim = player.position - self.position
        direction = aim.normalize() if aim.length_squared() > 0 else pygame.Vector2(1, 0)
        return Projectile(self.rect.centerx, self.rect.centery, direction)

    def _update_animation(self, dt):
        self._anim_timer += dt
        if self._anim_timer >= ANIM_FRAME_DURATION:
            self._anim_timer = 0.0
            self._anim_frame = (self._anim_frame + 1) % len(FRAMES)
        self.image = load_image(FRAMES[self._anim_frame])
