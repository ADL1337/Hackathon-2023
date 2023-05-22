import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, img_path, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(img_path).convert()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.mask.from_surface(self.image)

class MovableEntity(Entity):
    def __init__(self, vect_direct, speed, pos, img_path, *groups):
        super().__init__(pos, img_path, *groups)
        self.vect = pygame.math.Vector2(vect_direct)
        self.speed = speed

    def move(self):
        if self.vect.magnitude() != 0:
            self.vect = self.vect.normalize()
        self.rect.x += self.vect[0] * self.speed
        self.rect.y += self.vect[1] * self.speed

