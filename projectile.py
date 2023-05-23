import pygame
from game_data import WIDTH, HEIGHT
from entity import MovableEntity

class Projectile(MovableEntity):
    # stats est liste contenant vect_direct, speed, pos, img_path, nbre de sprites d'animation
    def __init__(self, stats, *groups):
        super().__init__(stats[0], stats[1], stats[2], stats[3], *groups)
        self.images_for_animation = self.create_image_list(stats[3], stats[4])
        self.sym_x = stats[5]
        self.sym_y = stats[6]
        self.size_factor = stats[7]

    def check_dead(self):
        if not -200 <= self.rect.x <= WIDTH or not -200 <= self.rect.y <= HEIGHT:
            self.kill()

    def update(self):
        self.move()
        self.animation(self.images_for_animation, self.sym_x, self.sym_y, self.size_factor)
        self.check_dead()

class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, pos, dir=1, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load("img/projectiles/meatball_4.png").convert_alpha(), (16, 16))
        self.rect = self.image.get_rect(middleleft=pos)
        self.speed = 10
        self.dir = dir

    def update(self):
        self.rect.x += self.speed * self.dir
