import pygame
import pygame.freetype

pygame.init()

# Initialisation de la police
pygame.freetype.init()
font = pygame.freetype.Font(None, 24)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

window_width = 800
window_height = 300
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pizza Vigilante")

# Héros principal
character_image = pygame.image.load("../main_character.png")
character_width = character_image.get_width()
character_height = character_image.get_height()

# Mafia boss
character_image = pygame.image.load("../main_character.png")
character_width = character_image.get_width()
character_height = character_image.get_height()

class DialogueBox:
    def __init__(self, x, y, width, height, message, next_dialogue=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.message = message
        self.next_dialogue = next_dialogue
        self.clicked = False

    def render(self):
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)

        text_surface, _ = font.render(self.message, BLACK)
        text_width, text_height = text_surface.get_size()
        text_x = self.x + (self.width - text_width) // 2
        text_y = self.y + (self.height - text_height) // 2

        window.blit(text_surface, (text_x, text_y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
                self.clicked = True

dialogue1 = DialogueBox(0, 0, 400, 200, "Vous : je m'appelle lieutnant croûte infernale et je vais t'arrêter aujourd'hui !", "dialogue2")
dialogue2 = DialogueBox(0, 0, 400, 200, "Mafia Boss : je suis le boss de la mafia et tu crois pouvoir m'arrêter ? Mouahahahahahahahaahahahahah", "dialogue3")
dialogue3 = DialogueBox(0, 0, 400, 200, "Vous : Oui car je suis gay !", "dialogue4")
dialogue4 = DialogueBox(0, 0, 400, 200, "Mafia Boss : Mouhahahahaha moi aussi je suis gay !", None)

current_dialogue = dialogue1
elapsed_time = 0
dialogue_delay = 3000

running = True
clock = pygame.time.Clock()
while running:
    clocktime = clock.tick(60)
    elapsed_time += clocktime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current_dialogue.handle_event(event)

    window.fill(GRAY)

    current_dialogue.render()

    window.blit(character_image, (window_width - character_width, window_height - character_height))

    if elapsed_time >= dialogue_delay:
        elapsed_time = 0
        if current_dialogue.next_dialogue:
            if current_dialogue.next_dialogue == "dialogue2":
                current_dialogue = dialogue2
            elif current_dialogue.next_dialogue == "dialogue3":
                current_dialogue = dialogue3
            elif current_dialogue.next_dialogue == "dialogue4":
                current_dialogue = dialogue4

    if current_dialogue.clicked and current_dialogue.next_dialogue:
        if current_dialogue.next_dialogue == "dialogue2":
            current_dialogue = dialogue2
        elif current_dialogue.next_dialogue == "dialogue3":
            current_dialogue = dialogue3
        elif current_dialogue.next_dialogue == "dialogue4":
            current_dialogue = dialogue4

    pygame.display.flip()

pygame.quit()
