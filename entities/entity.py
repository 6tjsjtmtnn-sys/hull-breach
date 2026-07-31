import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        raise NotImplementedError

    def draw(self, screen, camera_offset):
        screen.blit(self.image, self.rect.topleft - camera_offset)
