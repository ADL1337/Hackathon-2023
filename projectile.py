import pygame
from entity import MovableEntity

class Projectile(MovableEntity):
    def __init__(self, dammage, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.dammage = dammage

    def check_dead(self):
        if not -self.image.get_width()/2 <= self.rect.x <= WIDTH + 200 or not -self.image.get_height()/2 <= self.rect.y <= HEIGHT:
            self.kill()

    def update(self):
        self.move()
        self.check_dead()

