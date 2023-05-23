import pygame, sys
from game_data import WIDTH, HEIGHT
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

from boss import *
single = pygame.sprite.GroupSingle()
boss = Boss1((0,0), 5, (1000, 300), "img/boss1/idle/spr_pepperman_idle_", single)
from level import Level
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 50)
level = Level(boss, screen)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            screen.fill("black")
            level.update()
            single.update()
            single.draw(screen)
            pygame.display.update()
    clock.tick(60)

