import pygame # pygame 모듈의 임포트
import sys # 외장 모듈
from pygame.locals import * # QUIT 등의 pygame 상수들을 로드한다.
import random

width = 1600 # 상수 설정
height = 900    
white = (255, 255, 255)
black = (0, 0, 0)
gray = (204, 204, 204)

character_size = 50 # 캐릭터
charspeed = 0.6
character = pygame.image.load('character.jpg')
character = pygame.transform.scale(character, (character_size, character_size))
r1 = pygame.Rect(width / 2 - 400, height / 2 - 300, character_size, character_size)

def characterMove():
    keyInput = pygame.key.get_pressed()
    if keyInput[pygame.K_a] and r1.left >= 0:
        r1.x -= charspeed
    elif keyInput[pygame.K_d] and r1.right <= width:
        r1.x += charspeed
    elif keyInput[pygame.K_w] and r1.top >= 0:
        r1.y -= charspeed
    elif keyInput[pygame.K_s] and r1.bottom <= height:
        r1.y += charspeed

def initGame():
    global screen, clock, character
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Game') # 창 제목 설정
    clock = pygame.time.Clock() # 시간 설정


def runGame():
    global screen, clock, character, fps
    fps = clock.tick(60)
    onGame = True
    while onGame:
        for event in pygame.event.get(): # 발생한 입력 event 목록의 event마다 검사
            if event.type == QUIT: # event의 type이 QUIT에 해당할 경우
                pygame.quit() # pygame을 종료한다
                sys.exit() # 창을 닫는다

        characterMove() #캐릭터 움직임
        screen.fill(gray) # screen를 하얀색으로 채운다
        screen.blit(character, r1)    
        pygame.display.update() # 화면을 업데이트한다

initGame()
runGame()