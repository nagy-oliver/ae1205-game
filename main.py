import pygame as pg
import time
from math import sin, cos, radians, degrees, pi, sqrt 
import os

os.chdir("C:/Users/marti/Desktop/Weightlifting/ae1205-game")

pos1 = pg.transform.scale(pg.image.load("-1.png"), (500, 500))
pos2 = pg.transform.scale(pg.image.load("1.png"), (500, 500))
pos3 = pg.transform.scale(pg.image.load("2.png"), (500, 500))
pos4 = pg.transform.scale(pg.image.load("3.png"), (500, 500))

pg.init()

white = (255, 255, 255)
black = (0, 0, 0)


MINSLEEP = 0.001  # Minimum interval to sleep the CPU
tsim = 0.0  # Simulation time
tstart =  0.001 * pg.time.get_ticks()
dt = 1/60

X = 600
Y = 500

screen = pg.display.set_mode((X, Y))

pg.draw.rect(screen, (255, 255, 255), screen.get_rect())

clicks = 0
clickrate = 0
prevclicks = 0
running = True
t = 0
refreshtime = 0.5

font = pg.font.Font('freesansbold.ttf', 32)

score = 0
k = 2


while running:
#SIMULATION TIME
    tsim = tsim + dt
#REMAINDER TO SLEEP FOR CPU
    remainder = tsim - (0.001 * pg.time.get_ticks() - tstart)
    if remainder > MINSLEEP:
        time.sleep(remainder)
    
    t+=dt
    
    if t > refreshtime:
        t = 0
        curclicks = clicks - prevclicks
        prevclicks = clicks
        clickrate = curclicks/refreshtime
    
    text = font.render('Clickrate: ' + str(clickrate), True, black, white)
    textRect = text.get_rect()
    textRect.center = (X/2, 20)
    screen.blit(text, textRect)
    
    print(score)
    
    
    
    if clickrate >= 4:
        score = score + (clickrate-4) * k * dt
    elif clickrate < 4 and score > 0:
        score = score - 10*dt
    else:
        score = 0
   
    if score < 33:
        pos = pos1
    elif 66 > score >= 33:
        pos = pos2
    elif 100 > score >= 66:
        pos = pos3
    elif score >= 100:
        pos = pos4
        
    posrect = pos.get_rect()
    screen.blit(pos, posrect)
        
    pg.display.flip()
    pg.event.pump()   
#KEY COMMANDS   

    for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    clicks += 1
    keys = pg.key.get_pressed()     
# EXIT GAME
    if keys[pg.K_ESCAPE]:
        running = False

pg.quit()
