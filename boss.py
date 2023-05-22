import pygame
from entity import MovableEntity
from projectile import Projectile

class Boss(MovableEntity):
    def __init__(self, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)

class Boss1(Boss):
    def __init__(self, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.name = "Kaaris"
        self.mode = "Idle"
        self.state = 0
        self.last_ProjectileCreate = 0
        self.projectile_Timer = 2000
        self.projectile_Group = pygame.sprite.Group()
        self.images_Run = []
        self.images_Jump = []
        self.images_Hurt = []
        self.images_Idle = []
        self.iniatlize()

    def create_projectile(self):
        proj = Projectile(1, (-1, 0), 5, (WIDTH + 100), img_path, self.projectile_Group)

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

    def iniatlize(self):
        for i in range(0, 12):
            self.images_Run.append("img/boss1/fuite/spr_pepperman_rolling_"+str(i)+".png")
        for i in range(0, 9):
            self.images_Jump.append("img/boss1/jump/spr_pepperman_jump_"+str(i)+".png")
        for i in range(0, 5):
            self.images_Hurt.append("img/boss1/hurt/spr_pepperman_scared_"+str(i)+".png")
        for i in range(0, 12):
            self.images_Idle.append("img/boss1/idle/spr_pepperman_idle_"+str(i)+".png")

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
