import pygame
from projectile import Projectile
from res

class Level():
    def __init__(self, boss, screen):
        self.screen = screen
        self.boss = boss
        self.visibles_sprites = pygame.sprite.Group()
        self.mortals_sprites = pygame.sprite.Group()

    def create_proj(self):
        if self.boss.time_to_create_proj():
            proj = Projectile(self.boss.proj_stats, self.visibles_sprites, self.mortals_sprites)

    def handle_input(self):
        pass

    def update(self):
        self.create_proj()
        self.visibles_sprites.update()
        self.visibles_sprites.draw(self.screen)
