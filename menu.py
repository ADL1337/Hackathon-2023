import pygame

from game_data import *
from utils import *


class Button(pygame.sprite.Sprite):
    def __init__(self, screen, pos, text, font, size=(BUTTON["width"], BUTTON["height"]), hover=True, callback=lambda: None):
        super().__init__()
        self.screen = screen
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center=pos)
        self.text = text
        self.font = font
        self.hover = hover
        self.callback = callback
    
    def update(self):
        if self.hover is True:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.surf.fill(BUTTON["hover_color"])
            else:
                self.surf.fill(BUTTON["bgcolor"])
        else:
            self.surf.fill(BUTTON["bgcolor"])
            
        self.screen.blit(self.surf, self.rect)
        draw_text(self.screen, self.text, self.font, self.rect.center, BUTTON["color"])

class TextBlob(pygame.sprite.Sprite):
    def __init__(self, screen, pos, text, font, size=(BUTTON["width"], BUTTON["height"])):
        super().__init__()
        self.screen = screen
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center=pos)
        self.text = text
        self.font = font
        self.callback = lambda: print("TextBlob has no callback")
    
    def update(self):
        self.surf.fill(BUTTON["bgcolor"])
        self.screen.blit(self.surf, self.rect)
        for i, line in enumerate(self.text.split("\n"), start=2):
            draw_text(self.screen, line, self.font, (self.rect.centerx, self.rect.top + i * FONT_SIZE), BUTTON["color"], True)



class Menu:
    config = CustomLoader(PATHS["config"])
    stats = CustomLoader(PATHS["stats"])
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(PATHS["font"], FONT_SIZE)
        self.main_buttons = pygame.sprite.Group()
        self.options_buttons = pygame.sprite.Group()
        self.volume_buttons = pygame.sprite.Group()
        self.hotkey_buttons = pygame.sprite.Group()
        self.statistics_buttons = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

        self.menu_stack = []

    # I LITERALLY REMADE TKINTER BUT WORSE
        self.main_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 - BUTTON["height"] - BUTTON["spacing"]), "Play", self.font, callback=lambda: "play"))
        self.main_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2), "Options", self.font, callback=lambda: "options"))
        self.main_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 + BUTTON["height"] + BUTTON["spacing"]), "Statistics", self.font, callback=lambda: "statistics"))
        self.main_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 + (BUTTON["height"] + BUTTON["spacing"]) * 2), "Quit", self.font, callback=lambda: "quit"))

        self.options_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 - BUTTON["height"] - BUTTON["spacing"]), "Volume", self.font, callback=lambda: "volume"))
        self.options_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2), "Hotkeys", self.font, callback=lambda: "hotkeys"))
        self.options_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 + BUTTON["height"] + BUTTON["spacing"]), "Back", self.font, callback=lambda: "back"))

        stats_pannel_size = (WIDTH // 3, HEIGHT // 3)
        self.statistics_buttons.add(TextBlob(self.screen, (WIDTH // 2, HEIGHT // 2), statistics_string(self.stats.data), self.font, size=stats_pannel_size))
        self.statistics_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 + stats_pannel_size[1]), "Back", self.font, callback=lambda: "back"))
    
    def run(self):
        background = pygame.transform.scale(pygame.image.load(RES_PATH + "menu_background.png").convert_alpha(), (WIDTH, HEIGHT))
        running = True
        self.menu_stack.append(self.main_menu)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in self.menu_buttons:
                            if button.rect.collidepoint(event.pos):
                                callback = button.callback()
                                print(callback)
                                if callback is None:
                                    pass
                                elif callback == "quit":
                                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                                elif callback == "back":
                                    self.menu_stack.pop()
                                else:
                                    if hasattr(self, callback + "_menu"):
                                        new_menu = getattr(self, callback + "_menu")
                                        self.menu_stack.append(new_menu)
                                    else:
                                        print("Error: Menu not implemented")
            
            self.screen.blit(background, (0, 0))
            self.menu_stack[-1]()
            self.menu_buttons.update()
            pygame.display.update()
            self.clock.tick(FPS)
    
    def main_menu(self):
        self.menu_buttons = self.main_buttons
    
    def options_menu(self):
        self.menu_buttons = self.options_buttons

    def statistics_menu(self):
        self.menu_buttons = self.statistics_buttons
