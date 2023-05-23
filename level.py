import pygame

from projectile import Projectile
from utils import CustomLoader


class Level:
    def __init__(self, boss, screen, player):
        self.screen = screen
        self.boss = boss
        self.player = player
        self.visibles_sprites = pygame.sprite.Group(self.boss, self.player)
        self.mortals_sprites = pygame.sprite.Group()
        self.touches = CustomLoader("res/config.json")
        self.player_shoot_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

    def create_proj(self):
        if self.boss.time_to_create_proj():
            Projectile(self.boss.proj_stats, self.visibles_sprites, self.mortals_sprites)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.player.vect[0] = 1
        elif keys[pygame.K_LEFT]:
            self.player.vect[0] = -1
        else:
            self.player.vect[0] = 0

    def update(self):
        self.create_proj()
        self.handle_input()
        self.vertical_collision()
        self.horizontal_collision()
        self.visibles_sprites.update()
        self.visibles_sprites.draw(self.screen)
    
    def vertical_collision(self):
        collided_list = pygame.sprite.spritecollide(self.player, self.obstacle_sprites, False)
        for collision in collided_list:
            if self.player.gravity > 0:
                self.player.rect.bottom = collision.rect.top
                self.player.gravity = 0
                break
            elif self.player.vect[1] < 0:
                self.player.rect.top = collision.rect.bottom
                self.player.vect[1] = 0
                break

    def horizontal_collision(self):
        collided_list = pygame.sprite.spritecollide(self.player, self.obstacle_sprites, False)
        for collision in collided_list:
            if self.player.vect[0] > 0:
                self.player.rect.right = collision.rect.left
                self.player.vect[0] = 0
                break
            elif self.player.vect[0] < 0:
                self.player.rect.left = collision.rect.right
                self.player.vect[0] = 0
                break