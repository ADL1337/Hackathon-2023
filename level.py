import pygame
from projectile import *
from utils import CustomLoader
from player import Player
from boss import *
from plateform import Plateforme
from entity import *


class Level():
    def __init__(self, screen):
        self.visibles_sprites = pygame.sprite.Group()
        self.over_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.screen = screen
        self.player = Player((200, 200), self.player_group)
        self.mortals_sprites = pygame.sprite.Group()
        self.touches = CustomLoader("res/config.json")
        self.player_shoot_sprites = pygame.sprite.Group()
        self.plateforms_sprites = pygame.sprite.Group()
        self.zone_number = 0
        self.zones = [[[], [], []]]
        self.mode = "InGame"
        self.win_pos = [[], [], [], []]
        self.win = None

    def create_plat(self, number):
        for plat_infos in self.zones[number]:
            plat = Plateforme(plat_infos, self.visibles_sprites, self.plateforms_sprites)

    def create_boss_proj(self):
        if self.boss.time_to_create_proj():
            proj = Projectile(self.boss.proj_stats, self.visibles_sprites, self.mortals_sprites)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.player.run("right")
        elif keys[pygame.K_q]:
            self.player.run("left")
        else:
            self.player.run("stop")
        if keys[pygame.K_SPACE]:
            self.player.jump()
        if keys[pygame.K_e]:
            proj = self.player.shoot()
            if isinstance(proj, PlayerProjectile):
                self.player_shoot_sprites.add(proj)

    def check_change_level(self):
        if pygame.sprite.collide_mask(self.player, self.win) != None:
            if self.zone_number != 3:
                self.zone_number += 1
                self.player.rect.center = 100, 200
                self.win.kill()
                self.load_new_zone()
            else:
                self.mode = "LevelEnd"

    def check_boss_dead(self):
        if self.boss.live <= 0:
            self.win = Door(self.win_pos[self.zone_number], "res/img/boss1/boss_1_door_", 0.5, self.visibles_sprites)

    def check_boss_get_shoot(self):
        for shoot in self.player_shoot_sprites:
            if pygame.sprite.collide_mask(shoot, self.boss) != None:
                shoot.kill()
                self.boss.get_dammage(False, pygame.time.get_ticks())

    def check_player_get_touch(self):
        for meat in self.mortals_sprites:
            if pygame.sprite.collide_mask(meat, self.player) != None:
                meat.kill()
                self.mode = "GameOver"

    def load_new_zone(self):
        for plat in self.plateforms_sprites:
            plat.kill()
        for shoot in self.player_shoot_sprites:
            shoot.kill()
        self.create_plat(self.zone_number)
        if self.zone_number != 3:
            self.win = Door(self.win_pos[self.zone_number], "res/img/decors/change_level_door_", 0.5, self.visibles_sprites)
        elif self.zone_number == 3:
            self.boss = Boss1(["Jean-Michel", 1000], (0, 0), 5, (800, 300), "res/img/boss1/idle/spr_pepperman_idle_",self.visibles_sprites)

class Level1(Level):
    def __init__(self, screen, zone_number):
        super().__init__(screen)
        self.zones = [[[100, 400, 200, 20], [300, 300, 150, 20], [500, 200, 100, 20]], [[100, 400, 200, 20], [300, 300, 150, 20], [500, 200, 100, 20]], [[100, 400, 200, 20], [300, 300, 150, 20], [500, 200, 100, 20]], [[100, 400, 200, 20], [300, 300, 150, 20], [500, 200, 100, 20]]]
        self.win_pos = [[600, 600], [600, 600], [600, 600], [600, 600]]
        self.graph = None
        self.create_plat(self.zone_number)
        self.zone_number = zone_number
        self.load_new_zone()

    def check_for_graph(self):
        if self.boss != None:
            if self.graph == None and self.boss.graph == "Ok":
                self.graph = Grafity(self.boss.images_Grafity[0], self.over_sprites)
            elif self.graph != None and self.boss.graph == "Die":
                self.graph.kill()

    def update(self):
        self.check_change_level()
        if self.mode == "InGame":
            self.handle_input()
            if self.zone_number == 3:
                self.check_for_graph()
                self.create_boss_proj()
                self.check_boss_get_shoot()
                self.check_boss_dead()
        self.over_sprites.update()
        self.visibles_sprites.update()
        self.player_shoot_sprites.update()
        self.player_group.update(self.plateforms_sprites)
        self.visibles_sprites.draw(self.screen)
        self.player_shoot_sprites.draw(self.screen)
        self.player_group.draw(self.screen)
        self.over_sprites.draw(self.screen)
