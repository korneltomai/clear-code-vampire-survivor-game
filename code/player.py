from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, pos):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hit_box_rect = self.rect.inflate(-50, 0)

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def update(self, delta_time):
        self.input()
        self.move(delta_time)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, delta_time):
        self.hit_box_rect.x += self.direction.x * self.speed * delta_time
        self.collision(True)
        self.hit_box_rect.y += self.direction.y * self.speed * delta_time
        self.collision(False)
        self.rect.center = self.hit_box_rect.center

    def collision(self, moving_horizontally):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hit_box_rect):
                if moving_horizontally:
                    if self.direction.x > 0:
                        self.hit_box_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hit_box_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0:
                        self.hit_box_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hit_box_rect.top = sprite.rect.bottom