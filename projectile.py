import pygame
from movableEntity import MovableEntity

class Projectile(MovableEntity):
    def __init__(self, dammage, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.dammage = dammage

    
