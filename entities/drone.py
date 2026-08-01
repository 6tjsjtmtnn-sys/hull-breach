from constants import (
    CHASE_DEADZONE,
    DRONE_CHASE_SPEED,
    DRONE_DETECT_RANGE,
    DRONE_LOSE_RANGE,
    DRONE_PATROL_SPEED,
    GRAVITY,
    MAX_FALL_SPEED,
    TILE_SIZE,
)
from entities.entity import Entity
from entities.sprite_loader import load_image
from levels.collision import check_grounded, is_ledge_ahead, resolve_axis_collision

ANIM_FRAME_DURATION = 0.08
FRAMES = ["Enemies/saw.png", "Enemies/saw_move.png"]


class Drone(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, load_image(FRAMES[0]))
        self.direction = 1
        self.state = "patrol"
        self._anim_timer = 0.0
        self._anim_frame = 0

    def update(self, dt, solid_tiles, player):
        distance = self.position.distance_to(player.position)
        if self.state == "patrol" and distance < DRONE_DETECT_RANGE:
            self.state = "chase"
        elif self.state == "chase" and distance > DRONE_LOSE_RANGE:
            self.state = "patrol"

        held_still = False
        if self.state == "chase":
            dx = player.position.x - self.position.x
            if abs(dx) > CHASE_DEADZONE:
                self.direction = 1 if dx > 0 else -1
                self.velocity.x = self.direction * DRONE_CHASE_SPEED
            else:
                self.velocity.x = 0
                held_still = True
        else:
            self.velocity.x = self.direction * DRONE_PATROL_SPEED

        self.velocity.y = min(self.velocity.y + GRAVITY * dt, MAX_FALL_SPEED)

        self.rect.x += round(self.velocity.x * dt)
        self.rect, self.velocity, _, _ = resolve_axis_collision(
            self.rect, self.velocity, solid_tiles, "x"
        )

        self.rect.y += round(self.velocity.y * dt)
        self.rect, self.velocity, _, _ = resolve_axis_collision(
            self.rect, self.velocity, solid_tiles, "y"
        )

        on_ground = check_grounded(self.rect, solid_tiles, 1)
        if on_ground and self.velocity.y >= 0:
            self.velocity.y = 0

        if not held_still:
            hit_wall = self.velocity.x == 0
            ledge_ahead = on_ground and is_ledge_ahead(
                self.rect, solid_tiles, self.direction, 1, TILE_SIZE
            )
            if hit_wall or ledge_ahead:
                self.direction *= -1

        self.position.update(self.rect.topleft)
        self._update_animation(dt)

    def _update_animation(self, dt):
        self._anim_timer += dt
        if self._anim_timer >= ANIM_FRAME_DURATION:
            self._anim_timer = 0.0
            self._anim_frame = (self._anim_frame + 1) % len(FRAMES)
        self.image = load_image(FRAMES[self._anim_frame])
