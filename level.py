import pygame
from projectile import *
from utils import CustomLoader
from player import Player
from boss import *
from plateform import Plateforme
from entity import *
from dialog import Dialog


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
        self.dialogue_cont = []
        self.dial_font = pygame.font.SysFont("Arial", 24)
        self.dial_img = ()
        self.time_last_pause = 0
        self.boss = None

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
            if pygame.time.get_ticks() - self.time_last_pause > 1500:
                self.mode = "Pause"
                self.time_last_pause = pygame.time.get_ticks()

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

    def player_dead(self):
        self.player.dead_number += 1
        if self.boss != None:
            self.boss.kill()
            self.boss = None
        if self.dialogue != None:
            self.dialogue.kill()
        if self.graph != None:
            self.graph.kill()
            self.graph = None
        self.zone_number = 0
        self.load_new_zone()

    def check_player_outside(self):
        if not -200 <= self.player.rect.x <= WIDTH or not -200 <= self.player.rect.y <= HEIGHT:
            self.player_dead()

    def check_player_get_touch(self):
        for meat in self.mortals_sprites:
            if pygame.sprite.collide_mask(meat, self.player) != None:
                meat.kill()
                self.player_dead()

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
            self.phase = "Dial"
            self.dialogue = Dialog(self.dialogue_cont, self.dial_img, self.dial_font)
            self.dialogue.sound.play()
            self.boss = Boss1(["Jean-Michel", 1000], (0, 0), 5, (1100, 300), "res/img/boss1/idle/spr_pepperman_idle_",self.over_sprites)

class Level1(Level):
    def __init__(self, screen, player, zone_number):
        super().__init__(screen, player)
        self.zones = [[[100, 400, 200, 20], [300, 300, 150, 20], [900, 200, 100, 20]],
                      [[100, 400, 200, 20], [600, 300, 150, 20], [500, 200, 100, 20]],
                      [[100, 500, 200, 20], [200, 300, 150, 20], [500, 200, 100, 20]],
                      [[0, 400, 200, 20], [300, 300, 150, 20], [500, 200, 100, 20], [1120, 141, 120, 20],  [1120, 741, 120, 20], [1120, 442, 120, 20]]]
        self.win_pos = [[600, 600], [600, 600], [600, 600], [600, 600]]
        self.graph = None
        self.create_plat(self.zone_number)
        self.zone_number = zone_number
        self.load_new_zone()
        self.dialogue_cont = [("Hé, Piquanto ! Prêt à te faire mettre K.O ?", "Ha ! Tu penses vraiment pouvoir entrer sur mon territoire comme ça ?"), ("Je vais te montrer qu’à l’armée on n’est pas des zoulettes !","Sache que tu ne fais pas le poids contre moi."), (" Ne sois pas si sûr de toi ! je vais te faire mordre la poussière avant \n même que tu ne le réalises.","Fais de ton mieux. Mais je vais te montrer ce que signifie vraiment \n avoir du cran."), ("Les pizzas ne sont pas les seules choses que je sais livrer. Je suis prêt à \n te servir une bonne leçon.","Tu te surestimes. Tu n'as aucune idée de ce qui t'attend, je ne ferai \n aucune exception pour toi."), ("Je me battrai jusqu'à mon dernier souffle. Prépare-toi à sentir la \n transpiration de mes couilles !","Tant de paroles, mais seuls les actes comptent. Et crois-moi, je vais te \n montrer ce que signifie être un véritable chef de la mafia."), (" Je ne reculerai pas, j'ai l'honneur de mon côté et je me battrai avec \n bravoure.","Prépare-toi à être vaincu par le meilleur pizzaïolo soldat !"), ("On verra bien qui sortira vainqueur de ce combat.","Nous verrons, que le duel commence ! J’arrive te sauver Peppino Spaghetti !")]
        self.dial_img = (pygame.image.load("res/img/boss1/hurt/spr_pepperman_scared_0.png"), pygame.image.load("res/img/boss1/dead/spr_pepperman_hurtplayer_0.png"))

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
            self.check_player_outside()
            if self.zone_number == 3:
                if self.phase == "Dial":
                    self.player.run("stop")
                    self.dialogue.update(self.screen)
                    if self.dialogue.is_end:
                        self.boss.dial_end = True
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
