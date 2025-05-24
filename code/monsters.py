from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, frames, collision_sprites, pos, player, speed, damage):
        super().__init__(groups)
        self.image = frames[0]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -40)

        self.damage = damage

        # movement
        self.direction = pygame.Vector2()
        self.speed = speed
        self.collision_sprites = collision_sprites

        # animation
        self.frames = frames
        self.frame_index = 0

        self.player = player

        self.death_time = 0
        self.death_duration = 400

    def update(self, delta_time):
        if self.death_time == 0:
            self.move(delta_time)
            self.animate(delta_time)
        else:
            self.update_death_timer()

    def animate(self, delta_time):
        self.frame_index = self.frame_index + 5 * delta_time if self.direction else 0
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def move(self, delta_time):
        player_position = pygame.Vector2(self.player.rect.center)
        position = pygame.Vector2(self.rect.center)
        self.direction = (player_position - position).normalize()

        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.check_collision(True)
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        self.check_collision(False)

        self.rect.center = self.hitbox_rect.center

    def check_collision(self, moving_horizontally):
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

    def destroy(self):
        self.death_time = pygame.time.get_ticks()

        surface = pygame.mask.from_surface(self.frames[0]).to_surface()
        surface.set_colorkey("black")
        self.image = surface

    def update_death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()

class Bat(Enemy):
    def __init__(self, groups, surfaces, collision_sprites, pos, player):
        super().__init__(groups, surfaces, collision_sprites, pos, player, 350, 10)

    def check_collision(self, _):
        pass

class Blob(Enemy):
    def __init__(self, groups, surfaces, collision_sprites, pos, player):
        super().__init__(groups, surfaces, collision_sprites, pos, player, 200, 25)

class Skeleton(Enemy):
    def __init__(self, groups, surfaces, collision_sprites, pos, player):
        super().__init__(groups, surfaces, collision_sprites, pos, player, 300, 20)