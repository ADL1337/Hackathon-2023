import pygame
from game_data import *
from game import Game
pygame.init()
pygame.mixer.init()
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 50)
game = Game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if game.mode == "Menu":
                    game.menu.check_event(event)
        if event.type == SCREEN_UPDATE:
            game.update()
            pygame.display.update()

    clock.tick(60)
