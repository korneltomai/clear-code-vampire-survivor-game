from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, pos):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-48, -48)

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

    def animate(self, delta_time):
        if self.direction.x != 0:
            self.state = "right" if self.direction.x > 0 else "left"
        if self.direction.y != 0:
            self.state = "down" if self.direction.y > 0 else "up"

        self.frame_index = self.frame_index + 5 * delta_time if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])] if self.direction else self.frames["standing"][self.state]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, delta_time):
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
