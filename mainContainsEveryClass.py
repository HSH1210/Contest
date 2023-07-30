import pygame
import sys
import random
import math

'''이 게임에는 (주)이키나게임즈가 제공한 'Ramche(램체)'가 사용되었습니다.
'''




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
        for col, map_col in enumerate(self.map):
            self.rectlist.append([])
            for row, cell in enumerate(map_col):
                if cell == 0:
                    self.rectlist[col].append(0)
                elif cell == 1:
                    self.rectlist[col].append(pygame.Rect(row * self.size, col * self.size, self.size, self.size))
    
    
    def update(self, camera):
        for col in self.rectlist:
            for cell in col:
                if cell != 0:
                    cell.centerx -= camera[0]
                    cell.centery -= camera[1]
                    
                    
    def draw(self, surface):
        for col in self.rectlist:
            for cell in col:
                if cell != 0:
                    pygame.draw.rect(surface, (150,100,100), cell)
        


class Player(pygame.sprite.Sprite):
    def __init__(self, name, images, pos, speed, maxspeed, collisionmap):
        super(Player, self).__init__()
        self.name = name
        self.images = images
        self.speed = speed
        self.maxspeed = maxspeed
        self.velocity = pygame.math.Vector2(0, 0)
        self.collisionmap = collisionmap
        self.No = 0
        self.image = self.images[self.No][0]
        self.rect = self.image.get_rect(center=pos)

    def update(self, keys, camera):
        
        CursorX = pygame.mouse.get_pos()[0]
        if CursorX >= self.rect.center[0]:
            self.image = self.images[self.No][0]
        else:
            self.image = self.images[self.No][1]
        
        if keys[pygame.K_a]:
            self.velocity.x -= self.speed
        if keys[pygame.K_d]:
            self.velocity.x += self.speed
        if keys[pygame.K_w]:
            self.velocity.y -= self.speed
        if keys[pygame.K_s]:
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
        
        for col in self.collisionmap.rectlist:
            for rect in col:
                if rect != 0:
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
                
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        self.rect.centerx -= camera[0]
        self.rect.centery -= camera[1]
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
            
            

class Weapon(pygame.sprite.Sprite):
    def __init__(self, images):
        super(Weapon, self).__init__()
        self.images = images
        self.No = 0
    
    def update(self, pos):
        if self.No == len(self.images):
            self.No -= len(self.images)
        elif self.No < 0:
            self.No = len(self.images)-1
            
        CursorX = pygame.mouse.get_pos()[0]
        if CursorX >= pos[0]:
            self.image0 = self.images[self.No][0]
        else:
            self.image0 = self.images[self.No][1]
            
        CursorPos = pygame.mouse.get_pos()
        dx = CursorPos[0] - pos[0]
        dy = CursorPos[1] - pos[1]
        self.angle = math.degrees(math.atan2(dx, dy))-90

        self.image = pygame.transform.rotate(self.image0, int(self.angle))
        self.rect = self.image.get_rect(center=pos)
        
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
            
            

class Bullet(pygame.sprite.Sprite):
    def __init__(self, images, pos, angle, speed, No):
        super(Bullet, self).__init__()
        self.images = images
        self.No = No
        self.angle = angle
        self.speed = speed
        self.velocity = pygame.math.Vector2(0, 0)
        
        if self.No == len(self.images):
            self.No -= len(self.images)
        elif self.No < 0:
            self.No = len(self.images)-1
            
        CursorX = pygame.mouse.get_pos()[0]
        if CursorX >= pos[0]:
            self.image0 = self.images[self.No][0]
        else:
            self.image0 = self.images[self.No][1]
        
        self.image = pygame.transform.rotate(self.image0, int(self.angle))
        self.rect = self.image.get_rect(center=pos)
        
    def update(self, surface, camera):
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = -math.sin(math.radians(self.angle)) * self.speed
        self.velocity.x = dx
        self.velocity.y = dy
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        
        self.rect.centerx -= camera[0]
        self.rect.centery -= camera[1]
        
        if not self.rect.colliderect(surface.get_rect()):
            self.kill()


class Camera:
    def __init__(self, speed, maxspeed):
        self.vel = [0,0]
        self.speed = speed
        self.maxspeed = maxspeed
        
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.vel[0] -= self.speed
        if keys[pygame.K_RIGHT]:
            self.vel[0] += self.speed
        if keys[pygame.K_UP]:
            self.vel[1] -= self.speed
        if keys[pygame.K_DOWN]:
            self.vel[1] += self.speed
            
        self.vel[0] = max(-self.maxspeed, min(self.maxspeed, self.vel[0]))
        self.vel[1] = max(-self.maxspeed, min(self.maxspeed, self.vel[1]))

        if self.vel[0] < 0:
            self.vel[0] += self.speed / 2
        elif self.vel[0] > 0:
            self.vel[0] -= self.speed / 2
        if self.vel[1] < 0:
            self.vel[1] += self.speed / 2
        elif self.vel[1] > 0:
            self.vel[1] -= self.speed / 2





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


Player_image, Player_flipped = load_image('Player.png', 3, 'y')

Sword_image, Sword_flipped = load_image('Sword.png', 3, 'x')
Gun_image, Gun_flipped = load_image('Gun.png', 3, 'x')

Bullet_image, Bullet_flipped = load_image('Bullet.png', 3, 'x')

Player_Images = [[Player_image, Player_flipped]]

Weapon_Images = [[Sword_image, Sword_flipped],
                 [Gun_image, Gun_flipped]]

Bullet_Images = [[Bullet_image, Bullet_flipped]]

'''
def NoOutOfRange(No, images):
    if No == len(images):
        No -= len(images)
    elif No < 0:
        No = len(images)-1
    return No
'''


def main():
    fps = 60

    width = 1600
    height = 900
    
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Contest Game')
    clock = pygame.time.Clock()
    
    
    CameraSpeed = 2
    CameraMaxspeed = 20
    camera = Camera(CameraSpeed, CameraMaxspeed)
    
    collisionmap = CollisionMap()
    
    Player_name = 'HSH'
    Player_initpos = (width/2, height/2)
    Player_speed = 1
    Player_maxspeed = 10
    player = Player(Player_name, Player_Images,
                  Player_initpos, Player_speed, Player_maxspeed, collisionmap)
    
    weapon = Weapon(Weapon_Images)
    
    Bullet_Group = pygame.sprite.Group()

    
    
    onGame = True
    while onGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                onGame = False
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    weapon.No += 1
                elif event.y < 0:
                    weapon.No -= 1
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(Bullet_Images, weapon.rect.center, weapon.angle, 10, weapon.No)
                Bullet_Group.add(bullet)
                
                
        keys = pygame.key.get_pressed()
        
        camera.update(keys)
        
        player.update(keys, camera.vel)
        collisionmap.update(camera.vel)
        weapon.update(player.rect.center)
        Bullet_Group.update(screen, camera.vel)
        
        screen.fill((200,200,200))
        collisionmap.draw(screen)
        player.draw(screen)
        Bullet_Group.draw(screen)
        weapon.draw(screen)


        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    main()

