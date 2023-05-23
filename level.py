import pygame
from projectile import Projectile

class Level():
    def __init__(self, boss):
        self.boss = boss
        self.visibles_sprites = pygame.sprite.Group()
        self.mortals_sprites = pygame.sprite.Group()

    def create_proj(self):
        if self.boss.time_to_create_proj():
            proj = Projectile(self.boss.stats, self.visibles_sprites, self.mortals_sprites)

