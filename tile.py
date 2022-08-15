import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, position, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        # inherit the Sprite __init__, pass in our sprite groups
		super().__init__(groups)

		# This is so we can specialize our tile sprites; eg, a tree obstacle or grass
		self.sprite_type = sprite_type

        # pygame.sprite.Sprite requires image and rect for __init__
		self.image = surface

		if sprite_type == "object":
			# do an offset for tall objects so tiles drawn correctly; large object height is exactly double TILESIZE
			self.rect = self.image.get_rect(topleft = (position[0], position[1] - TILESIZE))
		else:
			self.rect = self.image.get_rect(topleft = position)

		# Our hitbox will be slightly smaller than the image rectangle; overlap provides illusion of depth
		# We attach the hitbox to the sprite rect. This allows player to walk behind boundary objects.
		self.hitbox = self.rect.inflate(-3, HITBOX_Y_OFFSET[sprite_type])