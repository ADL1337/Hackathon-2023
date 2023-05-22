import pygame
from random import randint
from game_data import WIDTH, HEIGHT
from entity import MovableEntity

class Boss1(MovableEntity):
    def __init__(self, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.name = "Mafia Boss"
        self.mode = "Hurt"
        self.live = 1000
        self.last_live = self.live
        self.image = pygame.transform.flip(self.image, True, False)
        self.last_ProjectileCreate = 0
        self.projectile_Timer = 2000
        self.time_hurting = 0
        self.pos_possibility = [0, 300, 600]
        self.time_last_dep = 0
        self.blinking_value = [(0,0,0), (128,128,128)]
        self.blinking = False
        self.graph = None

        self.images_Run = self.create_image_list("img/boss1/fuite/spr_pepperman_rolling_", 12)
        self.images_Jump = self.create_image_list("img/boss1/jump/spr_pepperman_jump_", 9)
        self.images_Hurt = self.create_image_list("img/boss1/hurt/spr_pepperman_scared_", 5)
        self.images_Fall = self.create_image_list("img/boss1/fall/spr_pepperman_groundpoundstart_", 6)
        self.images_Dead = self.create_image_list("img/boss1/dead/spr_pepperman_hurtplayer_", 3)
        self.images_Idle = self.create_image_list(img_path, 12)
        self.images_Make_Grafity = self.create_image_list("img/boss1/make_grafiti/spr_peppermanvengeful_", 3)
        self.images_Grafity = self.create_image_list("img/boss1/grafiti/grafiti_", 5)

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
                self.mode = "Graph"
                self.graph = Grafity(self.images_Grafity[randint(0, len(self.images_Grafity)-1)])
                self.state = 0

    def get_dammage(self, player_boost):
        if self.mode == "Idle":
            self.live -= player_boost * 1
            self.image.fill(self.blinking_value[self.blinking], special_flags=pygame.BLEND_RGB_ADD)
            self.blinking = not self.blinking
        if self.live <= 0:
            self.mode = "Dead"
        if self.last_live - self.live > 500:
            self.get_hurt()

    def graphe_animation(self):
        if 6500 <= pygame.time.get_ticks() - self.time_hurting < 12000:
            self.rect.x, self.rect.y = WIDTH, self.pos_possibility[randint(0, len(self.pos_possibility)-1)]
            self.graph.update()
        if pygame.time.get_ticks() - self.time_hurting >= 12000:
            self.graph.kill()
            self.mode = "Coming"

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
            if self.vect[1] == -1:
                self.animation(self.images_Jump, True)
            else:
                self.animation(self.images_Fall, True)
            if self.new_pos - self.rect.y == 0:
                self.return_to_idle()

        elif self.mode == "Idle":
            self.animation(self.images_Idle, True)
            self.change_pos()

        elif self.mode == "Dead":
            self.animation(self.images_Dead, True)

        elif self.mode == "Graph":
            self.graphe_animation()
            if pygame.time.get_ticks() - self.time_hurting < 6500:
                self.rect = self.image.get_rect(topleft=(0, 0))
                self.animation(self.images_Make_Grafity, False)

class Grafity(pygame.sprite.Sprite):
    def __init__(self, skin):
        super().__init__()
        self.image = pygame.image.load(skin).convert_alpha()
        self.rect = self.image.get_rect(topleft=(0,0))

    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect)
