import pygame

from game_data import *
from menu import Menu, MenuPause
from level import *
from utils import CustomLoader, animate_endgame
from player import Player

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.menu = Menu(self.screen)
        self.mode = "Menu"
        self.player = Player((0, 1000))
        self.plateforms_group = pygame.sprite.Group()
        self.loader = CustomLoader("res/stats.json")
        self.pause_menu = None
        self.saver = CustomLoader("res/save.json")
        self.level_number = self.saver["level_number"]
        self.levels = [Level1]
        self.level = None
        self.menu_musique = pygame.mixer.Sound("res/song/The Perfect Girl (Instrumental) [8PQu-5TPlik].mp3")
        self.pause_musique = pygame.mixer.Sound("res/song/RED SUN IN THE SKY (EARRAPE).mp3")
        self.pause_trigger = pygame.mixer.Sound("res/song/Chinese explaining sound effect ⧸ Social credit speech [4iIBFIh0rxg].mp3")
        self.menu_musique.play(-1)
        self.time_pause_start = 0
        self.earrape_play = False
        self.end_screen = None


    def save_stat(self):
        self.loader["distance_travelled"] += int(self.player.distance_travelled / 100)
        self.loader["playtime"] += int(pygame.time.get_ticks())
        self.loader["death_count"] += int(self.player.dead_number)
        self.loader["shots_fired"] += int(self.player.shoot_number)
        self.loader["jump_count"] += int(self.player.jump_number)
        self.loader.save()

    def update(self):
        self.screen.fill("black")
        if self.level != None:
            self.screen.blit(pygame.transform.scale(self.level.bgs[self.level.zone_number], (1280, 780)), (0,0))
        if self.mode == "Menu":
            self.menu.update()
            if self.menu.play:
                self.mode = "Level"
                self.menu = None
                self.saver = CustomLoader("res/save.json")
                self.level_number = self.saver["level_number"]
                self.level = self.levels[self.level_number-1](self.screen, self.player, self.saver["level_zone"])
        elif self.mode == "Pause":
            if (not self.earrape_play) and pygame.time.get_ticks() - self.time_pause_start > 12800:
                self.pause_musique.play(-1)
                self.earrape_play = True
            self.pause_menu.update()
            if self.pause_menu.etat == "Quit":
                self.mode = "Quit"
            if self.pause_menu.etat == "Continue":
                self.mode = "Level"
                pygame.mixer.stop()
                self.level.mode = "InGame"
            if self.pause_menu.etat == "Save":
                self.saver["level_number"] = self.level_number
                self.saver["level_zone"] = self.level.zone_number
                self.saver.save()
                self.pause_menu.etat = "Continue"
        else: # En jeux
            if self.level.mode == "Pause" and self.mode != "Pause":
                self.pause_trigger.play()
                self.mode = "Pause"
                self.time_pause_start = pygame.time.get_ticks()
            if self.mode == "Level":
                self.level.update()
                if self.level.mode == "Pause":
                    self.pause_menu = MenuPause(self.screen)
                    self.pause_trigger.play()
                    self.mode = "Pause"
                    self.time_pause_start = pygame.time.get_ticks()
                if self.level.mode == "LevelEnd":
                    animate_endgame(self.screen, self.level.time_boss_dead)