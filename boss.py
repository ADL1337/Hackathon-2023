import pygame
from random import randint
from game_data import WIDTH, HEIGHT
from entity import MovableEntity

class Boss1(MovableEntity):
    def __init__(self, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.name = "Mafia Boss"
        self.mode = "Idle"
        self.live = 1000
        self.last_live = self.live
        self.image = pygame.transform.flip(self.image, False, True)
        self.last_ProjectileCreate = 0
        self.projectile_Timer = 2000
        self.images_Run = self.create_image_list("img/boss1/fuite/spr_pepperman_rolling_", 12)
        self.images_Jump = self.create_image_list("img/boss1/jump/spr_pepperman_jump_", 9)
        self.images_Hurt = self.create_image_list("img/boss1/hurt/spr_pepperman_scared_", 5)
        self.images_Idle = self.create_image_list(img_path, 12)
        self.time_hurting = 0
        self.pos_possibility = [0, 300, 600]
        self.time_last_dep = 0
        self.blinking_value = [(0,0,0), (128,128,128)]
        self.blinking = False

    def get_hurt(self):
        self.vect = pygame.math.Vector2(0, 0)
        self.time_hurting = pygame.time.get_ticks()
        self.mode = "Hurt"

    def hurt_animation(self):
        if not pygame.time.get_ticks() - self.time_hurting > 2000:
            self.animation(self.images_Hurt, True)
        else:
            self.vect = pygame.math.Vector2(1, 0)
            self.animation(self.images_Run, False)
            if self.rect.x > WIDTH:
                self.vect = pygame.math.Vector2(0, 0)
                if pygame.time.get_ticks() - self.time_hurting > 7000:
                    self.mode = "Coming"

    def get_dammage(self, player_boost):
        if self.mode == "Idle":
            self.live -= player_boost * 1
            self.image.fill(self.blinking_value[self.blinking], special_flags=pygame.BLEND_RGB_ADD)
            self.blinking = not self.blinking
        if self.live <= 0:
            self.dead_animation()
        if self.last_live - self.live > 500:
            self.get_hurt()

    def dead_animation(self):
        pass

    def graphe_animation(self):
        pass

    def change_pos(self):
        if pygame.time.get_ticks() - self.time_last_dep >= 3000:
            self.new_pos = self.pos_possibility[randint(0, len(self.pos_possibility)-1)]
            if self.new_pos != self.rect.y:
                self.vect = pygame.math.Vector2(0, 1)
                if self.new_pos < self.rect.y:
                    self.vect = pygame.math.Vector2(0, -1)
                self.mode = "Jump"
                self.state = 0

    def return_to_idle(self):
        self.state = 0
        self.vect = pygame.math.Vector2(0, 0)
        self.time_last_dep = pygame.time.get_ticks()
        self.mode = "Idle"

    def update(self):
        self.move()

        if self.mode == "Hurt":
            self.hurt_animation()

        elif self.mode == "Coming":
            self.vect = pygame.math.Vector2(-1, 0)
            self.animation(self.images_Run, True)
            if self.rect.x == 1000:
                self.return_to_idle()

        elif self.mode == "Jump":
            self.animation(self.images_Jump, True)
            if self.new_pos - self.rect.y == 0:
                self.return_to_idle()

        elif self.mode == "Idle":
            self.animation(self.images_Idle, True)
            self.change_pos()



