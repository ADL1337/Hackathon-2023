import pygame

from game_data import *
from utils import draw_text

class Dialog(pygame.sprite.Sprite):
    def __init__(self, text_list, characters_img, font):
        super().__init__()
        self.surf = pygame.Surface((800, 80))
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT - 100))
        self.text = text_list
        self.current_phase = 0
        self.current_character = 0
        self.characters_img = characters_img
        self.max_phases = len(text_list)
        self.is_end = False
        self.current_text = ""
        self.last_show = pygame.time.get_ticks()
        self.wait_time = 5000
        self.font = font
        self.bgcolor = (128, 128, 128)
        self.surf.fill(self.bgcolor)
        self.sound = pygame.mixer.Sound("res/song/abou_bakr.mp3")

    def update(self, screen):
        if self.current_phase < self.max_phases:
            screen.blit(self.surf, self.rect)
            current_text = self.text[self.current_phase][self.current_character].split("\n")
            for i, line in enumerate(current_text):
                draw_text(screen, line, self.font, (self.rect.left, self.rect.top + i*DIALOG_FONTSIZE), (0, 0, 0), False)
            screen.blit(self.characters_img[self.current_character], (self.rect.left - 150, self.rect.top - 80))
            if  self.last_show + self.wait_time < pygame.time.get_ticks():
                self.last_show = pygame.time.get_ticks()
                self.current_character += 1
                if self.current_character > 1:
                    self.current_character = 0
                    self.current_phase += 1
        else:
            self.is_end = True
