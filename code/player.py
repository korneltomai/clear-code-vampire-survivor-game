from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_frect(center = pos)

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 500

    def update(self, delta_time):
        self.move(delta_time)

    def inpit(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time