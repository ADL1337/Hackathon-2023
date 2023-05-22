import pygame

from game_data import *
from utils import *


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, image, action):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.action = action


class Menu:
    config = CustomLoader(PATHS["config"])
    stats = CustomLoader(PATHS["stats"])
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(PATHS["font"], FONT_SIZE)
        self.main_buttons = pygame.sprite.Group()
        self.options_buttons = pygame.sprite.Group()
        self.volume_buttons = pygame.sprite.Group()
        self.hotkey_buttons = pygame.sprite.Group()
    
    def run(self):
        pass
