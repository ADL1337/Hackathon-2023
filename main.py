import pygame
import time

pygame.init()

# Dimensions de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ecran de chargement")

# Couleurs
background_color = (255, 255, 255)
bar_color = (0, 0, 255)
text_color = (0, 0, 0)

# Police de caractères
font = pygame.font.Font(None, 36)

# Variables de jeu
game_running = False
loading_progress = 0

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Touche "Entrée"
                game_running = True

    # Si le jeu est en cours d'exécution, quitter la boucle principale du chargement
    if game_running:
        running = False

    # Effacer l'écran
    screen.fill(background_color)

    # Dessiner le texte
    text = font.render("Chargement en cours...", True, text_color)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(text, text_rect)

    # Dessiner la barre de chargement
    pygame.draw.rect(screen, bar_color, (screen_width // 4, screen_height // 2, loading_progress, 25))

    # Mettre à jour l'écran
    pygame.display.flip()

    # Mettre à jour la progression de chargement
    loading_progress += 10
    if loading_progress > screen_width // 2:
        loading_progress = 0

    # Temps de pause (simule le chargement)
    time.sleep(0.5)

# Boucle du jeu
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Mettre ici votre logique de jeu
    # ...

    # Effacer l'écran du jeu
    screen.fill(background_color)

    # Dessiner les éléments du jeu
    # ...

    # Mettre à jour l'écran du jeu
    pygame.display.flip()

# Quitter Pygame
pygame.quit()