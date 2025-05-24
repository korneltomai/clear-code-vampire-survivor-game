from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, enemy_sprites, pos):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-48, -48)

        self.hit_sound = pygame.mixer.Sound(join("audio", "player_hit.wav"))
        self.hit_sound.set_volume(0.5)

        # damage
        self.enemy_sprites = enemy_sprites
        self.health_points = 100
        self.invincible = False
        self.last_hit_time = 0
        self.iframes = 500

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

        # animation
        self.load_images()
        self.state = "down"
        self.frame_index = 0

    def load_images(self):
        self.frames = {"left": [], "right": [], "up": [], "down": []}

        for state in self.frames.keys():
            for folder_path, subfolders, file_names in walk(join("images", "player", state)):
                if file_names:
                    for file_name in sorted(file_names, key = lambda file_name: int(file_name.split(".")[0])):
                        full_path = join(folder_path, file_name)
                        surface = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surface)

        self.frames["standing"] = {
            "left": pygame.image.load(join("images", "player", "standing", "left.png")).convert_alpha(), 
            "right": pygame.image.load(join("images", "player", "standing", "right.png")).convert_alpha(), 
            "up": pygame.image.load(join("images", "player", "standing", "up.png")).convert_alpha(), 
            "down": pygame.image.load(join("images", "player", "standing", "down.png")).convert_alpha()
        }

    def update(self, delta_time):
        self.handle_input()
        self.move(delta_time)
        self.animate(delta_time)
        self.update_iframes()
        self.check_enemy_collision()

    def animate(self, delta_time):
        if self.direction.x != 0:
            self.state = "right" if self.direction.x > 0 else "left"
        if self.direction.y != 0:
            self.state = "down" if self.direction.y > 0 else "up"

        self.frame_index = self.frame_index + 5 * delta_time if self.direction else 0

        if self.invincible:
            original_image = self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])] if self.direction else self.frames["standing"][self.state]
            surface = pygame.mask.from_surface(original_image).to_surface()
            surface.set_colorkey("black")
            self.image = surface
        else:
            self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])] if self.direction else self.frames["standing"][self.state]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, delta_time):
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

    def check_enemy_collision(self):
        if not self.invincible:
            collided_enemies = pygame.sprite.spritecollide(self, self.enemy_sprites, False, pygame.sprite.collide_mask)
            for enemy in collided_enemies:
                self.hit_sound.play()
                self.last_hit_time = pygame.time.get_ticks()
                self.invincible = True
                self.health_points = max(self.health_points - enemy.damage, 0)

    def update_iframes(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time >= self.iframes:
                self.invincible = False

class HealthDisplay(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.font = pygame.font.Font(size=60)
        self.image = self.font.render("0", True, (20, 20, 20))
        self.rect = self.image.get_rect(midbottom = (player.rect.centerx, player.rect.top))
        self.player = player

    def update(self, _):
        self.image = self.font.render(str(self.player.health_points), True, (20, 20, 20))
        self.rect = self.image.get_rect(midbottom = (self.player.rect.centerx, self.player.rect.top))