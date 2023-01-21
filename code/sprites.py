import pygame
from settings import *

class GenericSprite(pygame.sprite.Sprite):
    def __init__(self, position, surf, groups, z = Layers["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = position)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Water(GenericSprite):
    def __init__(self, position, frames, groups, z):

        # Animation setup
        self.frames = frames
        self.frame_index = 0

        # Sprite setup
        super().__init__(
            position = position, 
            surf = self.frames[self.frame_index],
            groups = groups,
            z = z
        )

    def animate(self, dt):
        """ Animate the water """

        # Increment our frame index by an arbitrary amount: 5
        self.frame_index = self.frame_index + 5 * dt

        # If wour frame goes over the amount of animation states we have, 
        # reset it to 0 so we restart the animation
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        """ All sprites called by update"""
        self.animate(dt)

class WildFlower(GenericSprite):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

class Tree(GenericSprite):
    def __init__(self, pos, surface, groups, name):
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)