import pygame


class CollisionMap:
    def __init__(self, map, size):
        self.map = map
        self.size = size
        self.rectlist = []

    def draw(self, surface):
        self.rectlist = []
        for col, map_col in enumerate(self.map):
            for row, cell in enumerate(map_col):
                if cell == 0:
                    pygame.draw.rect(surface, (200,200,200),
                                     (row * self.size, col * self.size, self.size, self.size))
                elif cell == 1:
                    pygame.draw.rect(surface, (0,200,200),
                                     (row * self.size, col * self.size, self.size, self.size))
                    self.rectlist.append(pygame.Rect(row * self.size, col * self.size, self.size, self.size))
                    