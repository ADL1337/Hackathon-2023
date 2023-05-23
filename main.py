import pygame

# Initialisation de Pygame
pygame.init()

# Définition de la taille de l'écran
largeur_ecran = 800
hauteur_ecran = 600
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Polices de caractères
police = pygame.font.SysFont("Arial", 24)

# Boîte de dialogue
dialogue = [
    "Bonjour !",
    "Comment ça va ?",
    "Je suis un PNJ dans le jeu.",
    "Amusez-vous bien !"
]

# Variables de défilement du dialogue
indice_dialogue = 0
temps_dialogue = 0
delai_dialogue = 2000  # Délai entre chaque message en millisecondes

# Boucle principale du jeu
en_cours = True
horloge = pygame.time.Clock()
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            # Passage au dialogue suivant lors d'un clic de souris
            indice_dialogue += 1
            temps_dialogue = pygame.time.get_ticks()

    ecran.fill(BLANC)

    # Affichage du dialogue
    if indice_dialogue < len(dialogue):
        message = police.render(dialogue[indice_dialogue], True, NOIR)
        rect_message = message.get_rect(center=(largeur_ecran // 2, hauteur_ecran // 2))
        ecran.blit(message, rect_message)

    # Passage automatique au dialogue suivant après un délai
    temps_actuel = pygame.time.get_ticks()
    if temps_actuel - temps_dialogue >= delai_dialogue:
        indice_dialogue += 1
        temps_dialogue = temps_actuel

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
