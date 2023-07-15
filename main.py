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



class CollisionMap:
    def __init__(self):
        self.map = [[1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,1,0,1,0,0,0,0,0,1],
                    [1,0,1,0,0,0,1,0,1,1,1,0,1],
                    [1,0,0,0,1,1,1,0,0,0,0,0,1],
                    [1,0,1,0,0,0,0,0,1,1,1,0,1],
                    [1,0,1,0,1,1,1,0,1,0,0,0,1],
                    [1,0,1,0,1,0,0,0,1,1,1,0,1],
                    [1,0,1,0,1,1,1,0,1,0,1,0,1],
                    [1,0,0,0,0,0,0,0,0,0,1,0,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1]]
        
        self.size = 150
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
                    



class Player(pygame.sprite.Sprite):
    def __init__(self, name, image, flipped, pos, speed, maxspeed, collisionmap):
        super(Player, self).__init__()
        self.name = name
        self.image = image
        self.flipped = flipped
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.maxspeed = maxspeed
        self.velocity = pygame.math.Vector2(0, 0)
        self.collisionmap = collisionmap

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
            
        
        new_left = pygame.Rect(self.rect.left + self.velocity.x, self.rect.top, 1, self.rect.height)
        new_right = pygame.Rect(self.rect.right + self.velocity.x, self.rect.top, 1, self.rect.height)
        new_top = pygame.Rect(self.rect.left, self.rect.top + self.velocity.y, self.rect.width, 1)
        new_bottom = pygame.Rect(self.rect.left, self.rect.bottom + self.velocity.y, self.rect.width, 1)
        
        # try:
        for rect in self.collisionmap.rectlist:
            if new_left.colliderect(rect):
                self.velocity.x = 0
                self.rect.left = rect.right
            if new_right.colliderect(rect):
                self.velocity.x = 0
                self.rect.right = rect.left
            if new_top.colliderect(rect):
                self.velocity.y = 0
                self.rect.top = rect.bottom
            if new_bottom.colliderect(rect):
                self.velocity.y = 0
                self.rect.bottom = rect.top
        # except UnboundLocalError:
        #     pass
                
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



# class Game:
def RunGame():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Contest Game')
    clock = pygame.time.Clock()

    Player_name = 'HSH'
    Player_initpos = (width/2, height/2)
    Player_speed = 1
    Player_maxspeed = 10
    collisionmap = CollisionMap()
    char = Player(Player_name, Player_image, Player_flipped, 
                  Player_initpos, Player_speed, Player_maxspeed, collisionmap)
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
        collisionmap.draw(screen)
        char.draw(screen)
        weapon.draw(screen)

        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    RunGame()

