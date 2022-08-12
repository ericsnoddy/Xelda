import pygame
import sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        # initiate all modules instead of doing so individually
        pygame.init()

        # Set up our display window. WIDTH, HEIGHT imported from settings.py
        self.DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Xelda')

        # Initiate the clock for clock.tick(FPS)
        self.clock = pygame.time.Clock()

        # Initiate the level to pass to the game event loop
        self.level = Level()

    def run(self):
        # Game loop
        while True:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # black background
            self.DISPLAY.fill('black')

            # Run our initialized level
            self.level.run()

            # Update the screen for the next frame 
            pygame.display.update()            

            # Tick the clock for the next frame; FPS imported from settings.py
            self.clock.tick(FPS)

if __name__ == "__main__": 
    # Initialize and run a new game class -- begin the game loop
    game = Game()
    game.run()