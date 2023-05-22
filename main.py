import pygame, sys
from game_data import WIDTH, HEIGHT
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

from boss import *
single = pygame.sprite.GroupSingle()
boss = Boss1((0,0), 5, (100, 300), "img/boss1/ilde/spr_pepperman_jump_0.png",single)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            single.update()
            screen.fill("black")
            single.draw(screen)
            pygame.display.update()
    clock.tick(60)

