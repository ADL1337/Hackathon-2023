import pygame

from game_data import *
from menu import Menu
from level import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.menu = Menu(self.screen)
        self.mode = "Menu"
        self.plateforms_group = pygame.sprite.Group()

    def update(self):
        self.screen.fill("black")
        if self.mode == "Menu":
            self.menu.update()
            if self.menu.play:
                self.mode = "Level1"
                self.menu = None
                self.level = Level1(self.screen)
                self.level.create_plat(0)
        else: # En jeux
            if self.mode == "Level1":
                self.level.update()









