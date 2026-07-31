import pygame

from constants import GRAVITY, JUMP_IMPULSE, MAX_FALL_SPEED, MOVE_SPEED
from entities.entity import Entity
from entities.sprite_loader import load_image
from levels.collision import check_grounded, resolve_axis_collision

WALK_FRAME_DURATION = 0.12

FRAMES = {
    "stand": "Players/128x256/Blue/alienBlue_stand.png",
    "jump": "Players/128x256/Blue/alienBlue_jump.png",
    "walk": [
        "Players/128x256/Blue/alienBlue_walk1.png",
        "Players/128x256/Blue/alienBlue_walk2.png",
    ],
}


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, load_image(FRAMES["stand"]))
        self.gravity_dir = 1
        self.on_ground = False
        self.facing_right = True
        self._walk_timer = 0.0
        self._walk_frame = 0

    def update(self, dt, solid_tiles):
        self._handle_input()

        self.velocity.y += GRAVITY * self.gravity_dir * dt
        if self.gravity_dir > 0:
            self.velocity.y = min(self.velocity.y, MAX_FALL_SPEED)
        else:
            self.velocity.y = max(self.velocity.y, -MAX_FALL_SPEED)

        self.rect.x += round(self.velocity.x * dt)
        self.rect, self.velocity, _, _ = resolve_axis_collision(
            self.rect, self.velocity, solid_tiles, "x"
        )

        self.rect.y += round(self.velocity.y * dt)
        self.rect, self.velocity, _, _ = resolve_axis_collision(
            self.rect, self.velocity, solid_tiles, "y"
        )

        self.on_ground = check_grounded(self.rect, solid_tiles, self.gravity_dir)
        if self.on_ground and self.gravity_dir * self.velocity.y >= 0:
            self.velocity.y = 0

        self.position.update(self.rect.topleft)
        self._update_animation(dt)

    def _handle_input(self):
        keys = pygame.key.get_pressed()
        direction = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction += 1
        self.velocity.x = direction * MOVE_SPEED
        if direction != 0:
            self.facing_right = direction > 0

        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]
        if jump_pressed and self.on_ground:
            self.velocity.y = -JUMP_IMPULSE * self.gravity_dir

    def _update_animation(self, dt):
        if not self.on_ground:
            frame = load_image(FRAMES["jump"])
        elif self.velocity.x != 0:
            self._walk_timer += dt
            if self._walk_timer >= WALK_FRAME_DURATION:
                self._walk_timer = 0.0
                self._walk_frame = (self._walk_frame + 1) % len(FRAMES["walk"])
            frame = load_image(FRAMES["walk"][self._walk_frame])
        else:
            frame = load_image(FRAMES["stand"])

        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        self.image = frame
