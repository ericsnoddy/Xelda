import pygame
from settings import *
from os import path

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)

        # Status is always player direction + optional "_string"; we can split off the optional string
        direction = player.status.split('_')[0]

        # GRAPHICS
        # weapon images are named after direction for convenience
        weapon_file_path = path.join("graphics", "weapons", player.weapon, direction + ".png")
        self.image = pygame.image.load(weapon_file_path).convert_alpha()

        # PLACEMENT
        # Here we attach Weapon rect to Player rect with offset for alignment 
        match direction:
            case 'up':
                self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))
            case 'down':
                self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
            case 'left':
                self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
            case 'right': 
                self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
            # Default case ensures we never throw an error
            case _:
                self.rect = self.image.get_rect(center = player.rect.center)
