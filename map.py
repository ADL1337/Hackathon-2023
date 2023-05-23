import pygame

from csv import reader

from game_data import TILESIZE


class Map:
    pass


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, img, *groups):
        super().__init__(*groups)
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)

class TileMap:
    def __init__(self, path, tilesize=TILESIZE):
        self.map = AssetLoader.map_from_csv(path)
        print(self.map)
        self.tilesize = tilesize
        self.surfaces = AssetLoader.surfaces_from_spritesheet("res/Terrain.png", tilesize)
        self.tiles = pygame.sprite.Group()
        self.create_tiles()
    
    def create_tiles(self):
        for y, row in enumerate(self.map):
            for x, tile_id in enumerate(row):
                if tile_id != "-1":
                    print(tile_id, x, y)
                    Tile((x * self.tilesize, y * self.tilesize), self.surfaces[int(tile_id)], self.tiles)


class AssetLoader:
    @staticmethod
    def map_from_csv(path):
        with open(path, "r") as f:
            csv_reader = reader(f)
            return [row for row in csv_reader]
    
    @staticmethod
    def surfaces_from_spritesheet(path, tilesize):
        spritesheet = pygame.image.load(path).convert_alpha()
        height, width = spritesheet.get_height() // tilesize, spritesheet.get_width() // tilesize
        print(height, width)
        return [spritesheet.subsurface(x * tilesize, y * tilesize, tilesize, tilesize) for x in range(width) for y in range(height)]


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True

    test_sheet = pygame.image.load("res/Terrain.png").convert_alpha()
    tile_group = pygame.sprite.Group()
    tiles = AssetLoader.surfaces_from_spritesheet("res/Terrain.png", 16)
    print(len(tiles))
    i = 0
    tile_group.add(Tile((0, 0), tiles[101]))
    while i < 241:
        clock.tick(60)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = 241
        screen.blit(tiles[i], (0, 0))

        i += 1
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()