import pygame
import sys
import random
import math


fps = 60

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (204, 204, 204)

ch_size = (50, 50)
Player_image = pygame.image.load('character2.png')
Player_image = pygame.transform.scale(Player_image, ch_size)
Player_flipped = pygame.transform.flip(Player_image, True, False)

class Player:
    def __init__(self, image, image_flipped, x, y, speed, maxspeed):
        self.image = image
        self.flipped = image_flipped
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = speed
        self.maxspeed = maxspeed
        self.velocity = pygame.math.Vector2(0, 0)

    def move(self, keyInput):
        if keyInput[pygame.K_a]:
            self.velocity.x -= self.speed
        if keyInput[pygame.K_d]:
            self.velocity.x += self.speed
        if keyInput[pygame.K_w]:
            self.velocity.y -= self.speed
        if keyInput[pygame.K_s]:
            self.velocity.y += self.speed

        self.velocity.x = max(-self.maxspeed, min(self.maxspeed, self.velocity.x))
        self.velocity.y = max(-self.maxspeed, min(self.maxspeed, self.velocity.y))

        if self.velocity.x < 0:
            self.velocity.x += self.speed / 2
        elif self.velocity.x > 0:
            self.velocity.x -= self.speed / 2
        if self.velocity.y < 0:
            self.velocity.y += self.speed / 2
        elif self.velocity.y > 0:
            self.velocity.y -= self.speed / 2
    
        self.rect.move_ip(self.velocity.x, self.velocity.y)

    def draw(self, surface):
        cursorx = pygame.mouse.get_pos()[0]
        if cursorx >= self.rect.centerx:
            surface.blit(self.image, self.rect)
        else:
            surface.blit(self.flipped, self.rect)
        

def RunGame():
    pygame.init()
    width = 1600
    height = 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Contest Game')
    clock = pygame.time.Clock()

    ch_initx = 0
    ch_inity = 0
    ch_speed = 1
    maxspeed = 10
    char = Player(Player_image, Player_flipped, ch_initx, ch_inity, ch_speed, maxspeed)

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
        clock.tick(fps)

if __name__ == '__main__':
    RunGame()

