import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, img_path, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(img_path).convert()
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = self.image.get_masks()


