from settings import *
from player import Player
from sprites import *

from random import randint

class Game():
    def __init__(self):
    
        # basic setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivor")
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # sprites
        self.player = Player(self.all_sprites, self.collision_sprites, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        for i in range(6):
            random_position = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
            random_size = (randint(60, 120), randint(50, 100))
            CollisionSprite((self.all_sprites, self.collision_sprites), random_position, random_size)

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) /  1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(delta_time)

            # draw
            self.display_surface.fill("black")
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()