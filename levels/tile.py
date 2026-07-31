class Tile:
    def __init__(self, x, y, image, solid=True, hazard=False, oxygen_pickup=False, gravity_pickup=False):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
        self.solid = solid
        self.hazard = hazard
        self.oxygen_pickup = oxygen_pickup
        self.gravity_pickup = gravity_pickup

    def draw(self, screen, camera_offset):
        screen.blit(self.image, self.rect.topleft - camera_offset)
