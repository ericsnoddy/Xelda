import pygame
pygame.init()

# create a new Font object with default font, size 30
font = pygame.font.Font(None,30)

def debug(info, x = 10, y = 10):
    # Get a reference to the current display surface
    display_surface = pygame.display.get_surface()

    # Renders our info string onto a surface with white, anti-aliased font
    debug_surf = font.render(str(info), True, (255,255,255))

    # pygame.Surfaces don't have a position; this returns a rectangle with the size of our rendered string at (x,y)
    debug_rect = debug_surf.get_rect(topleft = (x,y))

    # Draw a black rectangle containing our debug_rect onto the display_surface
    pygame.draw.rect(display_surface, (0,0,0), debug_rect)

    # Blit the rectangle onto the display surface; draw.rect() wasn't sufficient because we have a font to render.
    display_surface.blit(debug_surf, debug_rect)




