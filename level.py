import pygame
from os import path
from random import choice
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from support import *
from weapon import Weapon
from ui import UI
from debug import debug


class Level:
    def __init__(self):
        # Get a reference to the currently set display surface
        # This is a useful function to avoid having to pass the surface through the __init__ function input.
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup; required by pygame.sprite.Sprite. I customize one as a "camera"
        self.visible_sprites = YSortedCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # For magic/weapon attack sprites
        self.current_attack = None
        self.attacking_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Sprite setup
        self.create_map()

        # User Interface
        self.ui = UI()

    def create_map(self):
        # From our support.py methods we generate dictionaries of map data
        layouts = {
            "boundary": import_csv_layout(path.join("map", "map_FloorBlocks.csv")),
            "flora": import_csv_layout(path.join("map", "map_Grass.csv")),
            "object": import_csv_layout(path.join("map", "map_Objects.csv")),
            "entity": import_csv_layout(path.join("map", "map_Entities.csv"))
        }
        graphics = {
            "flora": import_folder(path.join("graphics", "flora")),
            "objects": import_folder(path.join("graphics", "objects"))            
        }

        # Draw all the things, left to right, top to bottom
        # items() turns our dict into a list; enumerate() returns the index with the value
        for tile_style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        # TILESIZE from settings.py is # of pixels to space out each output; '-1' means no entity at that tile
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        # Here is where we differentiate tile behavior
                        # boundary is collidable but not visible
                        if tile_style == "boundary":
                            Tile((x,y), [self.obstacle_sprites], "invisible")
                        if tile_style == "flora":
                            # A flora Tile is collidable and visible
                            rand_flora_surface = choice(graphics["flora"])
                            Tile((x,y), 
                                [self.visible_sprites, 
                                self.obstacle_sprites, 
                                self.attackable_sprites], 
                                "flora", 
                                rand_flora_surface
                            )
                        if tile_style == "object":
                            # An object Tile is collidable and visible
                            # Object filenames conveniently sync with values in the csv, so we can use indexes to draw them.
                            object_surface = graphics["objects"][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], "object", object_surface)
                        if tile_style == "entity":
                            # An entity Tile is collidable and visible
                            if col == '394':  # this tile number is from Tiled editor, in csv file
                            # HERE IS OUR PLAYER ENTITY drawn on top of all but enemies
                            # Python FYI: we are passing the function create_attack(), not calling it, so no '( )'
                            # This is so Player() has access to Weapon(), but both remain a sub-routine of Level()
                                self.player = Player((x,y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_attack,
                                    self.create_magic
                                )
                            else:
                                if col == '390': enemy_name = 'bamboo'
                                elif col == '391': enemy_name = 'spirit'
                                elif col == '392': enemy_name ='raccoon'
                                else: enemy_name = 'squid'
                                
                                Enemy(enemy_name, (x,y), 
                                    [self.visible_sprites, self.attackable_sprites], 
                                    self.obstacle_sprites
                                )

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attacking_sprites])

    def destroy_attack(self):
        if self.current_attack:
            # Sprite.kill() removes Sprite from (visible_) Group; for next DISPLAY update 
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        pass

    def create_magic(self, spell, strength, cost):
        print(spell)
        print(strength)
        print(cost)

    def run(self):
        # Draw and update with custom draw; no args needed for update because we already have the display_surface
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display_hud(self.player)

# This custom Group acts as our camera, sorted by Y-coord so we can add a bit of overlap for illusion of depth
# Y-sorting will help us control drawing order and overlap.
class YSortedCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # General setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # This offset acts as our camera, centering the player; see custom_draw()
        # First we get (x,y)-center of the display surface. Rect() auto converts float to int
        self.centerx, self.centery = (self.display_surface.get_size()[0] / 2, 
                                      self.display_surface.get_size()[1] / 2)
        self.offset = pygame.math.Vector2(self.centerx, self.centery)

        # Creates the floor; converts the image to same pixel format as the display Surface; puts in it a rect
        self.floor_image = pygame.image.load(path.join("graphics", "tilemap", "ground.png")).convert()
        self.floor_rect = self.floor_image.get_rect(topleft=(0,0))

    def custom_draw(self, player):
        # We get the offset vector by subtracting display_surface's (x,y)-center coords from player's (x,y)-center coords
        self.offset.x = player.rect.centerx - self.centerx
        self.offset.y = player.rect.centery - self.centery

        # Draws the floor with our camera-centering offset
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_image, floor_offset_pos)

        # Sorts the sprites by default by their centery position using a lambda function for the key
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            # Offsetting our sprites from the display surface acts as our centering camera.
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

