import pygame
import sys
from settings import *

pygame.init()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY = pygame.display.set_mode( (800, 600) )

    test_rect = pygame.rect.Rect( 20, 30, 200, 270 )
    test_rect.centery = 164.5
    print(test_rect.center)

    pygame.display.update()
