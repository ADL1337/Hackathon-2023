import pygame

from game_data import *
from menu import Menu, MenuPause
from level import *
from utils import CustomLoader
from player import Player

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.menu = Menu(self.screen)
        self.mode = "Menu"
        self.player = Player((0, 300))
        self.plateforms_group = pygame.sprite.Group()
        self.loader = CustomLoader("res/stats.json")
        self.pause_menu = None
        self.level_number = 1
        self.levels = [Level1]

    def save_stat(self):
        self.loader["distance_travelled"] += int(self.player.distance_travelled / 100)
        self.loader.save()

    def update(self):
        self.screen.fill("black")
        if self.mode == "Menu":
            self.menu.update()
            if self.menu.play:
                self.mode = "Level"
                self.menu = None
                self.level = self.levels[self.level_number-1](self.screen, self.player, 0)
        elif self.mode == "Pause":
            self.pause_menu.update()
            if self.pause_menu.etat == "Quit":
                self.mode = "Quit"
            if self.pause_menu.etat == "Continue":
                self.mode = "Level"
                self.level.mode = "InGame"
        else: # En jeux
            if self.level.mode == "Pause" and self.mode != "Pause":
                self.mode = "Pause"
            if self.mode == "Level":
                self.level.update()
                if self.level.mode == "Pause":
                    self.pause_menu = MenuPause(self.screen)
                    self.mode = "Pause"









