import pygame

from game_data import *
from utils import *
from utils import CustomLoader


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

        self.background = pygame.transform.scale(pygame.image.load(RES_PATH + "img/menu_background.png").convert_alpha(), (WIDTH, HEIGHT))
        self.game_title = pygame.image.load(RES_PATH + "img/game_title.png").convert_alpha()
        self.font = pygame.font.Font("res/font/game_font.TTF", FONT_SIZE)

        self.background = pygame.transform.scale(pygame.image.load(RES_PATH + "img/menu_background.png").convert_alpha(), (WIDTH, HEIGHT))
        self.game_title = pygame.image.load(PATHS["img"] + "game_title.png").convert_alpha()
        self.font = pygame.font.Font(PATHS["font"], FONT_SIZE)

        self.main_buttons = pygame.sprite.Group()
        self.options_buttons = pygame.sprite.Group()
        self.volume_buttons = pygame.sprite.Group()
        self.hotkey_buttons = pygame.sprite.Group()
        self.reprendre_buttons = pygame.sprite.Group()
        self.statistics_buttons = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.menu_buttons = self.main_buttons
        self.play = False
        self.menu_stack = []

    # I LITERALLY REMADE TKINTER BUT WORSE
        self.main_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 - BUTTON["height"] - BUTTON["spacing"]), "Play", self.font, callback=lambda: "play"))
        self.main_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2), "Options", self.font, callback=lambda: "options"))
        self.main_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 + BUTTON["height"] + BUTTON["spacing"]), "Statistics", self.font, callback=lambda: "statistics"))
        self.main_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 + (BUTTON["height"] + BUTTON["spacing"]) * 2), "Quit", self.font, callback=lambda: "quit"))

        self.options_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 - BUTTON["height"] - BUTTON["spacing"]), "Volume", self.font, callback=lambda: "volume"))
        self.options_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2), "Hotkeys", self.font, callback=lambda: "hotkeys"))
        self.options_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 + BUTTON["height"] + BUTTON["spacing"]), "Back", self.font, callback=lambda: "back"))

        self.reprendre_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 - BUTTON["height"] - BUTTON["spacing"]), "Continue", self.font, callback=lambda: "continue"))
        self.reprendre_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2), "New Partie", self.font, callback=lambda: "reset"))
        self.reprendre_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 + BUTTON["height"] + BUTTON["spacing"]), "Back", self.font, callback=lambda: "back"))

        stats_pannel_size = (WIDTH // 3, HEIGHT // 3)
        self.statistics_buttons.add(TextBlob(self.screen, (WIDTH // 2, HEIGHT // 2), statistics_string(self.stats.data), self.font, size=stats_pannel_size))
        self.statistics_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 + stats_pannel_size[1]), "Back", self.font, callback=lambda: "back"))

    def check_event(self, event):
        for button in self.menu_buttons:
            if button.rect.collidepoint(event.pos):
                callback = button.callback()
                print(callback)
                if callback is None:
                    pass
                elif callback == "play":
                    self.menu_buttons = self.reprendre_buttons
                    self.menu_stack.append(self.main_buttons)
                elif callback == "continue":
                    self.play = True
                elif callback == "reset":
                    saver = CustomLoader("res/save.json")
                    saver["level_number"] = 1
                    saver["level_zone"] = 0
                    saver.save()
                    self.play = True
                elif callback == "quit":
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif callback == "back":
                    self.menu_buttons = self.menu_stack[-1]
                    self.menu_stack.pop()
                elif callback == "statistics":
                    self.menu_buttons = self.statistics_buttons
                    self.menu_stack.append(self.main_buttons)
                elif callback == "options":
                    self.menu_buttons = self.options_buttons
                    self.menu_stack.append(self.main_buttons)
                elif callback == "volume":
                    print("Option pas encore disponible")
                else:
                    if hasattr(self, callback + "_menu"):
                        new_menu = getattr(self, callback + "_menu")
                        self.menu_stack.append(new_menu)
                    else:
                        print("Error: Menu not implemented")

    def update(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.game_title, (WIDTH // 2 - self.game_title.get_width() // 2, 0))
        self.menu_buttons.update()
    
    def main_menu(self):
        self.menu_buttons = self.main_buttons
    
    def options_menu(self):
        self.menu_buttons = self.options_buttons

    def statistics_menu(self):
        self.menu_buttons = self.statistics_buttons

class MenuPause:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(PATHS["font"], FONT_SIZE)
        self.main_buttons = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.etat = "InPlace"

        # I LITERALLY REMADE TKINTER BUT WORSE
        self.main_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 - BUTTON["height"] - BUTTON["spacing"]), "Continuer", self.font, callback=lambda: "continue"))
        self.main_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2), "Sauvegarder", self.font, callback=lambda: "save"))
        self.main_buttons.add(Button(self.screen, (WIDTH // 2, HEIGHT // 2 + BUTTON["height"] + BUTTON["spacing"]), "Quitter", self.font, callback=lambda: "quit"))

    def check_event(self, event):
        for button in self.main_buttons:
            if button.rect.collidepoint(event.pos):
                callback = button.callback()
                print(callback)
                if callback == "continue":
                    self.etat = "Continue"
                elif callback == "save":
                    self.etat = "Save"
                elif callback == "quit":
                    self.etat = "Quit"
                else:
                    print("Error: Menu not implemented")

    def update(self):
        background = pygame.transform.scale(pygame.image.load(RES_PATH + "menu_background.png").convert_alpha(),
                                            (WIDTH, HEIGHT))
        self.screen.blit(background, (0, 0))
        self.main_buttons.update()
