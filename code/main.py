from pytmx.util_pygame import load_pygame
from random import randint, choice

from settings import *
from player import Player
from sprites import *
from groups import AllSprites

class Game():
    def __init__(self):
        # basic setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivor")
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        # enemy spawning
        self.enemy_types = ["bat", "blob", "skeleton"]
        self.enemy_frames = {}
        self.enemy_spawn_positions = []
        self.enemy_spawn_cooldown = 2000
        self.enemy_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_timer, self.enemy_spawn_cooldown)
        
        self.load_images()
        self.setup()

    def load_images(self):
        for enemy_type in self.enemy_types:
            frames = []
            for folder_path, _, file_names in walk(join("images", "enemies", enemy_type)):
                if file_names:
                    for file_name in sorted(file_names, key = lambda file_name: int(file_name.split(".")[0])):
                        full_path = join(folder_path, file_name)
                        frames.append(pygame.image.load(full_path).convert_alpha())
            self.enemy_frames[enemy_type] = frames
                        

    def setup(self):
        map = load_pygame(join("data", "maps", "world.tmx"))

        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite((self.all_sprites), image, (x * TILE_SIZE, y * TILE_SIZE))

        for object in map.get_layer_by_name("Collisions"):
            CollisionSprite((self.collision_sprites), pygame.Surface((object.width, object.height)), (object.x, object.y))

        for object in map.get_layer_by_name("Objects"):
            CollisionSprite((self.all_sprites, self.collision_sprites), object.image, (object.x, object.y))

        for marker in map.get_layer_by_name("Entities"):
            if marker.name == "Player":
                self.player = Player(self.all_sprites, self.collision_sprites, (marker.x, marker.y))
                self.gun = Gun(self.all_sprites, self.player)
            elif marker.name == "Enemy":
                self.enemy_spawn_positions.append((marker.x, marker.y))

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) /  1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_timer:
                    self.spawn_enemy()

            # update
            self.handle_input()
            self.all_sprites.update(delta_time)

            # draw
            self.display_surface.fill("black")
            self.all_sprites.draw(self.player.rect.center)

            pygame.display.update()

        pygame.quit()

    def handle_input(self):
        if pygame.mouse.get_pressed()[0]:
            self.gun.shoot((self.all_sprites, self.bullet_sprites))

    def spawn_enemy(self):
        random_enemy_type = choice(self.enemy_types)
        random_enemy_spawn_position = choice(self.enemy_spawn_positions)

        if random_enemy_type == "bat":
            Bat((self.all_sprites), self.enemy_frames[random_enemy_type], self.collision_sprites, random_enemy_spawn_position, self.player)
        elif random_enemy_type == "blob":
            Blob((self.all_sprites), self.enemy_frames[random_enemy_type], self.collision_sprites, random_enemy_spawn_position, self.player)
        elif random_enemy_type == "skeleton":
            Skeleton((self.all_sprites), self.enemy_frames[random_enemy_type], self.collision_sprites, random_enemy_spawn_position, self.player)

if __name__ == "__main__":
    game = Game()
    game.run()