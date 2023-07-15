import pygame
import math


class Weapon:
    def __init__(self, image, flipped):
        super(Weapon, self).__init__()
        self.image0 = image
        self.flipped0 = flipped
    
    def update(self, player):
        cursor_pos = pygame.mouse.get_pos()
        dx = cursor_pos[0] - player.rect.centerx
        dy = cursor_pos[1] - player.rect.centery
        self.angle = math.degrees(math.atan2(dx, dy))-90

        self.image1 = pygame.transform.rotate(self.image0, int(self.angle))
        self.flipped1 = pygame.transform.rotate(self.flipped0, int(self.angle))

        self.rect = self.image1.get_rect(center=player.rect.center)

    def draw(self, surface):
        cursorx = pygame.mouse.get_pos()[0]
        if cursorx >= self.rect.centerx:
            surface.blit(self.image1, self.rect)
        else:
            surface.blit(self.flipped1, self.rect)