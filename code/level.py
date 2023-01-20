import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprites import GenericSprite

class Level:
    def __init__(self):

		# get the display surface
        self.display_surface = pygame.display.get_surface()

		# sprite groups
        self.all_sprites = CameraGroup()

        # Create the player, etc in setup()
        self.setup()
        # Create the overlay for our game
        self.overlay = Overlay(self.player)
    
    def setup(self):
        # Create a player sprite at the given position and group
        self.player = Player((640, 360), self.all_sprites)
        # Create background
        GenericSprite(
            position = (0, 0),
            surf = pygame.image.load("../graphics/world/ground.png").convert_alpha(),
            groups = self.all_sprites,
            z = Layers["ground"]
        )

    def run(self,dt):
        self.display_surface.fill('black')
        # Draw our sprite on the display surface
        self.all_sprites.custom_draw(self.player)
        # Update our sprites
        self.all_sprites.update(dt)

        # Run our overlay
        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # Get position of player, then calculate the offset 
        # of the playe rinto the center of the screen
        self.offset.x = player.rect.centerx - Screen_Width / 2
        self.offset.y = player.rect.centery - Screen_Height / 2

        for layer in Layers.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    # Make a rect of the player's offset then subtract it 
                    # from the sprite's position to make effect of movement
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

