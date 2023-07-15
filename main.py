import pygame
import sys
import random
import math

from ClassPlayer import *
from ClassWeapon import *
from ClassCollisionMap import *


fps = 60

white = (255, 255, 255)
black = (0, 0, 0)
gray = (204, 204, 204)

width = 1600
height = 900

Game_map = [[1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,0,1,0,0,0,0,0,1],
            [1,0,1,0,0,0,1,0,1,1,1,0,1],
            [1,0,0,0,1,1,1,0,0,0,0,0,1],
            [1,0,1,0,0,0,0,0,1,1,1,0,1],
            [1,0,1,0,1,1,1,0,1,0,0,0,1],
            [1,0,1,0,1,0,0,0,1,1,1,0,1],
            [1,0,1,0,1,1,1,0,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1]]


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


# class Game:
def RunGame():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Contest Game')
    clock = pygame.time.Clock()


    map_size = 100
    collisionmap = CollisionMap(Game_map, map_size)

    Player_size = 4
    Player_image, Player_flipped = load_image('character2.png', Player_size, 'y')
    Player_name = 'HSH'
    Player_initpos = (width/2, height/2)
    Player_speed = 1
    Player_maxspeed = 10
    char = Player(Player_name, Player_image, Player_flipped, 
                  Player_initpos, Player_speed, Player_maxspeed, collisionmap)
    
    Weapon_image, Weapon_flipped = load_image('Weapon1.png', Player_size, 'x')
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

