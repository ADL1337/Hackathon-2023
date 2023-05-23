import pygame, sys
from levels import Level
from level_data import level_1

pygame.init()

tile_width = 80
tile_height = 48
tile_size = 16
screen_height = 720 #tile_width * tile_height
screen_width = 1280
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(level_1, screen)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill('grey')

	pygame.display.update()
	clock.tick(60)