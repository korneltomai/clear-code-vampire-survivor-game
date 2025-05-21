from settings import *

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, groups, pos, size):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill("blue")
        self.rect = self.image.get_frect(center = pos)