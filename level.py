import pygame
from projectile import *
from utils import CustomLoader
from player import Player
from boss import *
from plateform import Plateforme
from entity import *


class Level():
    def __init__(self, screen, player):
        self.visibles_sprites = pygame.sprite.Group()
        self.over_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.screen = screen
        self.player = player
        self.player_group.add(self.player)
        self.mortals_sprites = pygame.sprite.Group()
        self.touches = CustomLoader("res/config.json")
        self.player_shoot_sprites = pygame.sprite.Group()
        self.plateforms_sprites = pygame.sprite.Group()
        self.zone_number = 0
        self.zones = [[[], [], []]]
        self.mode = "InGame"
        self.phase = "Fight"
        self.win_pos = [[], [], [], []]
        self.win = None
        self.graph = None
        self.dialogue = None

    def create_plat(self, number):
        for plat_infos in self.zones[number]:
            plat = Plateforme(plat_infos, self.visibles_sprites, self.plateforms_sprites)

    def create_boss_proj(self):
        if self.boss.time_to_create_proj():
            proj = Projectile(self.boss.proj_stats, self.visibles_sprites, self.mortals_sprites)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if self.phase != "Dial":
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
        if keys[pygame.K_ESCAPE]:
            self.mode = "Pause"

        else:
            if keys[pygame.K_RETURN]:
                self.dialogue.kill()
                self.phase = "Fight"

    def check_change_level(self):
        if pygame.sprite.collide_mask(self.player, self.win) != None:
            if self.zone_number != 3:
                self.zone_number += 1
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
                if self.boss.mode == "Idle" or self.boss.mode == "Jump":
                    self.boss.hit_sound.play()
                    self.boss.get_dammage(True, pygame.time.get_ticks())

    def check_player_get_touch(self):
        for meat in self.mortals_sprites:
            if pygame.sprite.collide_mask(meat, self.player) != None:
                meat.kill()
                self.boss.kill()
                if self.zone_number == 3:
                    if self.graph != None:
                        self.graph.kill()
                        self.graph = None
                self.zone_number = 0
                self.load_new_zone()

    def load_new_zone(self):
        if self.graph != None:
            self.graph.kill()
        self.player.rect.center = 50, 200
        for plat in self.plateforms_sprites:
            plat.kill()
        for shoot in self.player_shoot_sprites:
            shoot.kill()
        for proj in self.mortals_sprites:
            proj.kill()
        self.create_plat(self.zone_number)
        if self.zone_number != 3:
            self.win = Door(self.win_pos[self.zone_number], "res/img/decors/change_level_door_", 0.5, self.visibles_sprites)
        elif self.zone_number == 3:
            self.boss = Boss1(["Jean-Michel", 1000], (0, 0), 5, (1100, 300), "res/img/boss1/idle/spr_pepperman_idle_",self.over_sprites)

class Level1(Level):
    def __init__(self, screen, player, zone_number):
        super().__init__(screen, player)
        self.zones = [[[100, 400, 200, 20], [300, 300, 150, 20], [900, 200, 100, 20]],
                      [[100, 400, 200, 20], [600, 300, 150, 20], [500, 200, 100, 20]],
                      [[100, 500, 200, 20], [200, 300, 150, 20], [500, 200, 100, 20]],
                      [[100, 400, 200, 20], [300, 300, 150, 20], [500, 200, 100, 20], [1120, 141, 120, 20],  [1120, 741, 120, 20], [1120, 442, 120, 20]]]
        self.win_pos = [[600, 600], [600, 600], [600, 600], [600, 600]]
        self.graph = None
        self.create_plat(self.zone_number)
        self.zone_number = zone_number
        self.load_new_zone()
        self.dialogue_cont = []

    def check_for_graph(self):
        if self.boss != None:
            if self.graph == None and self.boss.graph == "Ok":
                self.graph = Grafity(self.boss.images_Grafity, self.over_sprites)
            elif self.graph != None and self.boss.graph == "Die":
                self.graph.kill()
                self.graph = None

    def update(self):
        if self.win != None:
            self.check_change_level()

        if self.mode == "InGame":
            self.handle_input()
            if self.zone_number == 3:
                if self.phase == "Dial":
                    self.dialogue.update()
                    if self.dialogue.end:
                        self.phase = "Fight"
                        self.dialogue.kill()
                else:
                    self.check_for_graph()
                    self.create_boss_proj()
                    self.check_boss_get_shoot()
                    self.check_boss_dead()

        self.check_player_get_touch()
        self.over_sprites.update()
        self.visibles_sprites.update()
        self.player_shoot_sprites.update()
        self.player_group.update(self.plateforms_sprites)
        self.visibles_sprites.draw(self.screen)
        self.player_shoot_sprites.draw(self.screen)
        self.player_group.draw(self.screen)
        self.over_sprites.draw(self.screen)
