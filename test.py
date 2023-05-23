import pygame, sys
from game_data import WIDTH, HEIGHT
from utils import CustomLoader
from level import Level
from player import Player
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

from boss import *
single = pygame.sprite.GroupSingle()
boss = Boss1((0,0), 5, (1000, 300), "img/boss1/idle/spr_pepperman_idle_")
from level import Level
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 50)
player = Player((0,0), 10, (1000, 300), "img/player/idle/player_idle_")
level = Level(boss, screen, player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            screen.fill("black")
            level.update()
            pygame.display.update()
    clock.tick(60)

