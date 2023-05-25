import pygame
from random import randint
from game_data import WIDTH, HEIGHT
from entity import MovableEntity

class Boss(MovableEntity):
    def __init__(self, stats, vect_direct, speed, pos, img_path, *groups):
        super().__init__(vect_direct, speed, pos, img_path, *groups)
        self.last_ProjectileCreate = 0
        self.projectile_Timer = 2000
        self.name = stats[0]
        self.mode = "Idle"
        self.live = stats[1]
        self.last_live = self.live
        self.blinking_value = [(0,0,0), (128,128,128)]
        self.blinking = False
        self.proj_stats = [(1, 0), 10, (0, 0), "res/img/projectiles/meatball/meatball_", 12, False, False, 0.4]

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
        self.hitbox = pygame.mask.from_surface(self.image)
        self.time_hurting = 0
        self.pos_possibility = [0, 300, 600]
        self.time_last_dep = 0
        self.graph = None
        self.time_get_touch = 0
        self.images_Run = self.create_image_list("res/img/boss1/fuite/spr_pepperman_rolling_", 12)
        self.images_Jump = self.create_image_list("res/img/boss1/jump/spr_pepperman_jump_", 9)
        self.images_Hurt = self.create_image_list("res/img/boss1/hurt/spr_pepperman_scared_", 5)
        self.images_Fall = self.create_image_list("res/img/boss1/fall/spr_pepperman_groundpoundstart_", 6)
        self.images_Dead = self.create_image_list("res/img/boss1/dead/spr_pepperman_hurtplayer_", 3)
        self.images_Idle = self.create_image_list(img_path, 12)
        self.images_Make_Grafity = self.create_image_list("res/img/boss1/make_grafiti/spr_peppermanvengeful_", 3)
        self.images_Grafity = self.create_image_list("res/img/boss1/grafiti/grafiti_", 4)
        self.hit_sound = pygame.mixer.Sound("res/song/Vine-boom-sound-effect.mp3")
        self.hurt_sound = pygame.mixer.Sound("res/song/Social-credit-siren-sound-effect.mp3")
        self.dial_end = False
        self.timer_touch = 0

    def get_hurt(self):
        self.projectile_Timer -= 500
        self.proj_stats[1] += 5
        self.last_live = self.live
        self.vect = pygame.math.Vector2(0, 0)
        self.time_hurting = pygame.time.get_ticks()
        self.hurt_sound.play()
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

    def get_dammage(self, player_boost, timer):
        # A appeller lors de la collision entre le projectile du joueur et le boss (prend en entrée un boolean qui indique si l'arme du joueur est sous l'effet d'un boost de dégat)
        if timer - self.time_get_touch > 200:
            deg = 20
            if player_boost:
                deg = int(deg * 2)
            if self.mode == "Jump":
                deg = int(deg/2)
            self.live -= deg
            self.time_get_touch = timer
            if not self.blinking:
                self.blinking = True
                self.timer_touch = pygame.time.get_ticks()

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
        if self.blinking:
            if pygame.time.get_ticks() - self.timer_touch > 50:
                self.blinking = False
        if self.mode == "Hurt":
            self.hurt_animation()
        elif self.mode == "Coming":
            self.vect = pygame.math.Vector2(-1, 0)
            self.animation(self.images_Run, True, False, 1)
            if self.rect.x == 1100:
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
            if self.dial_end:
                self.change_pos()
        elif self.mode == "Dead":
            self.state = 0
            self.animation(self.images_Dead, True, False, 1)
        elif self.mode == "Graph":
            self.graphe_animation()
            self.animation(self.images_Make_Grafity, False, False, 1)
        self.image.fill(self.blinking_value[self.blinking], special_flags=pygame.BLEND_RGB_ADD)

class Grafity(pygame.sprite.Sprite):
    def __init__(self, skins, *groups):
        super().__init__(*groups)
        skin = skins[randint(0, len(skins)-1)]
        self.image = pygame.transform.scale_by(pygame.image.load(skin).convert_alpha(), 1.5)
        self.rect = self.image.get_rect(topleft=(self.get_new_pos()))

    def get_new_pos(self):
        x = randint(0, 700)
        y = randint(0, 300)
        return x, y

class Door(pygame.sprite.Sprite):
    def __init__(self, pos, img_path, size_factor, *groups): #img_path = chemin de l'image sans le 'numéro.png'
        super().__init__(*groups)
        self.image = pygame.transform.scale_by(pygame.image.load(img_path+"0.png").convert_alpha(), 0.5) #Prend au départ la première ou la seule image de la collection
        self.hitbox = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
