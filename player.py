import pygame
from os import path
from settings import *
from support import *
from entity import Entity

class Player(Entity):
    # position is (x,y)-topleft; groups is list of sprite groups Player belongs to; obstacle_sprites for checking collision
    def __init__(self, position, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        # Inherit our Player __init__ from Sprite class
        super().__init__(groups)

        # Our inherited class requires self.image and self.rect
        self.image = pygame.image.load(path.join("graphics", "test", "player.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = position)

        # Our hitbox will be slightly smaller than the player rect; overlap provides illusion of depth
        self.hitbox = self.rect.inflate(0, -25)

        # Graphics and animations set-up
        self.import_player_assets()    

        # Player status which we'll use to determine player animations; eg, down_attack or left_idle.
        self.status = 'down'

        # PLAYER STATS
        self.stats = { 'maxhealth': 100, 'maxenergy': 100, 'attack': 10, 'magic': 4, 'speed': 5 }
            # Cannot level up further
        self.max_stats = { 'maxhealth': 300, 'maxenergy': 140, 'attack': 20, 'magic': 10, 'speed': 10 }
        self.upgrade_cost = { 'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100 }
        self.health = self.stats['maxhealth']
        self.energy = self.stats['maxenergy']
        self.exp = 500        
            # self.speed is a scalar velocity we will multiply with the direction vector
        self.speed = self.stats['speed']

        # We use a cooldown timer in milliseconds to avoid key spamming 60x per second.
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # Invulnerability timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # WEAPONS
        # We can manipulate passed functions as objects without (), at expense of readability 
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
            # timer
        self.can_switch_weapon = True
        self.switch_cooldown = 200
        self.switch_time = None

        # weapon_dict imported from settings.py, listified in order to index
        self.weapon_index = 0   # default sword
        self.weapon = list(weapon_dict.keys())[self.weapon_index]

        # MAGIC
        self.create_magic = create_magic
        # self.destroy_magic = destroy_magic
        self.can_switch_magic = True
        self.switch_magic_time = None
        self.magic_index = 0
        self.magic = list(magic_dict.keys())[self.magic_index]
        
        # For collision calculation; these sprites may or may not be visible
        self.obstacle_sprites = obstacle_sprites
 
    def import_player_assets(self):
        # This dictionary will contain lists of animation frames of the player
        self.animations = { 'up': [], 'down': [], 'left': [], 'right': [], 
                            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [] }

        for animation in self.animations.keys():
            # Path to folders containing animations; folders named same as dict keys.
            self.animations[animation] = import_folder(path.join("graphics", "player", animation))

    def key_input(self):
        # Inputs not accepted mid-attack
        if not self.attacking:    
            # Get all the key presses
            keys = pygame.key.get_pressed()

            # Movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # Attack input; see cooldown()
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # Cycle to previous/next weapon
            if keys[pygame.K_e] and self.can_switch_weapon:
                self.switch_time = pygame.time.get_ticks()
                
                # My solution for looping to the beginning of a list
                # I just catch an error if the index climbs out of range and reset to 0
                try:
                    self.weapon_index += 1
                    self.weapon = list(weapon_dict.keys())[self.weapon_index]
                except:
                    self.weapon_index = 0
                    self.weapon = list(weapon_dict.keys())[0]

                self.can_switch_weapon = False           

            # Magic input; see cooldown()
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                    # magic_dict from settings.py; magic attribute from self.stats
                spell = list(magic_dict.keys())[self.magic_index]
                strength = list(magic_dict.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_dict.values())[self.magic_index]['cost']
                self.create_magic(spell, strength, cost)

            # Cycle to previous/next spell
            if keys[pygame.K_q] and self.can_switch_magic:
                self.switch_magic_time = pygame.time.get_ticks()                
                try:
                    self.magic_index += 1
                    self.magic = list(magic_dict.keys())[self.magic_index]
                except:
                    self.magic_index = 0
                    self.magic = list(magic_dict.keys())[0]

                self.can_switch_magic = False    

    def get_status(self):

        # Check and update idle status
        if self.direction == (0,0):
            # We search self.status for a substring since variable could be something like "up_idle_idle_idle..."
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        # Check and update attack status
        if self.attacking:
            # Stop movement if Player is attacking
            self.direction.x, self.direction.y = (0, 0)

            # Update the status string
            if not "attack" in self.status:
                if "idle" in self.status:
                    # Overwrite idle
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + "_attack"
        else:
            # Remove attack status when not attacking
            if "attack" in self.status:
                self.status = self.status.replace('_attack', '')
        
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # Attack cooldown, including per weapon cooldown from settings.py
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_dict[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        # Switch weapon cooldown
        if not self.can_switch_weapon:
            if current_time - self.switch_time >= self.switch_cooldown:
                self.can_switch_weapon = True

        # Swtich magic cooldown
        if not self.can_switch_magic:
            if current_time - self.switch_magic_time >= self.switch_cooldown:
                self.can_switch_magic = True

        # Period of invulnerability after taking hit
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        # Assign image files (frames of animation) from import_player_assets() to list
        frames = self.animations[self.status]

        # Loop over the frame index. 0, 0.15. 0.30, 0.45, 0.60, 0.75, 0.90, 1.05
        # Smaller the 'speed', longer it takes to sum toward next whole number
        self.frame_index += self.animation_speed

        # Loop from last image to first image
        if self.frame_index >= len(frames):
            self.frame_index = 0
        
        # Set the image and update the rect. Converting float to int controls the speed, ensures int index.
        # Very clever way to control animation speed
        self.image = frames[int(self.frame_index)]

        # Aligning the center ensures any change in image dimensions from frame to frame is not noticeable
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # Flicker if invulnerable (player hit by enemy)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            # don't flicker; return to default opaque if transparent
            self.image.set_alpha(255)  # Full opaque

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_dict[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        magic_damage = magic_dict[self.magic]['strength']
        return base_damage + magic_damage

    def energy_recovery(self):
        if self.energy < self.stats['maxenergy']:
            # Remember this is 60x per second; trial and error to adjust
            self.energy += 0.01
        else:
            # In case our energy ends up greater than maxenergy, we need to set to max
            self.energy = self.stats['maxenergy']

    def update(self):
        self.key_input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()       

