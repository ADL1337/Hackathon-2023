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

def quit_game(game):
    pygame.quit()
    game.save_stat()
    quit()

while running:
    for event in pygame.event.get():
        if game.mode == "Quit":
            quit_game(game)
        if event.type == pygame.QUIT:
            quit_game(game)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if game.mode == "Menu":
                    game.menu.check_event(event)
                if game.mode == "Pause":
                    game.pause_menu.check_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.mode == "Pause":
                    game.mode = "Level"
                    game.level.mode = "InGame"
        if event.type == SCREEN_UPDATE:
            game.update()
            pygame.display.update()

    clock.tick(60)
