import pygame, sys
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assets()
        self.status = "down_idle" # Player's current animation state
        self.frame_index = 0 # The current frame of the current animation state

        # General Setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # Movement attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def import_assets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}

        for animation in self.animations.keys():
            full_path = '..\graphics\character\\' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        """ Create the player animations """

        # Increment our frame index by an arbitrary amount: 4
        self.frame_index = self.frame_index + 4 * dt

        # If wour frame goes over the amount of animation states we have, 
        # reset it to 0 so we restart the animation
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        # Return list with keys being pressed
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0

        # If we press the escape key, quit the game
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    def get_status(self):
        """ If the player is not moving, add
        idle to the status """
        # Status in up, down, left, right
        if self.status in ["up", "down", "left", "right"]:
            # Player is not moving
            if self.direction.y == 0 and self.direction.x == 0:
                self.status = self.status + "_idle"

    def move(self, dt):
        # Normalize the direction vector so speed is constant
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.get_status()

        self.move(dt)
        self.animate(dt)
