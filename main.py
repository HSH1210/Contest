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
char = pygame.image.load('character.png')
char = pygame.transform.scale(char, (ch_size, ch_size))
chx, chy, chxs, chys = 0, 0, 0, 0


def chMove():
    global chx, chy, chxs, chys
    keyInput = pygame.key.get_pressed()
    if keyInput[pygame.K_a]:
        chxs -= ch_speed
    if keyInput[pygame.K_d]:
        chxs += ch_speed
    if keyInput[pygame.K_w]:
        chys -= ch_speed
    if keyInput[pygame.K_s]:
        chys += ch_speed

    chxs = max(-maxspeed, min(maxspeed, chxs))
    chys = max(-maxspeed, min(maxspeed, chys))

    if chxs < 0:
        chxs += ch_speed/2
    elif chxs > 0:
        chxs -= ch_speed/2
    if chys < 0:
        chys += ch_speed/2
    elif chys > 0:
        chys -= ch_speed/2

    chx = round(chx, 2)
    chy = round(chy, 2)
    chxs = round(chxs, 2)
    chys = round(chys, 2)

    chx += chxs
    chy += chys


def initGame():
    global screen, clock, char
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Contest Game') # 창 제목 설정
    clock = pygame.time.Clock() # 시간 설정


def runGame():
    global screen, clock, char
    onGame = True
    while onGame:
        for event in pygame.event.get(): # 발생한 입력 event 목록의 event마다 검사
            if event.type == pygame.QUIT: # event의 type이 QUIT에 해당할 경우
                onGame = False
                pygame.quit() # pygame을 종료한다
                sys.exit() # 창을 닫는다

        chMove() # 캐릭터 움직임
        screen.fill(gray) # screen를 회색으로 채운다
        screen.blit(char, pygame.Rect(int(chx), int(chy), ch_size, ch_size)) # 캐릭터 blit   
        pygame.display.update() # 화면을 업데이트한다
        clock.tick(60)

initGame()
runGame()
