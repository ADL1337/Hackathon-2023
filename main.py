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
delai_dialogue = 1500  # Délai entre chaque message en millisecondes

# Boucle principale du jeu
en_cours = True
horloge = pygame.time.Clock()
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    ecran.fill(BLANC)

    # Affichage du dialogue
    if indice_dialogue < len(dialogue):
        message = police.render(dialogue[indice_dialogue], True, NOIR)
        ecran.blit(message, (50, hauteur_ecran // 10))
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel - temps_dialogue >= delai_dialogue:
            temps_dialogue = temps_actuel
            indice_dialogue += 1

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
