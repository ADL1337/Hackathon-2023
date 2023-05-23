import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, img_path, *groups): #img_path = chemin de l'image sans le 'numéro.png'
        super().__init__(*groups)
        self.image = pygame.image.load(img_path+"0.png").convert_alpha() #Prend au départ la première ou la seule image de la collection
        self.hitbox = pygame.mask.from_surface(self.image)
        self.rect = self.hitbox.get_bounding_rects()[0]
        self.rect.x = pos[0]
        self.rect.y = pos[1]

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

    def animation(self, liste, sym_x, sym_y, size_factor):
        self.image = pygame.transform.scale_by(pygame.transform.flip(pygame.image.load(liste[self.state]).convert_alpha(), sym_x, sym_y), size_factor)
        self.state += 1
        self.state %= len(liste)

    def create_image_list(self, path, limit):
        listes = []
        for i in range(0, limit):
            listes.append(path+str(i)+".png")
        return listes

