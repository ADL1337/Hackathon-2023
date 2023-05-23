import pygame

from game_data import *
#from menu import Menu # TODO: Create menu.py
#from game_loop import GameLoop # TODO: Create game_loop.py


class Game:
    pygame.init()
    pygame.display.set_caption(TITLE)
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    #menu = Menu(screen)
    #game_loop = GameLoop(screen)

    @classmethod
    def run(cls):
        #while True:
        #    cls.menu.run()
        #    cls.game_loop.run()
        pass


if __name__ == "__main__":
    print(Game.config["VOLUME"])
    print(Game.config["HOTKEYS"])
