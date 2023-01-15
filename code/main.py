import pygame, sys
from settings import *
from level import Level

class Game():
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((Screen_Width, Screen_Height))
		self.clock = pygame.time.Clock()
		# window title
		pygame.display.set_caption('Stardew Falling')
		# initialize the level
		self.level = Level()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			dt = self.clock.tick() / 1000
			# Run our level
			self.level.run(dt)
			pygame.display.update()

if __name__ == "__main__":
	game = Game()
	game.run()

