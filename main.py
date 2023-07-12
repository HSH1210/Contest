import pygame
import sys
import random
import math


fps = 60

white = (255, 255, 255)
black = (0, 0, 0)
gray = (204, 204, 204)

width = 1600
height = 900

screen = pygame.display.set_mode((width, height))

class Story:
    def nomalTalk(who, speech):
        pygame.draw.rect(screen, (204, 102, 0), pygame.Rect(0, height-300, 1600, 300))
        fontSize = 30
        cut = 80
        font = pygame.font.SysFont('comicsansms', fontSize)

        if who == 'player':
            pygame.draw.rect(screen, (104, 102, 0), pygame.Rect(50, height-350, 300, 100))
            if len(speech) >= cut:
                text1 = font.render(speech[0:cut], True, (0, 0, 0))
                text2 = font.render(speech[cut:cut*2], True, (0, 0, 0))
                screen.blit(text1, (50, height - 250))
                screen.blit(text2, (50, height - 200))
            else:
                text = font.render(speech, True, (0, 0, 0))
                screen.blit(text, (50, height - 250))
        elif who == 'NPC':
            pygame.draw.rect(screen, (104, 102, 0), pygame.Rect(width-500, height-350, 300, 100))
            if len(speech) >= cut:
                text1 = font.render(speech[0:cut], True, (0, 0, 0))
                text2 = font.render(speech[cut:cut*2], True, (0, 0, 0))
                screen.blit(text1, (50, height - 250))
                screen.blit(text2, (50, height - 200))
            else:
                text = font.render(speech, True, (0, 0, 0))
                screen.blit(text, (50, height - 250))
        
    def surpriseTalk(who, speech):
        pygame.draw.rect(screen, (204, 102, 0), pygame.Rect(0, height-300, 1600, 300))
        fontSize = 100
        font = pygame.font.SysFont('comicsansms', fontSize)

        if who == 'player':
            pygame.draw.rect(screen, (104, 102, 0), pygame.Rect(50, height-350, 300, 100))
            text = font.render(speech, True, (0, 0, 0))
            screen.blit(text, (50, height - 250))

        elif who == 'NPC':
            pygame.draw.rect(screen, (104, 102, 0), pygame.Rect(width-500, height-350, 300, 100))
            text = font.render(speech, True, (0, 0, 0))
            screen.blit(text, (50, height - 250))

def load_image(location, size, axis):
    image = pygame.image.load(location)
    sizeX = image.get_height()
    sizeY = image.get_width()
    image = pygame.transform.scale(image, (sizeX*size, sizeY*size))
    if axis == 'x':
        flipped = pygame.transform.flip(image, False, True)
    elif axis == 'y':
        flipped = pygame.transform.flip(image, True, False)

    return image, flipped


Player_image, Player_flipped = load_image('character2.png', 5, 'y')
Weapon_image, Weapon_flipped = load_image('Weapon1.png', 5, 'x')


class Player(pygame.sprite.Sprite):
    def __init__(self, image, flipped, pos, speed, maxspeed):
        super(Player, self).__init__()
        self.image = image
        self.flipped = flipped
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.maxspeed = maxspeed
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self, keyInput):
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


class Weapon:
    def __init__(self, image, flipped):
        super(Weapon, self).__init__()
        self.image0 = image
        self.flipped0 = flipped
        self.rect = self.image0.get_rect()
    
    def update(self, player):
        self.rect.center = player.rect.center

        cursor_x, cursor_y = pygame.mouse.get_pos()
        dx = cursor_x - self.rect0.centerx
        dy = cursor_y - self.rect0.centery
        self.angle = math.degrees(math.atan2(dx, dy))-90

        self.image1 = pygame.transform.rotate(self.image0, int(self.angle))
        self.flipped1 = pygame.transform.rotate(self.flipped0, int(self.angle))

    def draw(self, surface):
        cursorx = pygame.mouse.get_pos()[0]
        if cursorx >= self.rect1.centerx:
            surface.blit(self.image1, self.rect1)
        else:
            surface.blit(self.flipped1, self.rect1)
        

def RunGame():
    global width, height,screen
    pygame.init()
    pygame.display.set_caption('Contest Game')
    clock = pygame.time.Clock()

    initpos = (width/2, height/2)
    ch_speed = 1
    maxspeed = 10
    char = Player(Player_image, Player_flipped, initpos, ch_speed, maxspeed)
    weapon = Weapon(Weapon_image, Weapon_flipped) 

    onGame = True
    while onGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                onGame = False
                pygame.quit()
                sys.exit()

        keyInput = pygame.key.get_pressed()
        char.update(keyInput)
        weapon.update(char)

        screen.fill(gray)
        char.draw(screen)
        weapon.draw(screen)

        pygame.display.update()
        clock.tick(fps)

if __name__ == '__main__':
    RunGame()
