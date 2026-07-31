class Tile:
    def __init__(self, x, y, image, solid=True, hazard=False, flip_zone=False):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
        self.solid = solid
        self.hazard = hazard
        self.flip_zone = flip_zone

    def draw(self, screen, camera_offset):
        screen.blit(self.image, self.rect.topleft - camera_offset)
