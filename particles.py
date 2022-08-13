import pygame
from random import choice
from os import path
from support import import_folder

class AnimationPlayer:
    def __init__(self):

        self.frames = {
            # magic
            'flame': import_folder(path.join("graphics", "particles", "flame", "frames")),
            'aura': import_folder(path.join("graphics", "particles", "aura")),
            'heal': import_folder(path.join("graphics", "particles", "heal", "frames")),
            
            # attacks 
            'claw': import_folder(path.join("graphics", "particles", "claw")),
            'slash': import_folder(path.join("graphics", "particles", "slash")),
            'sparkle': import_folder(path.join("graphics", "particles", "sparkle")),
            'leaf_attack': import_folder(path.join("graphics", "particles", "leaf_attack")),
            'thunder': import_folder(path.join("graphics", "particles", "thunder")),

            # enemy deaths
            'squid': import_folder(path.join("graphics", "particles", "smoke_orange")),
            'raccoon': import_folder(path.join("graphics", "particles", "raccoon")),
            'spirit': import_folder(path.join("graphics", "particles", "nova")),
            'bamboo': import_folder(path.join("graphics", "particles", "bamboo")),
            
            # leaves 
            'leaf': (
                import_folder(path.join("graphics", "particles", "leaf1")),
                import_folder(path.join("graphics", "particles", "leaf2")),
                import_folder(path.join("graphics", "particles", "leaf3")),
                import_folder(path.join("graphics", "particles", "leaf4")),
                import_folder(path.join("graphics", "particles", "leaf5")),
                import_folder(path.join("graphics", "particles", "leaf6")),
                self.reflect_images(import_folder(path.join("graphics", "particles", "leaf1"))),
                self.reflect_images(import_folder(path.join("graphics", "particles", "leaf2"))),
                self.reflect_images(import_folder(path.join("graphics", "particles", "leaf3"))),
                self.reflect_images(import_folder(path.join("graphics", "particles", "leaf4"))),
                self.reflect_images(import_folder(path.join("graphics", "particles", "leaf5"))),
                self.reflect_images(import_folder(path.join("graphics", "particles", "leaf6")))
                )
            }

    def reflect_images(self, frames):
        # This method will mirror-reverse all frames in an animation for variety's sake
        flipped_frames = []
        for frame in frames:
            # flip-x True, flip-y False
            flipped_frames.append(pygame.transform.flip(frame, True, False))
        return flipped_frames

    def create_flora_particles(self, position, groups):
        # we randomize between all leaf animations with random.choice() function
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(position, animation_frames, groups)

    def create_particles(self, position, animation_type, groups):
        # Reused for various effects so we call animation_type intead of attack_type
        animation_frames = self.frames[animation_type]
        ParticleEffect(position, animation_frames, groups)

    def create_enemy_death(self, position, enemy_name, groups):
        animation_frames = self.frames[enemy_name]
        ParticleEffect(position, animation_frames, groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, animation_frames, groups):
        super().__init__(groups)
        # animation
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames

        # Of course all Sprite classes require a self.image and self.rect constructor
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = position)

        # Give it a sprite_type
        self.sprite_type = 'magic'

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()