import pygame

class Plateforme(pygame.sprite.Sprite):
    def __init__(self, infos, *groups):
        super().__init__(*groups)

        self.image = pygame.Surface((infos[2], infos[3]))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = infos[0]
        self.rect.y = infos[1]

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)