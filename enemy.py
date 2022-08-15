import pygame
from entity import Entity
from settings import *
from support import *
from particles import AnimationPlayer

class Enemy(Entity):
    def __init__(self, enemy_name, position, groups, obstacle_sprites, damage_player_func, trigger_death_particles_func, reward_player_func):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics
        self.import_graphics(enemy_name)
        self.status = 'idle'
            # frame_index is inherited from Entity
        self.image = self.animations[self.status][self.frame_index].convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

        # movement
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        # stats from settings.py
        self.enemy_name = enemy_name        
        enemy_info = enemy_dict[self.enemy_name]
        self.health = enemy_info['health']
        self.exp = enemy_info['exp']
        self.speed = enemy_info['speed']
        self.attack_damage = enemy_info['damage']
        self.recoil = enemy_info['recoil']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']
        self.attack_type = enemy_info['attack_type']

        # Experience
        self.reward_player_func = reward_player_func  # This object is a passed function from level.py

        # player interaction / cooldown timer
        self.can_attack = True
        self.attack_cooldown = 400  # ms
        self.attack_time = None     # No need to initialize with a value
        self.damage_player_func = damage_player_func  # Making an object of a function

        # invincibility timer - Otherwise we attack 60x per second due to FPS
        self.vulnerable = True
        self.hit_time = None
        self.hit_duration = 300     # ms

        # particles/animation
        self.trigger_death_particles_func = trigger_death_particles_func

    def import_graphics(self, name):
        self.animations = { 'idle': [], 'move': [], 'attack': [] }

        for animation in self.animations.keys():
            # Path to folders containing animations; folders named same as dict keys.
            self.animations[animation] = import_folder(path.join("graphics", "enemies", name, animation))
    
    def scope_player(self, player):
        # returns scalar and vector tuple (distance, direction) relative from enemy to hero
        # Pygame has built in Vector math
        hero = pygame.math.Vector2(player.hitbox.center)
        enemy = pygame.math.Vector2(self.hitbox.center) # 2-d vector

        distance = (hero - enemy).magnitude()

        if distance > 0: # can't normalize 0
            direction = (hero - enemy).normalize()
        else:
            direction = pygame.math.Vector2() # (0,0)

        return (distance, direction) # make iterable tuple with ()

    def get_status(self, player):
        
        distance = self.scope_player(player)[0]       

        if distance <= self.attack_radius and self.can_attack:
            # ensures attacking always starts frame 1
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
            
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            # start timer
            self.attack_time = pygame.time.get_ticks()
            # input amount and type, health is subtracted if player vulnerable and hit
            self.damage_player_func(self.attack_damage, self.attack_type)
    
        elif self.status == 'move':
            self.direction = self.scope_player(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        # Assign image files (frames of animation) from import_player_assets() to list
        frames = self.animations[self.status]

        # Loop over the frame index. 0, 0.15. 0.30, 0.45, 0.60, 0.75, 0.90, 1.05
        # Smaller the 'speed', longer it takes to sum toward next whole number
        self.frame_index += self.animation_speed

        # Loop from last image to first image
        if self.frame_index >= len(frames):
            # Remove can_attack flag only after full animation loop
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        
        # Set the image and update the rect. Converting float to int controls the speed, ensures int index.
        # Clever way to control animation speed
        self.image = frames[int(self.frame_index)]

        # Aligning the center ensures any change in image dimensions from frame to frame is not noticeable
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # Ignore if enemy is attackable (yet to be hit)
        if not self.vulnerable:
            # flicker
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            # don't flicker
            self.image.set_alpha(255)  # Full opaque

    def cooldown(self):
            # Start the stopwatch
        current_time = pygame.time.get_ticks()

        if not self.can_attack:            
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.hit_duration:
                self.vulnerable = True

    def receive_damage(self, player, attack_type):
        # We have to slow this down; else 60x a second
        if self.vulnerable:
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage() 
            else:
                # magic damage
                self.health -= player.get_full_magic_damage()
                
            pygame.mixer.Sound.play(hit_wav)
        
        # timer stuff
        self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False

    def hit_reaction(self):
        # Prevent recoil if enemy is attackable
        if not self.vulnerable:
            # Negating a vector creates a vector in the opposite direction
            # Effect magnitude of recoil per enemy_dict in settings.py, see __init__()
            self.direction *= -(self.recoil)

    def check_death(self):
        # "self" is a sprite, which we kill after creating a death animation
        if self.health <= 0:
            # kill() removes the sprite from the sprite group and that's it; apparently it still has a position before draw update
            self.kill()
            self.trigger_death_particles_func(self.rect.center, self.enemy_name)
                # death sound
            pygame.mixer.Sound.play(enemy_death_wav)

            # reward the player
            self.reward_player_func(self.exp)

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.check_death()
        self.cooldown()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)      
