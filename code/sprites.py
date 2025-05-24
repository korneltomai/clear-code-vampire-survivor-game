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

        #audio
        self.shoot_sound = pygame.mixer.Sound(join("audio", "shoot.wav"))
        self.shoot_sound.set_volume(0.4)
        self.impact_sound = pygame.mixer.Sound(join("audio", "impact.ogg"))
        self.impact_sound.set_volume(0.6)

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

    def shoot(self, bullet_groups, enemy_sprites):
        if self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks() 

            pos = self.rect.center + self.player_direction * 50
            Bullet(bullet_groups, enemy_sprites, self.bullet_surface, pos, self.player_direction, self.impact_sound)
            self.shoot_sound.play()

    def update_cooldown(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown:
                self.can_shoot = True

class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, enemy_sprites, surf, pos, direction, impact_sound):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.direction = direction
        self.speed = 1000
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000
        self.enemy_sprites = enemy_sprites
        self.impact_sound = impact_sound

    def update(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

        collision_enemies = pygame.sprite.spritecollide(self, self.enemy_sprites, False, pygame.sprite.collide_mask)
        if collision_enemies:
            for enemy in collision_enemies:
                if enemy.death_time == 0:
                    enemy.destroy()
                    self.kill()
                    self.impact_sound.play()           