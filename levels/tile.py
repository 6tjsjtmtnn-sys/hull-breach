class Tile:
    def __init__(self, x, y, image, solid=True, hazard=False):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
        self.solid = solid
        self.hazard = hazard

    def draw(self, screen, camera_offset):
        screen.blit(self.image, self.rect.topleft - camera_offset)
