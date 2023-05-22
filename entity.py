import pygame

# ! Format d'image requis nom_numéro.png (Toujours compté à partir de 0 mettre numéro à 0 même si image seul)
# Exemple boulette_0.png
class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, img_path, *groups): #img_path = chemin de l'image sans le 'numéro.png'
        super().__init__(*groups)
        self.image = pygame.image.load(img_path+"0.png").convert_alpha() #Prend au départ la première ou la seule image de la collection
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.mask.from_surface(self.image)

class MovableEntity(Entity):
    def __init__(self, vect_direct, speed, pos, img_path, *groups):
        super().__init__(pos, img_path, *groups)
        self.vect = pygame.math.Vector2(vect_direct)
        self.speed = speed
        self.state = 0

    def move(self):
        if self.vect.magnitude() != 0:
            self.vect = self.vect.normalize()
        self.rect.x += self.vect[0] * self.speed
        self.rect.y += self.vect[1] * self.speed

    def animation(self, liste, need_mirror):
        if need_mirror:
            self.image = pygame.transform.flip(pygame.image.load(liste[self.state]).convert_alpha(), True, False)
        else:
            self.image = pygame.image.load(liste[self.state]).convert_alpha()
        self.state += 1
        if self.state > len(liste) - 1:
            self.state = 0

    def create_image_list(self, path, limit):
        listes = []
        for i in range(0, limit):
            listes.append(path+str(i)+".png")
        return listes

