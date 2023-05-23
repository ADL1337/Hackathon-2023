import pygame
from layoutimport import import_csv_layout

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        layout = import_csv_layout(level_data['calc1'])
        