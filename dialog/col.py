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

# Initialisation de la fenêtre
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dialogue entre personnages")

# Classe pour la boîte de dialogue
class DialogueBox:
    def __init__(self, x, y, width, height, message):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.message = message

    def render(self):
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)

        text_surface, _ = font.render(self.message, BLACK)
        text_width, text_height = text_surface.get_size()
        text_x = self.x + (self.width - text_width) // 2
        text_y = self.y + (self.height - text_height) // 2

        window.blit(text_surface, (text_x, text_y))

# Création des dialogues
dialogue1 = DialogueBox(100, 200, 600, 100, "Personnage 1: Salut ! Comment ça va ?")
dialogue2 = DialogueBox(100, 300, 600, 100, "Personnage 2: Ça va bien, merci ! Et toi ?")
dialogue3 = DialogueBox(100, 400, 600, 100, "Personnage 1: Je vais bien aussi, merci !")

# Liste des dialogues
dialogues = [dialogue1, dialogue2, dialogue3]

# Dialogue actuel
current_dialogue_index = 0

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(GRAY)

    # Affichage du dialogue actuel
    dialogues[current_dialogue_index].render()

    pygame.display.flip()

    # Passage au dialogue suivant avec la touche Entrée
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        current_dialogue_index += 1
        if current_dialogue_index >= len(dialogues):
            running = False

pygame.quit()