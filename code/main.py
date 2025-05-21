from settings import *
from player import Player

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

        # sprites
        self.player = Player(self.all_sprites, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

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