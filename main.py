import pygame as pg
import time
from math import sin, cos, radians, degrees, pi, sqrt, floor

pos1 = pg.transform.scale(pg.image.load("-1.png"), (500, 500))
pos2 = pg.transform.scale(pg.image.load("1.png"), (500, 500))
pos3 = pg.transform.scale(pg.image.load("2.png"), (500, 500))
pos4 = pg.transform.scale(pg.image.load("3.png"), (500, 500))

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

background = pg.image.load("Background.png")
background = pg.transform.scale(background, (500, 500))
backgroundRect = background.get_rect()
backgroundRect.center = (X/2+25, Y/2)

progress = pg.image.load("BAR.png")
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

score = 0
k = 4
difficulty = 4


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
        pos = pos1
    elif 66 > score >= 33:
        pos = pos2
    elif 100 > score >= 66:
        pos = pos3
    elif score >= 100:
        pos = pos4
        
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
        
    pg.display.flip()
#KEY COMMANDS
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_SPACE:
                clicks += 1  
        elif event.type == pg.QUIT:
            running = False   
pg.quit()
