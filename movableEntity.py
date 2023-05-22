import pygame
from entity import Entity

class MovableEntity(Entity):
    def __init__(self, vect_direct, speed, pos, img_path, *groups):
        super().__init__(pos, img_path, *groups)
        self.vect = pygame.math.Vector2(vect_direct)
        self.speed = speed