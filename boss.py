import pygame
from random import randint
from game_data import WIDTH, HEIGHT
from entity import MovableEntity

class Boss(MovableEntity):
    def __init__(self, stats, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.last_ProjectileCreate = 0
        self.projectile_Timer = 2500
        self.name = stats[0]
        self.mode = "Idle"
        self.live = stats[1]
        self.last_live = self.live
        self.blinking_value = [(0,0,0), (128,128,128)]
        self.blinking = False
        self.proj_stats = [(1, 0), 5, (0, 0), "img/projectiles/meatball/meatball_", 12, False, False, 0.5]

    def time_to_create_proj(self):
        # A assembler avec une fonction dans le main qui check si la sortie est True, si oui crée un projectiles avec comme entrée boss.proj_stats
        if pygame.time.get_ticks() - self.last_ProjectileCreate >= self.projectile_Timer:
            self.last_ProjectileCreate = pygame.time.get_ticks()
            nbre = randint(0, 3)
            match nbre:
                case 0:
                    self.proj_stats[2] = (-100, randint(0, HEIGHT-50))
                    self.proj_stats[0] = (1, 0)
                case 1:
                    self.proj_stats[2] = (WIDTH, randint(0, HEIGHT - 50))
                    self.proj_stats[0] = (-1, 0)
                case 2:
                    self.proj_stats[2] = (randint(0, WIDTH-50), -50)
                    self.proj_stats[0] = (0, 1)
                case 3:
                    self.proj_stats[2] = (randint(0, WIDTH-50), HEIGHT)
                    self.proj_stats[0] = (0, -1)
            return True

class Boss1(Boss):
    def __init__(self, stats, vect_direct, speed, pos, img_path, *groups):
        super().__init__(stats, vect_direct, speed, pos, img_path, *groups)
        self.image = pygame.transform.flip(self.image, True, False)
        self.time_hurting = 0
        self.pos_possibility = [0, 300, 600]
        self.time_last_dep = 0
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
        self.projectile_Timer -= 500
        self.proj_stats[1] += 5
        self.last_live = self.live
        self.vect = pygame.math.Vector2(0, 0)
        self.time_hurting = pygame.time.get_ticks()
        self.mode = "Hurt"

    def hurt_animation(self):
        if not pygame.time.get_ticks() - self.time_hurting > 2000:
            self.animation(self.images_Hurt, True, False, 1)
        else:
            self.vect = pygame.math.Vector2(1, 0)
            self.animation(self.images_Run, False, False, 1)
            if self.rect.x > WIDTH:
                self.vect = pygame.math.Vector2(0, 0)
                self.mode = "Graph"
                self.state = 0
                self.time_hurting = pygame.time.get_ticks()

    def get_dammage(self, player_boost):
        # A appeller lors de la collision entre le projectile du joueur et le boss (prend en entrée un boolean qui indique si l'arme du joueur est sous l'effet d'un boost de dégat)
        if self.mode == "Idle":
            if player_boost:
                self.live -= 5
            else:
                self.live -= 1
            self.image.fill(self.blinking_value[self.blinking], special_flags=pygame.BLEND_RGB_ADD)
            self.blinking = not self.blinking
        if self.live <= 0:
            self.mode = "Dead"
        if self.last_live - self.live > 350:
            self.state = 0
            self.get_hurt()

    def graphe_animation(self):
        if pygame.time.get_ticks() - self.time_hurting >= 7000:
            self.graph = "Die"
            self.state = 0
            self.mode = "Coming"
        elif pygame.time.get_ticks() - self.time_hurting >= 1500:
            self.rect.x, self.rect.y = WIDTH, self.pos_possibility[randint(0, len(self.pos_possibility)-1)]
            self.graph = "Ok"
        elif pygame.time.get_ticks() - self.time_hurting >= 1000:
            self.rect.x, self.rect.y = 300,400
        elif pygame.time.get_ticks() - self.time_hurting >= 500:
            self.rect.x, self.rect.y = 800,500
        else:
            self.rect.x, self.rect.y = 100,100

    def change_pos(self):
        if pygame.time.get_ticks() - self.time_last_dep >= 3000:
            self.new_pos = self.pos_possibility[randint(0, len(self.pos_possibility)-1)]
            if self.new_pos != self.rect.y:
                self.vect = pygame.math.Vector2(0, 1)
                if self.new_pos < self.rect.y:
                    self.vect = pygame.math.Vector2(0, -1)
                self.state = 0
                self.mode = "Jump"

    def return_to_idle(self):
        self.vect = pygame.math.Vector2(0, 0)
        self.time_last_dep = pygame.time.get_ticks()
        self.state = 0
        self.mode = "Idle"

    def update(self):
        self.move()
        if self.mode == "Hurt":
            self.hurt_animation()
        elif self.mode == "Coming":
            self.vect = pygame.math.Vector2(-1, 0)
            self.animation(self.images_Run, True, False, 1)
            if self.rect.x == 1000:
                self.return_to_idle()
        elif self.mode == "Jump":
            if self.vect[1] == -1:
                self.animation(self.images_Jump, True, False, 1)
            else:
                self.animation(self.images_Fall, True, False, 1)
            if self.new_pos - self.rect.y == 0:
                self.return_to_idle()
        elif self.mode == "Idle":
            self.animation(self.images_Idle, True, False, 1)
            self.change_pos()
            # self.get_dammage(True) Pour test les dégats
        elif self.mode == "Dead":
            self.animation(self.images_Dead, True, False, 1)
        elif self.mode == "Graph":
            self.graphe_animation()
            self.animation(self.images_Make_Grafity, False, False, 1)

class Grafity(pygame.sprite.Sprite):
    def __init__(self, skin, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale_by(pygame.image.load(skin).convert_alpha(), 1.5)
        self.rect = self.image.get_rect(topleft=(self.get_new_pos()))

    def get_new_pos(self):
        x = randint(0, 700)
        y = randint(0, 300)
        return x, y

