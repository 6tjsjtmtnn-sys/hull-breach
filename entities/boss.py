import pygame

from constants import (
    BOSS_CHASE_SPEED,
    BOSS_DETECT_RANGE,
    BOSS_FIRE_COOLDOWN,
    BOSS_FIRE_RANGE,
    BOSS_HP,
    BOSS_LOSE_RANGE,
    BOSS_PATROL_SPEED,
    BOSS_SCALE,
    BOSS_STUN_DURATION,
    CHASE_DEADZONE,
    GRAVITY,
    MAX_FALL_SPEED,
    TILE_SIZE,
)
from entities.entity import Entity
from entities.projectile import Projectile
from entities.sprite_loader import load_image_scaled
from levels.collision import check_grounded, is_ledge_ahead, resolve_axis_collision

FRAMES = ["Enemies/saw.png", "Enemies/saw_move.png"]
ANIM_FRAME_DURATION = 0.07


class Boss(Entity):
    """The station's reactor sentinel: a scaled-up, faster, tougher saw
    drone. Same patrol/chase/ledge-awareness as a regular Drone, but takes
    multiple stomps to defeat instead of one."""

    def __init__(self, x, y):
        super().__init__(x, y, load_image_scaled(FRAMES[0], BOSS_SCALE))
        self.hp = BOSS_HP
        self.direction = 1
        self.state = "patrol"
        self._anim_timer = 0.0
        self._anim_frame = 0
        self._stun_timer = 0.0
        self._fire_cooldown = BOSS_FIRE_COOLDOWN

    def try_fire(self, player):
        """Returns a new Projectile aimed at the player if off cooldown
        and in range, otherwise None."""
        if self._stun_timer > 0:
            return None
        if self._fire_cooldown > 0:
            return None
        if self.position.distance_to(player.position) > BOSS_FIRE_RANGE:
            return None

        self._fire_cooldown = BOSS_FIRE_COOLDOWN
        aim = player.position - self.position
        direction = aim.normalize() if aim.length_squared() > 0 else pygame.Vector2(1, 0)
        return Projectile(self.rect.centerx, self.rect.centery, direction)

    def take_hit(self):
        self.hp -= 1
        self._stun_timer = BOSS_STUN_DURATION
        return self.hp <= 0

    def update(self, dt, solid_tiles, player):
        self._fire_cooldown = max(0.0, self._fire_cooldown - dt)
        self._stun_timer = max(0.0, self._stun_timer - dt)

        distance = self.position.distance_to(player.position)
        if self.state == "patrol" and distance < BOSS_DETECT_RANGE:
            self.state = "chase"
        elif self.state == "chase" and distance > BOSS_LOSE_RANGE:
            self.state = "patrol"

        if self._stun_timer > 0:
            self.velocity.x = 0
        elif self.state == "chase":
            dx = player.position.x - self.position.x
            if abs(dx) > CHASE_DEADZONE:
                self.direction = 1 if dx > 0 else -1
                self.velocity.x = self.direction * BOSS_CHASE_SPEED
            else:
                self.velocity.x = 0
        else:
            self.velocity.x = self.direction * BOSS_PATROL_SPEED

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

        if self._stun_timer <= 0:
            hit_wall = self.velocity.x == 0
            ledge_ahead = on_ground and is_ledge_ahead(
                self.rect, solid_tiles, self.direction, 1, TILE_SIZE
            )
            if hit_wall or ledge_ahead:
                self.direction *= -1

        self.position.update(self.rect.topleft)
        if self._stun_timer <= 0:
            self._update_animation(dt)

    def _update_animation(self, dt):
        self._anim_timer += dt
        if self._anim_timer >= ANIM_FRAME_DURATION:
            self._anim_timer = 0.0
            self._anim_frame = (self._anim_frame + 1) % len(FRAMES)
        self.image = load_image_scaled(FRAMES[self._anim_frame], BOSS_SCALE)

    def draw(self, screen, camera_offset):
        if self._stun_timer > 0:
            flash = self.image.copy()
            flash.fill((255, 255, 255, 140), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(flash, self.rect.topleft - camera_offset)
        else:
            screen.blit(self.image, self.rect.topleft - camera_offset)
