import pygame
from game_data import WIDTH, HEIGHT
from entity import MovableEntity

class Projectile(MovableEntity):
    def __init__(self, vect_direct, speed, pos, img_path, limit, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.images_for_animation = self.create_image_list(img_path, limit)

    def check_dead(self):
        if not -self.image.get_width()/2 <= self.rect.x <= WIDTH + 200 or not -self.image.get_height()/2 <= self.rect.y <= HEIGHT:
            self.kill()

    def update(self):
        self.move()
        self.check_dead()

