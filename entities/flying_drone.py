from constants import FLYING_DRONE_PATROL_RANGE, FLYING_DRONE_SPEED
from entities.entity import Entity
from entities.sprite_loader import load_image

ANIM_FRAME_DURATION = 0.12
FRAMES = ["Enemies/fly.png", "Enemies/fly_move.png"]


class FlyingDrone(Entity):
    """A sentry that flies a fixed back-and-forth patrol near the ceiling.
    Ignores gravity entirely — it just oscillates horizontally around its
    spawn point, no ground/ledge collision needed."""

    def __init__(self, x, y):
        super().__init__(x, y, load_image(FRAMES[0]))
        self.origin_x = x
        self.direction = 1
        self._anim_timer = 0.0
        self._anim_frame = 0

    def update(self, dt, solid_tiles, player):
        self.velocity.x = self.direction * FLYING_DRONE_SPEED
        self.rect.x += round(self.velocity.x * dt)

        if self.rect.x <= self.origin_x - FLYING_DRONE_PATROL_RANGE:
            self.direction = 1
        elif self.rect.x >= self.origin_x + FLYING_DRONE_PATROL_RANGE:
            self.direction = -1

        self.position.update(self.rect.topleft)
        self._update_animation(dt)

    def _update_animation(self, dt):
        self._anim_timer += dt
        if self._anim_timer >= ANIM_FRAME_DURATION:
            self._anim_timer = 0.0
            self._anim_frame = (self._anim_frame + 1) % len(FRAMES)
        self.image = load_image(FRAMES[self._anim_frame])
