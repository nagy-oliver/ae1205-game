import pygame as pg
import time
from math import sin, cos, radians, degrees, pi, sqrt, floor

from game import Game
from menu import Menu

posList = []
for i in range(4):
    posList.append(pg.transform.scale(pg.image.load(f"assets/{i}.png"), (500, 500)))

pg.init()

white = (255, 255, 255)
black = (0, 0, 0)
grey = (200, 200, 200)
red = (200, 0, 0)


MINSLEEP = 0.001  # Minimum interval to sleep the CPU
tsim = 0.0  # Simulation time
tstart =  0.001 * pg.time.get_ticks()
dt = 1/60

X = 550
Y = 500

screen = pg.display.set_mode((X, Y))

background = pg.image.load("assets/Background.png")
background = pg.transform.scale(background, (500, 500))
backgroundRect = background.get_rect()

input = ""

progress = pg.image.load("assets/BAR.png")
progress = pg.transform.scale(progress, (50, 500))
progressRect = progress.get_rect()
progressRect.center = (25, Y/2)

clicks = 0
clickrate = 0
prevclicks = 0
running = True
t = 0
refreshtime = 1

font = pg.font.Font('freesansbold.ttf', 32)
font2 = pg.font.Font('freesansbold.ttf', 50)

score = 0
k = 4
difficulty = 4
inGame = False
inChoose = False
inLead = False

wnum = 0
wnums = ""
weight = 3*[0]

while running:
#SIMULATION TIME
    tsim = tsim + dt
#REMAINDER TO SLEEP FOR CPU
    remainder = tsim - (0.001 * pg.time.get_ticks() - tstart)
    if remainder > MINSLEEP:
        time.sleep(remainder)
    
    t+=dt
    screen.fill(grey)
    screen.blit(background, backgroundRect)

    if inGame:
        backgroundRect.center = (X/2+25, Y/2)
        pg.transform.scale(screen, (1000, 2000))
        if t > refreshtime:
            t = 0
            curclicks = clicks - prevclicks
            prevclicks = clicks
            clickrate = curclicks/refreshtime
        
        if score < 100:
            if clickrate >= difficulty:
                score = score + (clickrate-difficulty) * k * dt
            elif clickrate < difficulty and score > 0:
                score = score - 10*dt
            else:
                score = 0
        else:
            score = 100
    
        if score < 33:
            pos = posList[0]
        elif score == 33:
            pos = posList[0] #OTHER MECHANICS TO BE ADDED
        elif 66 > score > 33:
            pos = posList[1]
        elif score == 66:   
            pos = posList[1] #OTHER MECHANICS TO BE ADDED
        elif 100 > score > 66:
            pos = posList[2]
        elif score >= 100:
            pos = posList[3]
            
            text3 = font2.render("You Won!", True, white)
            text3Rect = text3.get_rect()
            text3Rect.center = (X/2, Y/4)
            screen.blit(text3, text3Rect)
            
        def myround(x, base=5):
            return base * (x//base)
            
        height = myround(5*score)
        pg.draw.rect(screen, red, pg.Rect(0, abs(500 - height), 50, height))
        
        screen.blit(progress, progressRect)

        # text1 = font.render('Clickrate: ' + str(clickrate), True, black, white)
        # text1Rect = text1.get_rect()
        # text1Rect.center = (X/2, 20)
        # screen.blit(text1, text1Rect)
        
        # text2 = font.render(str(floor(score)) + " %", True, black, white)
        # text2Rect = text2.get_rect()
        # text2Rect.center = (X/2, 60)
        # screen.blit(text2, text2Rect)
        
        posrect = pos.get_rect()
        posrect.centerx = X/2+25
        posrect.centery = Y/2
        screen.blit(pos, posrect)

    else:
        backgroundRect.center = (X/2, Y/2)            
        if inChoose:
            if wnum == 0: wnums = "first"
            elif wnum == 1: wnums = "second"
            elif wnum == 2: wnums = "third"
            
            textin = font.render("Input your " + wnums + " weight:", True, black, grey)
            textinRect = textin.get_rect()
            textinRect.center = (X/2, Y/2 - 20)
            
            screen.blit(textin, textinRect)
            
            if len(input) == 3:
                weight[wnum] = input
                wnum += 1
                input = ""
            if wnum == 3:
                inChoose = False
                inGame = True

        else:
            text1 = font.render("New Game", True, black, grey)
            text1Rect = text1.get_rect()
            text1Rect.center = (X/2, Y/2 - 20)
            
            screen.blit(text1, text1Rect)
            
            
            text2 = font.render("Leaderboard", True, black, grey)
            text2Rect = text2.get_rect()
            text2Rect.center = (X/2, Y/2 + 40)
            screen.blit(text2, text2Rect)
            
    pg.display.flip()
#KEY COMMANDS
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_SPACE:
                clicks += 1
            elif event.key == pg.K_BACKSPACE:
                input = input[:-1]
            elif event.key == pg.K_0 or event.key == pg.K_1 or event.key == pg.K_2 or event.key == pg.K_3 or event.key == pg.K_4 or event.key == pg.K_5 or event.key == pg.K_6 or event.key == pg.K_7 or event.key == pg.K_8 or event.key == pg.K_9:
                input += event.unicode
        elif event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            if text1Rect.collidepoint(pos):
                inChoose = True
                input = ""
                wnum = 0
            
pg.quit()
    