import pygame
import csv

pygame.init()

largeur_ecran = 1080
hauteur_ecran = 720
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))

# Chargement de la carte depuis un fichier CSV
def charger_carte(nom_fichier):
    carte = []
    with open(nom_fichier, newline='') as fichier_csv:
        lecteur_csv = csv.reader(fichier_csv, delimiter=',')
        for ligne in lecteur_csv:
            carte.append(list(map(int, ligne)))
    return carte

GRAVITE = 0.5
VITESSE_MAX = 3
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)

class Joueur(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(BLEU)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.saut = False

    def update(self):
        self.gravite()

        self.rect.x += self.vx
        blocs_collisionnes = pygame.sprite.spritecollide(self, blocs, False)
        for bloc in blocs_collisionnes:
            if self.vx > 0:
                self.rect.right = bloc.rect.left
            elif self.vx < -1:
                self.rect.left = bloc.rect.right

        self.rect.y += self.vy
        blocs_collisionnes = pygame.sprite.spritecollide(self, blocs, False)
        for bloc in blocs_collisionnes:
            if self.vy > 0:
                self.rect.bottom = bloc.rect.top
                self.saut = False
            elif self.vy < 0:
                self.rect.top = bloc.rect.bottom

    def gravite(self):
        if self.vy == 0:
            self.vy = 1
        else:
            self.vy += GRAVITE
        if self.vy > VITESSE_MAX:
            self.vy = VITESSE_MAX

    def sauter(self):
        if not self.saut:
            self.vy = -10
            self.saut = True

class Bloc(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill(BLANC)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

joueur = Joueur(16, 16)
blocs = pygame.sprite.Group()
carte = charger_carte("map.csv")
for ligne in range(len(carte)):
    for colonne in range(len(carte[ligne])):
        if carte[ligne][colonne] > 1:
            bloc = Bloc(colonne * 16, ligne * 16)
            blocs.add(bloc)
        if carte[ligne][colonne] == 699:
            print('mort')

running = True
horloge = pygame.time.Clock()
while running:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            running = False
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

    joueur.update()

    ecran.fill((0, 0, 0))
    blocs.draw(ecran)
    ecran.blit(joueur.image, joueur.rect)

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()