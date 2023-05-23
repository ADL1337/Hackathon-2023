import pygame
from game_data import WIDTH, HEIGHT
from entity import MovableEntity

class Projectile(MovableEntity):
    # stats est liste contenant vect_direct, speed, pos, img_path, nbre de sprites d'animation + 1
    def __init__(self, stats, *groups):
        super().__init__(stats[0], stats[1], stats[2], stats[3], *groups)
        self.images_for_animation = self.create_image_list(stats[3], stats[4])

    def check_dead(self):
        if not -self.image.get_width()/2 <= self.rect.x <= WIDTH or not -self.image.get_height()/2 <= self.rect.y <= HEIGHT:
            self.kill()

    def update(self):
        self.move()
        self.check_dead()

