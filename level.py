import pygame
from projectile import Projectile
from utils import CustomLoader
from player import Player
from boss import *
from plateform import Plateforme


class Level():
    def __init__(self, screen):
        self.visibles_sprites = pygame.sprite.Group()
        self.over_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.screen = screen
        self.player = Player((200, 200), self.player_group)
        self.boss = Boss1(["Jean-Michel", 1000], (0, 0), 5, (800, 300), "img/boss1/idle/spr_pepperman_idle_",self.visibles_sprites)
        self.mortals_sprites = pygame.sprite.Group()
        self.touches = CustomLoader("res/config.json")
        self.player_shoot_sprites = pygame.sprite.Group()
        self.plateforms_sprites = pygame.sprite.Group()
        self.zone_number = 0
        self.zones = [[[], [], []]]

    def create_plat(self, number):
        for plat_infos in self.zones[number]:
            plat = Plateforme(plat_infos, self.visibles_sprites, self.plateforms_sprites)

    def create_proj(self):
        if self.boss.time_to_create_proj():
            proj = Projectile(self.boss.proj_stats, self.visibles_sprites, self.mortals_sprites)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            pass
        elif keys[pygame.K_LEFT]:
            pass
        else:
            pass

    def update(self):
        self.create_proj()
        self.visibles_sprites.update()
        self.visibles_sprites.draw(self.screen)


class Level1(Level):
    def __init__(self, screen):
        super().__init__(screen)
        self.zones = [[[100, 400, 200, 20], [300, 300, 150, 20], [500, 200, 100, 20]]]
        self.graph = None

    def check_for_graph(self):
        pass

    def update(self):
        self.create_proj()
        self.player_group.update(self.plateforms_sprites)
        self.visibles_sprites.update()
        self.visibles_sprites.draw(self.screen)
        self.player_group.draw(self.screen)