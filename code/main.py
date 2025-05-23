from pytmx.util_pygame import load_pygame
from random import randint

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

        # 

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.load_images()
        self.setup()

    def load_images(self):
        pass

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

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) /  1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

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

if __name__ == "__main__":
    game = Game()
    game.run()