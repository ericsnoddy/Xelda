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

        # Initiate our Level class to pass to the game event loop
        self.level = Level()

    def run(self):
        # Game loop
        while True:
            # Event loop
            # Pygame records every 'event' per loop, such as key presses and mouse clicks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 'X'-out or ALT-F4
                    pygame.quit()
                    sys.exit()

                # Pausing the game / upgrade screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pause_and_upgrade_key: # from settings.py
                        self.level.upgrade_GUI()

             # black background
            self.DISPLAY.fill('black')

            # Run our initial ized level
            self.level.run()

            # Update the screen for the next frame 
            pygame.display.update()            

            # Tick the clock for the next frame; FPS imported from settings.py
            self.clock.tick(FPS)

if __name__ == "__main__": 
    # Initialize and run a new game class -- begin the game loop
    game = Game()
    game.run()