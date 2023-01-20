import pygame, sys
from settings import *
from support import *
from timer import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assets()
        self.status = "down_idle" # Player's current animation state
        self.frame_index = 0 # The current frame of the current animation state

        # General Setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = Layers["main"]

        # Movement attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # Timers
        self.timers = {
            "tool use": Timer(350, self.use_tool),
            "tool switch": Timer(200),
            "seed use": Timer(350, self.use_seed),
            "seed switch": Timer(200)
        }

        # Tools: axe, hoe, water
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = "water"

        # Seeds to plant
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]


    
    def use_seed(self):
        print(f"Planting {self.selected_seed} seed")



    def use_tool(self):
        print(f"Using {self.selected_tool}")



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

        # Directions
        if not self.timers["tool use"].active:
            # If we are not using a tool, player is allowed to move
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

            # Tool use on space
            if keys[pygame.K_SPACE]:
                # Activate our tool use timer since we just used a tool, so you have to wait
                # for cooldown before using tool again
                self.timers["tool use"].activate()
                # If the player is using a tool, reset their movement vector
                self.direction = pygame.math.Vector2()
                # Set frame index to 0 so animation for tool starts at 0
                self.frame_index = 0

            # Change tools
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                # Activate our tool switch timer so we can't switch tools for 200 ms again
                self.timers['tool switch'].activate()
                # Increase our tool index by 1 so we switch to next tool, if we go over the amount of 
                # tools we have reset to index 0
                self.tool_index += (1 if self.tool_index < len(self.tools) - 1 else -1 * (len(self.tools) - 1))
                # Change our selected tool
                self.selected_tool = self.tools[self.tool_index]
                # Print our newly selected tool
                print(f"Selecting {self.tools[self.tool_index]} tool")

            # Seed use on Control
            if keys[pygame.K_LCTRL] and not self.timers['seed use'].active:
                # Activate our timer for planting seeds that will also call method to plant seeds
                self.timers['seed use'].activate()
                # If the player is using a tool, reset their movement vector
                self.direction = pygame.math.Vector2()
                # Set frame index to 0 so animation for tool starts at 0
                self.frame_index = 0


            # Change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                # Activate our seed switch timer so we can't switch seeds for 200 ms again
                self.timers['seed switch'].activate()
                # Increase our seed index by 1 so we switch to next seed, if we go over the amount of 
                # seeds we have reset to index 0
                self.seed_index += (1 if self.seed_index < len(self.seeds) - 1 else -1 * (len(self.seeds) - 1))
                # Change our selected seed
                self.selected_seed = self.seeds[self.seed_index]
                # Print our newly selected seed
                print(f"Selecting {self.seeds[self.seed_index]} seed")

        # If we press the escape key, quit the game
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()



    def get_status(self):
        """" Updates the status of the player's movement """

        # Player's x and y vectors equal 0, so not moving
        if self.direction.magnitude() == 0:
            self.status = self.status.split("_")[0] + "_idle"

        # Tools
        if self.timers["tool use"].active:
            self.status = self.status.split("_")[0] + "_" + self.selected_tool



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



    def update_timers(self):
        # Update our timers if they are active
        for timer in self.timers:
            if self.timers[timer].active:
                self.timers[timer].update()



    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)
