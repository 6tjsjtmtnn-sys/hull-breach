import pygame


class Particle:
    def __init__(self, x, y, velocity, color, lifetime, radius=3):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(velocity)
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
        self.radius = radius

    @property
    def alive(self):
        return self.age < self.lifetime

    def update(self, dt):
        self.age += dt
        self.position += self.velocity * dt

    def draw(self, screen, camera_offset):
        life_ratio = max(0.0, 1 - self.age / self.lifetime)
        radius = max(1, round(self.radius * life_ratio))
        pos = self.position - camera_offset

        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*self.color, round(255 * life_ratio)), (radius, radius), radius)
        screen.blit(surface, (pos.x - radius, pos.y - radius))
