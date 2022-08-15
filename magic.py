import pygame
from random import randint
from settings import *
from particles import AnimationPlayer


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, cost, strength, groups):
        # Do we have enough energy to cast? Also, do nothing if we are at full health already
        if player.energy >= cost and player.health < player.stats['health']:
                # player.energy getting turned into float somewhere and I don't know why
            player.energy -= cost
            # We don't want to heal more than max HP...
            new_HP = player.health + strength
            if new_HP > player.stats['health']:
                player.health = player.stats['health']
            else:
                player.health = new_HP

            # play sound
            pygame.mixer.Sound.play(cast_heal_wav)

            # aura is an effect for all spell casts, heal is the particular effect (offset puts heal anim above player's head)
            self.animation_player.create_particles(player.rect.center, 'aura', groups)
            self.animation_player.create_particles(player.rect.center + pygame.math.Vector2(0,-60), 'heal', groups)

    def flame(self, player, cost, strength, groups):
        # Do we have enough energy to cast?
        if player.energy >= cost:
            player.energy -= cost

            # play sound
            pygame.mixer.Sound.play(cast_flame_wav)
        
            # We need to know which direction to send the flames
            # I use split('_') bc status could be 'right_idle' for example (see player.py)
            if player.status.split('_')[0]  == 'right': direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0]  == 'left': direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0]  == 'up': direction = pygame.math.Vector2(0,-1)
            else: direction = pygame.math.Vector2(0,1)

            # Generate 5 flame particles in a row, all tile adjacent
            # This is all Vector2 math
            for i in range(1,6):    
                if direction.x:     # Is horizontal
                    offset_x = i * direction.x * TILESIZE
                        # Adding randomness for effect
                    rand_offset = randint(-TILESIZE // 3, TILESIZE // 3)

                    x = player.rect.centerx + offset_x + rand_offset
                    y = player.rect.centery + rand_offset

                    self.animation_player.create_particles((x,y), 'flame', groups)
                else:               # Is vertical
                    offset_y = i * direction.y * TILESIZE
                    rand_offset = randint(-TILESIZE // 3, TILESIZE // 3)
                    x = player.rect.centerx + rand_offset
                    y = player.rect.centery + offset_y + rand_offset
                    self.animation_player.create_particles((x,y), 'flame', groups)