import pygame
from entity import MovableEntity

class Player(MovableEntity):
    def __init__(self, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.boost = False
        self.images_idle = self.create_image_list("img/player/idle/player_idle_", 2)
        self.images_run = self.create_image_list("img/player/run/player_run_", 11)
        self.images_shoot = self.create_image_list("img/player/shoot/player_shoot_", 16)
        self.images_spawn = self.create_image_list("img/player/spawn/player_spawn_", 8)

    def shoot(self):
        pass

    def jump(self):
        pass

    def take_dammage(self):
        pass

    def update(self):
        pass