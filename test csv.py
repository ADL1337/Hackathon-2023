import csv
import pygame

# Dimensions des tuiles dans la tileset
TILE_WIDTH = 40
TILE_HEIGHT = 40

tile_ids = {}

# Lire le fichier CSV et attribuer un ID à chaque tuile
with open("maptest.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        x = int(row["x"])
        y = int(row["y"])
        tile = tileset.subsurface(pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT))
        tile_id = assign_tile_id()  # Assigner un ID unique à la tuile (selon votre logique)
        tile_ids[(x // TILE_WIDTH, y // TILE_HEIGHT)] = tile_id

