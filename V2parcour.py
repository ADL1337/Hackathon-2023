import pygame
import csv

# Initialisation de Pygame
pygame.init()

# Définition de la taille de l'écran
largeur_ecran = 1300
hauteur_ecran = 800
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))

# Chargement de l'image de fond
fond = pygame.image.load("desmet.jpg").convert()
fond = pygame.transform.scale(fond, (largeur_ecran, hauteur_ecran))

# Chargement des images des personnages
personnage_image1 = pygame.image.load("player.png").convert_alpha()
personnage_image2 = pygame.image.load("player.png").convert_alpha()

# Chargement des images des blocs
bloc_image = pygame.image.load("block.png").convert_alpha()
bloc_degat_image = pygame.image.load("block2.png").convert_alpha()

# Chargement de l'image de l'ennemi
ennemi_image = pygame.image.load("enemi.png").convert_alpha()

# Chargement de la carte depuis un fichier CSV
def charger_carte(nom_fichier):
    carte = []
    with open(nom_fichier, newline='') as fichier_csv:
        lecteur_csv = csv.reader(fichier_csv, delimiter=',')
        for ligne in lecteur_csv:
            carte.append(list(map(int, ligne)))
    return carte

# Chargement des blocs à partir du fichier CSV
def charger_blocs(nom_fichier, image):
    blocs = pygame.sprite.Group()
    with open(nom_fichier, newline='') as fichier_csv:
        lecteur_csv = csv.reader(fichier_csv, delimiter=',')
        for ligne in range(len(carte)):
            for colonne in range(len(carte[ligne])):
                if carte[ligne][colonne] > 1:
                    bloc = Bloc(colonne * 16, ligne * 16, image)
                    blocs.add(bloc)
    return blocs

# Chargement des blocs de dégâts à partir du fichier CSV
def charger_blocs_degats(nom_fichier, image):
    blocs_degats = pygame.sprite.Group()
    with open(nom_fichier, newline='') as fichier_csv:
        lecteur_csv = csv.reader(fichier_csv, delimiter=',')
        for ligne in range(len(carte)):
            for colonne in range(len(carte[ligne])):
                if carte[ligne][colonne] > 698:
                    bloc_degat = BlocDegat(colonne * 16, ligne * 16, image)
                    blocs_degats.add(bloc_degat)
    return blocs_degats

# Classe du joueur
class Joueur(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.saut = False

    def update(self, blocs):
        self.gravite()

        # Déplacement horizontal
        self.rect.x += self.vx
        blocs_collisionnes = pygame.sprite.spritecollide(self, blocs, False)
        for bloc in blocs_collisionnes:
            if self.vx > 0:
                self.rect.right = bloc.rect.left
            elif self.vx < 0:
                self.rect.left = bloc.rect.right

        # Déplacement vertical
        self.rect.y += self.vy
        blocs_collisionnes = pygame.sprite.spritecollide(self, blocs, False)
        for bloc in blocs_collisionnes:
            if self.vy > 0:
                self.rect.bottom = bloc.rect.top
                self.saut = False
            elif self.vy < 0:
                self.rect.top = bloc.rect.bottom
        if self.rect.bottom >= hauteur_ecran:
            self.rect.bottom = hauteur_ecran
            self.saut = False

    def sauter(self):
        if not self.saut:
            self.vy = -10
            self.saut = True

    def gravite(self):
        if self.vy == 0:
            self.vy = 1
        else:
            self.vy += 0.5

# Classe des blocs
class Bloc(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Classe des blocs de dégâts
class BlocDegat(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Ajoutez ici la logique pour les dégâts aux joueurs ou aux ennemis
        pass

# Classe de l'ennemi
class Ennemi(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 2

    def update(self, blocs):
        self.rect.x += self.vx
        blocs_collisionnes = pygame.sprite.spritecollide(self, blocs, False)
        for bloc in blocs_collisionnes:
            if self.vx > 0:
                self.rect.right = bloc.rect.left
                self.vx = -self.vx
            elif self.vx < 0:
                self.rect.left = bloc.rect.right
                self.vx = -self.vx

# Chargement de la carte depuis le fichier CSV
carte = charger_carte("map1_walls.csv")

# Chargement des blocs
blocs = charger_blocs("map1_walls.csv", bloc_image)

# Chargement des blocs de dégâts
blocs_degats = charger_blocs_degats("map1_spikes.csv", bloc_degat_image)

# Création du joueur
joueur = Joueur(50, 50, personnage_image1)

# Création de l'ennemi
ennemi = Ennemi(0, 550, ennemi_image)
ennemis = pygame.sprite.Group()
ennemis.add(ennemi)

# Boucle principale du jeu
en_cours = True
horloge = pygame.time.Clock()
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_SPACE:
                joueur.sauter()

    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT]:
        joueur.vx = -5
    elif touches[pygame.K_RIGHT]:
        joueur.vx = 5
    else:
        joueur.vx = 0

    joueur.update(blocs)
    ennemis.update(blocs)

    ecran.blit(fond, (0, 0))
    blocs.draw(ecran)
    blocs_degats.draw(ecran)
    ennemis.draw(ecran)
    ecran.blit(joueur.image, joueur.rect)
    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
