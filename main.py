import pygame
import sys
import random

width = 1600
height = 900    
white = (255, 255, 255)
black = (0, 0, 0)
gray = (204, 204, 204)

ch_size = 50
ch_speed = 0.1
maxspeed = 2.5
ch = pygame.image.load('character.jpg')
ch = pygame.transform.scale(ch, (ch_size, ch_size))
chx, chy, chsx, chsy = 0, 0, 0, 0


def chMove():
    global chx, chy, chsx, chsy
    keyInput = pygame.key.get_pressed()
    if keyInput[pygame.K_a]:
        chsx -= ch_speed
    if keyInput[pygame.K_d]:
        chsx += ch_speed
    if keyInput[pygame.K_w]:
        chsy -= ch_speed
    if keyInput[pygame.K_s]:
        chsy += ch_speed

    chsx = max(-maxspeed, min(maxspeed, chsx))
    chsy = max(-maxspeed, min(maxspeed, chsy))

    if chsx < 0:
        chsx += ch_speed/2
    elif chsx > 0:
        chsx -= ch_speed/2
    if chsy < 0:
        chsy += ch_speed/2
    elif chsy > 0:
        chsy -= ch_speed/2

    chx = round(chx, 2)
    chy = round(chy, 2)
    chsx = round(chsx, 2)
    chsy = round(chsy, 2)

    chx += chsx
    chy += chsy
    print(chx,chy,chsx,chsy)


def initGame():
    global screen, clock, ch
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Game') # 창 제목 설정
    clock = pygame.time.Clock() # 시간 설정


def runGame():
    global screen, clock, ch, fps
    fps = clock.tick(60)
    onGame = True
    while onGame:
        for event in pygame.event.get(): # 발생한 입력 event 목록의 event마다 검사
            if event.type == QUIT: # event의 type이 QUIT에 해당할 경우
                pygame.quit() # pygame을 종료한다
                sys.exit() # 창을 닫는다

        chMove() # 캐릭터 움직임
        screen.fill(gray) # screen를 하얀색으로 채운다
        screen.blit(ch, pygame.Rect(int(chx), int(chy), ch_size, ch_size)) # 캐릭터 blit   
        pygame.display.update() # 화면을 업데이트한다

initGame()
runGame()
