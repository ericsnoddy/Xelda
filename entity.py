import pygame

# For functions that enemies and the player have in common
class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # Create a 2-D vector for direction of travel; empty brackets default to (x=0,y=0)
        # East will be (1,0) - West (-1,0) - North (0,1) - South (0,-1) - Northeast (1,1) etc.
        self.direction = pygame.math.Vector2()

        # Technical data for animation. Need to track the current frame for seamless animation. See animate()
        self.frame_index = 0
        self.animation_speed = 0.15

    def move(self, speed):
        # Normalize the length of the direction vector to 1, otherwise diagonal travel is faster due to trig
        # pygame throws an error if you try to normalize a zero magnitude vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Move (x,y)-topleft of the sprite rect() by the velocity vector, check for collision with our hitbox
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        # Now we link the hitbox with our player rect by equating the (x,y)-center coords
        self.rect.center = self.hitbox.center

    def collision(self, direction):
    # We adjust the horiz position first and separately, instead of simultaneous, to avoid teleporting effect
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                # We have to determine the coords if a hitbox collision occurs and deny movement in that direction
                # Pygame I guess cannot provide the coords of collision, only T or F that collision occurred.
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right, collision likely from the right
                        # This denies overlap by altering the player's right coords to the obstacle's left coords
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left, collision likely from the left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down, collision likely from the bottom
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # moving up, collision likely from the top
                        self.hitbox.top = sprite.hitbox.bottom