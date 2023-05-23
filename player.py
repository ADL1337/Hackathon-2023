import pygame
from entity import MovableEntity
from game_data import GRAVITY

class Player(MovableEntity):
    def __init__(self, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.boost = False
        self.images_idle = self.create_image_list("img/player/idle/player_idle_", 2)
        self.images_run = self.create_image_list("img/player/run/player_run_", 11)
        self.images_shoot = self.create_image_list("img/player/shoot/player_shoot_", 16)
        self.images_spawn = self.create_image_list("img/player/spawn/player_spawn_", 8)
        self.life = None
        self.proj_stats = [(1, 0), 5, (0, 0), "img/projectiles/meatball/meatball_", 12, False, False, 0.5]
        self.last_ProjectileCreate = 1000
        self.projectile_Timer = 1000
        self.left = False
        self.gravity = GRAVITY

    def run(self):
        if self.vect[0] != 0:
            if self.vect[0] == 1:
                self.left = False
            elif self.vect[0] == -1:
                self.left = True
            self.animation(self.images_run, self.left, False, 0.5)
        else:
            self.image = pygame.transform.scale_by(pygame.transform.flip(pygame.image.load("img/player/idle/player_idle_0.png"), self.left, False), 0.5)

    def shoot(self):
        if pygame.time.get_ticks() - self.last_ProjectileCreate >= self.projectile_Timer:
            self.last_ProjectileCreate = pygame.time.get_ticks()

    def jump(self):
        pass

    def take_dammage(self):
        pass

    def collision(self, obs):
        pass

    def update(self):
        self.move()
        self.run()
        self.gravity += GRAVITY
        print(self.gravity)
        self.rect.y += self.gravity