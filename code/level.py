import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprites import GenericSprite, Water, WildFlower, Tree
from pytmx.util_pygame import load_pygame
from support import *

class Level:
    def __init__(self):

		# get the display surface
        self.display_surface = pygame.display.get_surface()

		# sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        # Create the player, etc in setup()
        self.setup()
        # Create the overlay for our game
        self.overlay = Overlay(self.player)
    
    def setup(self):
        # Using pytmx to import tiled map
        tmx_data = load_pygame("../data/map.tmx")

        # House
        for layer in ["HouseFloor", "HouseFurnitureBottom"]:
            for x, y, surface in tmx_data.get_layer_by_name(layer).tiles():
                GenericSprite((x * Tile_Size, y * Tile_Size), surface, self.all_sprites, Layers["house bottom"])

        for layer in ["HouseWalls", "HouseFurnitureTop"]:
            for x, y, surface in tmx_data.get_layer_by_name(layer).tiles():
                GenericSprite((x * Tile_Size, y * Tile_Size), surface, self.all_sprites, Layers["main"])

        # Fence
        for x, y, surface in tmx_data.get_layer_by_name("Fence").tiles():
            GenericSprite((x * Tile_Size, y * Tile_Size), surface, [self.all_sprites, self.collision_sprites], Layers["main"])

        # Water
        water_frames = import_folder("../graphics/water")
        for x, y, surface in tmx_data.get_layer_by_name("Water").tiles():
            Water((x * Tile_Size, y * Tile_Size), water_frames, self.all_sprites, Layers["water"])

        # Wild Flowers
        for obj in tmx_data.get_layer_by_name("Decoration"):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        # Trees
        for obj in tmx_data.get_layer_by_name("Trees"):
            Tree((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites], obj.name)

        # Collision Tiles
        for x, y, surface in tmx_data.get_layer_by_name("Collision").tiles():
            GenericSprite((x * Tile_Size, y * Tile_Size), pygame.Surface((Tile_Size, Tile_Size)), self.collision_sprites)

        # Create a player sprite at the given position and group
        for obj in tmx_data.get_layer_by_name("Player"):
            if obj.name == "Start":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
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
            # Loop through all of our sprites, sorting them so player can appear behind
            # objects
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    # Make a rect of the player's offset then subtract it 
                    # from the sprite's position to make effect of movement
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

