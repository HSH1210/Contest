import pygame
import sys
import random

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (204, 204, 204)

class Player:
    def __init__(self, location, x, y, sizeX, sizeY, speed, maxspeed):
        self.image = pygame.image.load(location)
        self.image = pygame.transform.scale(self.image, (sizeX, sizeY))
        self.flipped = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.maxspeed = maxspeed
        self.rect.x = x
        self.rect.y = y
        self.xs = 0
        self.ys = 0

    def move(self, keyInput):
        if keyInput[pygame.K_a]:
            self.xs -= self.speed
        if keyInput[pygame.K_d]:
            self.xs += self.speed
        if keyInput[pygame.K_w]:
            self.ys -= self.speed
        if keyInput[pygame.K_s]:
            self.ys += self.speed

        self.xs = max(-self.maxspeed, min(self.maxspeed, self.xs))
        self.ys = max(-self.maxspeed, min(self.maxspeed, self.ys))

        if self.xs < 0:
            self.xs += self.speed / 2
        elif self.xs > 0:
            self.xs -= self.speed / 2
        if self.ys < 0:
            self.ys += self.speed / 2
        elif self.ys > 0:
            self.ys -= self.speed / 2

        self.rect.x += round(self.xs, 2)
        self.rect.y += round(self.ys, 2)

    def draw(self, surface):
        cursorx = pygame.mouse.get_pos()[0]
        if cursorx >= self.rect.x + self.rect.width/2:
            surface.blit(self.image, (int(self.rect.x), int(self.rect.y)))
        else:
            surface.blit(self.flipped, (int(self.rect.x), int(self.rect.y)))
        

def RunGame():
    pygame.init()
    width = 1600
    height = 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Contest Game')
    clock = pygame.time.Clock()

    ch_initx = 0
    ch_inity = 0
    ch_size = 50
    ch_speed = 1
    maxspeed = 10
    char = Player('character2.png', ch_initx, ch_inity, ch_size, ch_size, ch_speed, maxspeed)

    onGame = True
    while onGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                onGame = False
                pygame.quit()
                sys.exit()

        keyInput = pygame.key.get_pressed()
        char.move(keyInput)

        screen.fill(gray)
        char.draw(screen)
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    RunGame()

