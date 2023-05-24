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

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(TITLE)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    font = pygame.font.SysFont("Arial", 24)
    picanto = pygame.image.load(f"img/boss1/dead/spr_pepperman_hurtplayer_0.png").convert_alpha()
    main_character = pygame.image.load(f"img/player/shoot/player_shoot_6.png").convert_alpha()
    characters_img = (main_character, picanto)
    dialog_text = [("Tes pouvoirs extraterrestres ne me font pas peur.\nJe suis la meilleure pizza de combat de tout l'univers et je compte bien le\n retrouver.", "Les pizzas ne sont pas les seules choses que je sais livrer.\nJe suis prêt à te servir une bonne leçon."), ("Tes pouvoirs extraterrestres ne me font pas peur.\nJe suis la meilleure pizza de combat de tout l'univers et je compte bien le\n retrouver.", "Les pizzas ne sont pas les seules choses que je sais livrer.\nJe suis prêt à te servir une bonne leçon.")]
    dialog = Dialog(dialog_text, characters_img, font)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((255, 255, 255))
        dialog.update(screen)
        pygame.display.update()
        clock.tick(60)