from settings import *
from math import atan2, degrees

class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.is_ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        # player connection
        self.player = player
        self.distance = 100
        self.player_direction = pygame.Vector2(0, 1)

        # sprite setup
        super().__init__(groups)
        self.original_surface = pygame.image.load(join("images", "gun", "gun.png")).convert_alpha()
        self.image = self.original_surface
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

        self.bullet_surface = pygame.image.load(join("images", "gun", "bullet.png")).convert_alpha()
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown = 100

    def update(self, _):
        self.get_direction()
        self.rotate()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

        self.update_cooldown()
    
    def get_direction(self):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        player_position = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_position - player_position).normalize()

    def rotate(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.original_surface, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.original_surface, -(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def shoot(self, bullet_groups):
        if self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks() 

            pos = self.rect.center + self.player_direction * 50
            Bullet(bullet_groups, self.bullet_surface, pos, self.player_direction)

    def update_cooldown(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown:
                self.can_shoot = True

class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos, direction):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.direction = direction
        self.speed = 1000
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000

    def update(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, frames, collision_sprites, pos, player, speed):
        super().__init__(groups)
        self.image = frames[0]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -40)

        # movement
        self.direction = pygame.Vector2()
        self.speed = speed
        self.collision_sprites = collision_sprites

        # animation
        self.frames = frames
        self.frame_index = 0

        self.player = player

    def update(self, delta_time):
        self.move(delta_time)
        self.animate(delta_time)

    def animate(self, delta_time):
        self.frame_index = self.frame_index + 5 * delta_time if self.direction else 0
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def move(self, delta_time):
        player_position = pygame.Vector2(self.player.rect.center)
        position = pygame.Vector2(self.rect.center)
        self.direction = (player_position - position).normalize()

        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.collision(True)
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        self.collision(False)

        self.rect.center = self.hitbox_rect.center


    def collision(self, moving_horizontally):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if moving_horizontally:
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom

class Bat(Enemy):
    def __init__(self, groups, surfaces, collision_sprites, pos, player):
        super().__init__(groups, surfaces, collision_sprites, pos, player, 400)

class Blob(Enemy):
    def __init__(self, groups, surfaces, collision_sprites, pos, player):
        super().__init__(groups, surfaces, collision_sprites, pos, player, 200)

class Skeleton(Enemy):
    def __init__(self, groups, surfaces, collision_sprites, pos, player):
        super().__init__(groups, surfaces, collision_sprites, pos, player, 300)
