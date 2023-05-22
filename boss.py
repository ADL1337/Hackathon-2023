import pygame
from game_data import WIDTH, HEIGHT
from entity import MovableEntity
from projectile import Projectile

class Boss(MovableEntity):
    def __init__(self, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.state = 0

    def create_image_liste(self, patch, limit):
        listes = []
        for i in range(0, limit):
            listes.append(patch+str(i)+".png")
        return listes

class Boss1(Boss):
    def __init__(self, proj_img_path, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.name = "Mafia Boss"
        self.mode = "Idle"
        self.proj_img_path = proj_img_path
        self.last_ProjectileCreate = 0
        self.projectile_Timer = 2000
        self.projectile_Group = pygame.sprite.Group()
        self.images_Run = self.create_image_liste("img/boss1/fuite/spr_pepperman_rolling_", 12)
        self.images_Jump = self.create_image_liste("img/boss1/jump/spr_pepperman_jump_", 9)
        self.images_Hurt = self.create_image_liste("img/boss1/hurt/spr_pepperman_scared_", 5)
        self.images_Idle = self.create_image_liste("img/boss1/idle/spr_pepperman_idle_", 12)

    def create_projectile(self):
        proj = Projectile(1, (-1, 0), 5, (WIDTH + 100), self.proj_img_path, self.projectile_Group)

    def idle_animation(self):
        self.image = pygame.image.load(self.images_Idle[self.state]).convert()
        self.state += 1
        if self.state > 11:
            self.state = 0

    def fuite_animation(self):
        self.move()
        self.image = pygame.image.load(self.images_Run[self.state]).convert()
        self.state += 1
        if self.state > 11:
            self.state = 0

    def jump_animation(self):
        self.move()
        self.image = pygame.image.load(self.images_Jump[self.state]).convert()
        self.state += 1
        if self.state > 8:
            self.state = 0

    def take_dammage_animation(self):
        self.image = pygame.image.load(self.images_Hurt[self.state]).convert()
        self.state += 1
        if self.state > 4:
            self.state = 0

    def update(self):
        if self.mode == "Hurt":
            self.vect = (0, 0)
            self.take_dammage_animation()
        elif self.mode == "Fuite":
            self.vect = (1, 0)
            self.fuite_animation()
        elif self.mode == "Jump":
            self.vect = (0, -1)
            self.jump_animation()
        elif self.mode == "Idle":
            self.vect = (0, 0)
            self.idle_animation()

class Boss2(Boss):
    def __init__(self, proj_img_path, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.name = "Tchad Pillar"
        self.mode = "Idle"
        self.proj_img_path = proj_img_path
        self.last_ProjectileCreate = 0
        self.projectile_Timer = 2000
        self.projectile_Group = pygame.sprite.Group()
        self.images_Hurt = self.create_image_liste("img/boss2/hurt/)  #DEVOIR SEPARER LES TILES SHEET AVEC UNE CLASSE
        self.images_Idle = self.create_image_liste("img/boss2/idle/)

    def create_projectile(self):
        proj = Projectile(1, (-1, 0), 5, (WIDTH + 100), self.proj_img_path, self.projectile_Group)

    def idle_animation(self):
        self.image = pygame.image.load(self.images_Idle[self.state]).convert()
        self.state += 1
        if self.state > 11:
            self.state = 0

    def take_dammage_animation(self):
        self.image = pygame.image.load(self.images_Hurt[self.state]).convert()
        self.state += 1
        if self.state > 4:
            self.state = 0

    def update(self):
        if self.mode == "Hurt":
            self.vect = (0, 0)
            self.take_dammage_animation()
        elif self.mode == "Idle":
            self.vect = (0, 0)
            self.idle_animation()